import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

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
def display_top_statuses(topics, topic_tweets):
	for topic in topics:
		print '%s (Vol: %s)' % (topic.name, topic.tweet_volume)
		for tweet in topic_tweets[topic.name.encode('utf-8')]:
			if(tweet.lang == 'en'):
				name = tweet.user.name.encode('utf-8')
				status = tweet.text.encode('utf-8')
				print '\t' + name
				for line in linecutter(status):
					print '\t\t' + line
		print '\n'



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

	topics = get_top_topics(twitter_api, woeid)
	topic_tweets = get_top_statuses(twitter_api, topics, 10, 'en')

	display_top_statuses(topics, topic_tweets)
