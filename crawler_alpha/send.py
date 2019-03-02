#!/usr/bin/env python3

import pika
import requests
from bs4 import BeautifulSoup as bs
import json


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='tweets')


url = "https://twitter.com/Marvel"
response = requests.get(url)
soup = bs(response.content, 'lxml')
tweets = soup.find_all('li', 'js-stream-item')

for tweet in tweets:
    try:
        user_id = tweet.find('a', 'account-group').get('data-user-id')
        avatar = tweet.find('img', 'avatar').get('src')
        tweet_user = tweet.find('span', 'username').text
        user_fullname = tweet.find('strong', 'fullname').text
        tweet_text = tweet.find('p', 'tweet-text').text
        tweet_id = tweet['data-item-id']
        datetime = tweet.find('a', 'tweet-timestamp')['title']
        comment_count = tweet.findAll('span', {'class': 'ProfileTweet-actionCount'})[0].text.strip()
        retweet_count = tweet.findAll('span', {'class': 'ProfileTweet-actionCount'})[1].text.strip()
        like_count = tweet.findAll('span', {'class': 'ProfileTweet-actionCount'})[2].text.strip()
        data = {'User id': user_id,
                'User avatar': avatar,
                'Username': tweet_user,
                'User Fullname': user_fullname,
                'Tweet text': tweet_text,
                'Tweet id': tweet_id,
                'Datetime': datetime,
                'Comment count': comment_count,
                'Retweet count': retweet_count,
                'Like count': like_count}
        channel.basic_publish(exchange='',
                              routing_key='tweets',
                              body=json.dumps(data))
        print(" [x] Sent {}".format(data))            

    except:
        pass

connection.close()
