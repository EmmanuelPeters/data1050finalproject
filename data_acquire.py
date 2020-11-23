"""This module downloads data from Twitter and save it to MongoDB database"""
# How to filter tweets: https://developer.twitter.com/en/docs/tutorials/building-high-quality-filters
# How to connect to filtered stream endpoint: https://developer.twitter.com/en/docs/tutorials/listen-for-important-events
import time
import sched
import requests
import os
import json
from database import upsert

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# Or directly input your bear token here

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAvXJwEAAAAAIcXaFn0%2BJTvnohILXLyQ9Dv5YTQ%3D9fJq0CoqICLCNSfyKEkDxDf4JbXlS0bTCY4MSackOwr71G33s4"
DOWNLOAD_PERIOD = 1   # seconds
KEYWORDS = ['happy', 'sad']
TOP_WORDS = ['like', 'hate', 'i', 'to', 'a', '\"and\"', 'is', 'in', 'it', 'you', 'of', 'for', 'on', 'my',
             'at', 'that', 'with', 'me', 'do', 'have', 'just', 'this', 'be', 'so', 'are',
             'can', 'the']
SAMPLE_RULES = [
        {"value": "(" + " OR ".join(TOP_WORDS) + ")" + " -is:retweet -is:reply -is:quote lang:en"}
    ]


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, rules):
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
    print(json.dumps(response.json()))


def set_rules(headers):
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


def get_stream(headers):
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


def ymdhms(delimiter='-'):
    t = time.localtime()
    t = [str(i) for i in t[:6]]
    return delimiter.join(t)


def update_once(keywords=KEYWORDS):
    kw_freq = {kw: 0 for kw in keywords}
    headers = create_headers(BEARER_TOKEN)
    stream = get_stream(headers)
    i = 0
    while i < 1000:
        tweet = next(stream)
        if tweet:
            i += 1
            words = [word.lower() for word in json.loads(tweet)['data']['text'].split()]
            for word in words:
                if word in kw_freq:
                    kw_freq[word] += 1
    kw_freq['timestamp'] = ymdhms()
    upsert(kw_freq)


def main_loop(timeout=DOWNLOAD_PERIOD):
    # bearer_token = os.environ.get("BEARER_TOKEN")
    bearer_token = BEARER_TOKEN
    headers = create_headers(bearer_token)
    rules = get_rules(headers)
    delete_all_rules(headers, rules)
    set_rules(headers)
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
        try:
            update_once()
        except Exception as e:
            print(e)
            # logger.warning("main loop worker ignores exception and continues: {}".format(e))
        scheduler.enter(timeout, 1, _worker)    # schedule the next event

    scheduler.enter(0, 1, _worker)              # start the first event
    scheduler.run(blocking=True)


if __name__ == "__main__":
    main_loop()