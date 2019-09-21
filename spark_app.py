from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests

conf = SparkConf()
conf.setAppName("TwitterStreamApp")

sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

ssc = StreamingContext(sc, 2)
ssc.checkpoint("checkpoint_TwitterApp")

dataStream = ssc.socketTextStream("localhost",9009)


def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']

def send_df_to_dashboard(df):
    # extract the hashtags from dataframe and convert them into array
    top_tags = [str(t.hashtag) for t in df.select("hashtag").collect()]
    # extract the counts from dataframe and convert them into array
    tags_count = [p.hashtag_count for p in df.select("hashtag_count").collect()]
    # initialize and send the data through REST API
    url = 'http://localhost:5001/updateData'
    request_data = {'label': str(top_tags), 'data': str(tags_count)}
    response = requests.post(url, data=request_data)

def process_rdd(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        sql_context = get_sql_context_instance(rdd.context)
        # convert the RDD to Row RDD
        row_rdd = rdd.map(lambda w: Row(hashtag=w[0], hashtag_count=w[1]))

        hashtags_df = sql_context.createDataFrame(row_rdd)
        hashtags_df.registerTempTable("hashtags")
        hashtag_counts_df = sql_context.sql("select hashtag, hashtag_count from hashtags order by hashtag_count desc limit 10")
        #hashtag_counts_df.show()
        send_df_to_dashboard(hashtag_counts_df)
        print("----------- DEBUG -----------")
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)
        print(sys.exc_info())

words = dataStream.flatMap(lambda line: line.split(" "))
# filter the words to get only hashtags, then map each hashtag to be a pair of (hashtag,1)
hashtags = words.filter(lambda w: '#' in w).map(lambda x: (x, 1))

#hashtags = words.map(lambda x: (x, 1))
tags_totals = hashtags.updateStateByKey(aggregate_tags_count)
tags_totals.foreachRDD(process_rdd)

ssc.start()
ssc.awaitTermination()
