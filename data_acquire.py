"""
This module downloads data from Twitter and save it to MongoDB database. 
get_sample_batch and get_freq_batch will be called
"""
# How to filter tweets: https://developer.twitter.com/en/docs/tutorials/building-high-quality-filters
# How to connect to filtered stream endpoint: https://developer.twitter.com/en/docs/tutorials/listen-for-important-events
# How to connect to sample stream endpoint:
# How to lookup a tweet: 
import time
import sched
import requests
import os
import json
from database import insert_data
from preprocess import preprocess_text
from utils import ymdhms


# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
KEYWORDS = ['happy', 'sad', 'snow', 'gift']
# Key words for filter
TOP_WORDS = ['like', 'hate', 'i', 'to', 'a', '\"and\"', 'is', 'in', 'it', 'you', 'of', 'for', 'on', 'my',
             'at', 'that', 'with', 'me', 'do', 'have', 'just', 'this', 'be', 'so', 'are',
             'can', 'the']
# Filter rules
SAMPLE_RULES = [
        {"value": "(" + " OR ".join(TOP_WORDS) + ")" + " -is:retweet -is:reply -is:quote lang:en"}
    ]


def create_headers(bearer_token):
    '''A header is used to talk to twitter endpoints. It works as our identity and credential'''
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers):
    '''Get the current rule used by the filtered stream'''
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    return response.json()


def delete_all_rules(headers, rules):
    '''Delete all rules used by the filtered stream'''
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )


def set_rules(headers):
    '''Set the rules used by the filtered stream'''
    sample_rules = SAMPLE_RULES
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_filtered_stream(headers):
    '''Connect to a filtered stream. Returns an iterable object x. next(x) return a tweet.'''
    # Clear the old rules
    rules = get_rules(headers)
    delete_all_rules(headers, rules)
    # Set the new rules
    set_rules(headers)
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    return response.iter_lines()


def get_sample_stream(headers):
    while True:
        response = requests.get(
            "https://api.twitter.com/2/tweets/sample/stream" + 
            "?tweet.fields=created_at,geo,lang,public_metrics", 
            headers=headers,
            stream=True
        )
        print(response.status_code)
        if response.status_code == 200:
            return response.iter_lines()
        else:
            print("Request returned an error: {} {}".format(
                    response.status_code, response.text
                    )
            )
            time.sleep(3)


def read_stream(stream, keywords=KEYWORDS, batch_size=1000):
    '''
    Find the frequency of keywords in 1000 tweets. Creates a dictionary {'kw1': freq, 'kw2':freq,...}
    and tokenize the text and insert the dictionary to MongoDB databases.
    '''
    kw_freq = {kw: 0 for kw in keywords}
    i = 0
    tweets = []
    while i < batch_size:
        tweet = next(stream)
        if tweet:
            tweet = json.loads(tweet)
            if tweet['data']['lang'] == 'en':
                i += 1
                words = [word.lower() for word in tweet['data']['text'].split()]
                for word in words:
                    if word in kw_freq:
                        kw_freq[word] += 1
                tweet['timestamp'] = ymdhms()
                tweet['data']['text_tokenized'] = preprocess_text(tweet['data']['text'])
                tweets.append(tweet)
                # print(f"read_stream {i}/{batch_size}")
    kw_freq['timestamp'] = ymdhms()
    insert_data(kw_freq, 'keywords_frequencies', many=False)
    insert_data(tweets, 'tweets', many=True)
    

def main_loop():
    headers = create_headers(BEARER_TOKEN) 
    sample_stream = get_sample_stream(headers)
    while True:
        try:
            read_stream(sample_stream)
        except Exception as e:
            print(e)
            # logger.warning("_worker1 ignores exception and continues: {}".format(e))
        time.sleep(1)
         

if __name__ == "__main__":
    main_loop()