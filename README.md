# Apache Spark Streaming with TwitterAPI

Project create to learn a bit more about the Apache Spark Streaming module integrated with Twitter API. Any tips, suggestion or corrections are welcome :)

### Prerequisites

To run this project just follow the installation instructions. To execute, first run the python code (twitter_app.py) with

```
python3 twitter_app.py 
```
Them run the spark_app.py code

```
$SPARK_HOME/bin/spark-submit spark_app.py
```

### Installing

Naturally to run this project it's necessary to have Apache Spark, Python and Java JDK installed on your machine.
There are plenty of examples of how to install the JDK
For Python you can download it from https://www.python.org/downloads/ or via terminal
To install Spark, just follow the site overview https://spark.apache.org/docs/latest/

It's necessary to set the JAVA_HOME to use Spark and it's highly advisable to set the SPARK_HOME for easy use of the same