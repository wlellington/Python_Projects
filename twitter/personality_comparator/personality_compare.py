# Code based on that provided in the Learn the Watson API Course at:
# https://www.codecademy.com/learn/ibm-watson

# Output formatting modified by Layton Ellington

import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

def analyze(handle):

  # Token credentials for access to Twiter APi
  twitter_consumer_key = ''
  twitter_consumer_secret = ''
  twitter_access_token = ''
  twitter_access_secret = ''

  # Instance Twitter API object
  twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                  consumer_secret=twitter_consumer_secret,
                  access_token_key=twitter_access_token,
                  access_token_secret=twitter_access_secret)

  # Pull 200 tweets from user
  statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)

  # Create long string of all tweets
  text = ""
  for s in statuses:
    # Convert to UTF-8 if english
    if (s.lang =='en'):
      text += s.text.encode('utf-8')

  # Login credentials for Watson Personality insights
  pi_username = ''
  pi_password = ''

  # Instance personality insights
  personality_insights = PersonalityInsights(username=pi_username, password=pi_password)

  # Pull insights from text
  pi_result = personality_insights.profile(text)
  return pi_result

# Flatten JSON formatted results 
def flatten(orig):
  data = {}
  for c in orig['tree']['children']:
    if 'children' in c:
      for c2 in c['children']:
        if 'children' in c2:
          for c3 in c2['children']:
            if 'children' in c3:
              for c4 in c3['children']:
                if (c4['category'] == 'personality'):
                  data[c4['id']] = c4['percentage']
                  if 'children' not in c3:
                    if (c3['category'] == 'personality'):
                      data[c3['id']] = c3['percentage']
  return data

##########################################################
#                     Process script                     #
##########################################################

# Compare results from two users, create difference score
def compare(dict1, dict2):
	compared_data = {}
	for keys in dict1:
    		if dict1[keys] != dict2[keys]:
			compared_data[keys] = abs(dict1[keys] - dict2[keys])
	return compared_data

# Define users to query
user_handle = "@OfficiaIKanye"
celebrity_handle = "@realDonaldTrump"

# Create Personality data for both users based on recent tweets
user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)

# Flatten results for easy comparison
user = flatten(user_result)
celebrity = flatten(celebrity_result)

# Compare final results
compared_results = compare(user,celebrity)

# Sort output
sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

# Display all personality scores, sorted 
for keys, value in sorted_result:
    print (keys + ':'),
    print ('(' + user_handle),
    print (str(user[keys]) + ')'),
    print ('(' + celebrity_handle),
    print (str(celebrity[keys]) +')'),
    print ('[Difference'),
    print (str(compared_results[keys]) + ']')
