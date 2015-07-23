import requests
import json
import urllib2
import urllib
import argparse
import sys
import oauth2


#twitter
consumer_key = "C1JJKUku4UoAzfbRXIYX8YJov"
consumer_secret = "sjqNYRK7J30MyinX8nT9D10M9gjvYYRRtVjKootW8iEm6m8PlF"
Access_Token ="254776272-gnSSmg76q4e0be8rFwsw5ai00M3uJ36WM7HuMHGp"
Access_Token_Secret	="STvoOLUgEIzsCPrjrhvoJpPUma2KfJPhhRZONARv6ZvOw"

search_url = 'https://api.twitter.com/1.1/search/tweets.json?q=depressed+OR+hopeless+OR+upset&result_type=mixed&count=100'


getFullTweet = 'https://api.twitter.com/1.1/statuses/oembed.json?id={0}'


tweetlist = []
htmllist = []


#gets data in json form
def request(url):


    consumer = oauth2.Consumer(consumer_key, consumer_secret)
    oauth_request = oauth2.Request(method="GET", url=url)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': Access_Token,
            'oauth_consumer_key': consumer_key
        }
    )
    token = oauth2.Token(Access_Token, Access_Token_Secret)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def putInList(data):
    for x in range(0, 10):
        if 'text' in data['statuses'][x]:
            status = data['statuses'][x]['text']
            if float(textSentiment(status)) < -0.2:
                tweetlist.append(data['statuses'][x]['id_str'])
    return tweetlist

def getIds():
    response = request(search_url)
    return putInList(response)

def getEmbed():
    tlist = getIds()
    for id in tlist:
        url = 'https://api.twitter.com/1.1/statuses/oembed.json?id={0}'.format(id)
        embed = request(url)
        htmllist.append(embed['html'])
    return htmllist


def textSentiment(status):
    tweettext = urllib.quote(status.encode('utf8'))
    textscore=0
    url = urllib2.urlopen('http://access.alchemyapi.com/calls/text/TextGetTextSentiment?apikey=b03f613c7adeb0313b4f01b630dc8cd207f91d4d&outputMode=json&text={0}'.format(tweettext))
    sentiment = json.loads(url.read())
    if 'score' in sentiment['docSentiment']:
        textscore = sentiment['docSentiment']['score']
    return textscore

print getEmbed()






