import socket
import sys
import requests
import requests_oauthlib
import json
import re
from datetime import datetime
import os

twitterApiKeys = open('TwitterAPIkeys', 'r')
CONSUMER_KEY = twitterApiKeys.readline().rstrip()
CONSUMER_SECRET = twitterApiKeys.readline().rstrip()
ACCESS_TOKEN = twitterApiKeys.readline().rstrip()
ACCESS_SECRET = twitterApiKeys.readline().rstrip()

my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)

def create_folder(folder_name):
	if os.path.isdir('./' + folder_name) is False:
		try:
			os.makedirs('./' + folder_name + '/')
		except OSError:
			print ('Error: Creating directory. ' +  folder_name)

def create_tweets_file(folder_name):
	create_folder(folder_name)
	file_name = folder_name + '/' + get_timestamp() + '.txt'

	file = open(file_name, 'w+')
	file.close()

	return file_name

def get_timestamp():
	dateTimeObj = datetime.now()
	return dateTimeObj.strftime("%d%b%Y%H%M%S%f")

def get_tweets():
	url = 'https://stream.twitter.com/1.1/statuses/filter.json'
	query_data = [('language', 'en'), ('locations', '-122.75,36.8,-121.75,37.8'),('track','#')]
	query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
	response = requests.get(query_url, auth=my_auth, stream=True)
	return response

def send_tweets_to_spark(http_resp, tcp_connection):
	file_name = create_tweets_file('tweets')

	for line in http_resp.iter_lines():
		try:
			tweets_file =  open(file_name, 'a')

			full_tweet = json.loads(line)
			print("Tweet Text: " + full_tweet['text'])
			tweet_text = str(full_tweet['text'].encode("utf-8"))
			print("Tweet Text: " + tweet_text)
			print ("------------------------------------------")

			tweets_file.write(tweet_text + '\n')
			tweets_file.close()

			tweet_data = bytes(tweet_text + '\n', 'utf-8') 
			tcp_connection.send(tweet_data)
		except:
			e = sys.exc_info()[0]
			print("Error: %s" % e)
			print(sys.exc_info())
			print('')

TCP_IP = "localhost"
TCP_PORT = 9009
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.")
resp = get_tweets()
send_tweets_to_spark(resp, conn)