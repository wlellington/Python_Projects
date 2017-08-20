import sys
import operator
import requests
import json
import twitter
import classifier

def linecutter(string):
	lines =  string.split('\n')
	return lines

def get_top_topics(twitter_api, woeid): 
	# Pull trending topics from site based on location
	return twitter_api.GetTrendsWoeid(woeid, exclude=None)


def get_top_statuses(twitter_api, topics, num_tweets, lang_loc):
	# look up each topic
	topic_tweets = {}
	for topic in topics:
		query = topic.name.encode('utf-8')

		# get search results for topic
		results = twitter_api.GetSearch(term=query, 
				raw_query=None, 
				geocode=None, 
				since_id=None, 
				max_id=None,
				until=None, 
				since=None, 
				count=num_tweets, 
				lang=lang_loc, 
				locale=None,
				result_type='popular',
				include_entities=None)

		topic_tweets[query] = results
	return topic_tweets

# Print topic, user and tweet information
def display_top_statuses(topics, topic_tweets, topic_sents):
	
	topic_str = ''
	sent_str = ''
	for i in range(0, len(topics)):
		topic_str = '%s (Vol: %s)' % (topics[i].name, topics[i].tweet_volume)
		sent_str = 'Pos: %s, Neg: %s, Neu: %s' %(topic_sents[i]['4'], topic_sents[i]['2'], topic_sents[i]['0'])
		print "%s  [%s]" % (topic_str, sent_str)
	
		for tweet in topic_tweets[topics[i].name.encode('utf-8')]:
			if(tweet.lang == 'en'):
				name = tweet.user.name.encode('utf-8')
				status = tweet.text.encode('utf-8')
				format_tweet = ''
				format_tweet += '\t [%s] \t' % (name)
				lines = linecutter(status)
				
				if len(lines) >= 1:
					count = 0
						
					for line in lines:
						if count > 0:
							format_tweet += '\t\t\t\t'
						format_tweet += str(line) + '\n'
						count += 1
				print format_tweet
		print '\n'

# Make estimate of sentiment based on tweets for a topic
def analyze_tweets(topics, topic_tweets, sent_class):
	sentiment = None
	topic_sents = []
	queries = []
	for topic in topics:
		for tweet in topic_tweets[topic.name.encode('utf-8')]:
			if (tweet.lang == 'en'):
				queries.append(tweet.text.encode('utf-8'))

			topic_sents.append(sent_class.get_sentiments(queries))
	
	return topic_sents

# Display summary of topics and public sentiment
def print_topic_sentiments(topics, topic_sents):
	topic_str = ''
	sent_str = ''
	for i in range(0, len(topics)):
		topic_str = '%s (Vol: %s)' % (topics[i].name, topics[i].tweet_volume)
		sent_str = 'Pos: %s, Neg: %s, Neu: %s' %(topic_sents[i]['4'], topic_sents[i]['2'],topic_sents[i]['0'])
		print "%s : %s" % (topic_str, sent_str)


if __name__ == "__main__":
# Dictionary of tweets assigned to topics
	topic_tweets = {}

	# Credential info for Twitter Api
	twitter_consumer_key = ''
	twitter_consumer_secret = ''
	twitter_access_token = ''
	twitter_access_secret = ''

	# Twitter Api Object
	twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
			consumer_secret=twitter_consumer_secret,
			access_token_key=twitter_access_token,
			access_token_secret=twitter_access_secret)

	# Credential info for Watson Cloud?

	# Yahoo where in the world Id
	woeid = 23424977

	# Pul information from twitter abotu topics and related tweets
	topics = get_top_topics(twitter_api, woeid)
	topic_tweets = get_top_statuses(twitter_api, topics, 10, 'en')



	# create classifier (will implement pkl later)
	sentiment_classifier  = classifier.Classifier()
	sentiment_classifier.process_data('./data/finalizedtrain.csv')
	queries = ["Why do you not work?", 
		"That is not good", 
		"How many times do I have to eat this?", 
		"Star wars is not science fiction", 
		"You're a beatutiful girl",
		"Perfect happy good",
		'I love Python']
	#print sentiment_classifier.get_sentiments(queries)
	topic_sents = analyze_tweets(topics, topic_tweets, sentiment_classifier)
	       

	display_top_statuses(topics, topic_tweets, topic_sents)
