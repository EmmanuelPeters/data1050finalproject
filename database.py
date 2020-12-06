'''This module interacts with MongoDB database'''
# A logger is used to record the changes happen in database (i.e., reading data, insertion of new data, etc.)
import os
import logging
import pymongo
from collections import defaultdict
# ExpriringDict works as a cache. See https://www.pluralsight.com/guides/explore-python-libraries:-in-memory-caching-using-expiring-dict
from expiringdict import ExpiringDict
from utils import setup_logger, ymdhms


client = pymongo.MongoClient(os.environ.get("MONGO"))
logger = logging.Logger(__name__)
setup_logger(logger, 'db.log')
RESULT_CACHE_EXPIRATION = 60             # seconds
# Set up time limited cache for data fetching from MongoDB database
_fetch_all_cache = ExpiringDict(max_len=1, max_age_seconds=RESULT_CACHE_EXPIRATION)


def insert_data(data, collec, many):
    """
    Update MongoDB database with the given python dictionary.
    """
    db = client.get_database('tweetstorm')
    collection = db.get_collection(collec)
    if many:
        collection.insert_many(data)
        logger.info(f"{ymdhms()} inserted {len(data)} tweets to {collec} collection")
    else:
        collection.insert_one(data)
        logger.info(f"{ymdhms()} inserted data {data} to {collec} collection")


def fetch_all_from_db(collec):
    """
    Fetch data from MongoDB database as list of dictionary.
    """
    db = client.get_database("tweetstorm")
    collection = db.get_collection(collec)
    ret = list(collection.find())
    logger.info(str(len(ret)) + ' documents read from the db')
    return ret


def fetch_all(collec, allow_cached=False):
    """
    Fetch data from MongoDB database as list of dictionary. When `allow_cached`,
    attempt to retrieve timed cached from `_fetch_all_cache`; ignore cache and 
    call `_work` if cache expires or `allow_cached` is False.
    """
    def _work():
        data = fetch_all_from_db(collec)
        if len(data) == 0:
            return None
        return data

    if allow_cached:
        try:
            return _fetch_all_cache[collec]
        except KeyError:
            pass
    ret = _work()
    _fetch_all_cache[collec] = ret
    return ret


def fetch_all_as_time_series(allow_cached=False):
    """
    Fetch all data from database and convert to time series for plot.
    """
    data = fetch_all("keywords_frequencies", allow_cached)
    kw_freq = {}
    for d in data:
        if 'timestamp' not in d:
            continue
        t = d['timestamp']
        d.pop('timestamp', None)
        d.pop('_id', None)
        for k, f in d.items():
            if k not in kw_freq:
                kw_freq[k] = defaultdict(list)
            kw_freq[k]['timestamps'].append(t)
            kw_freq[k]['frequencies'].append(f)
    return kw_freq

def fetch_all_as_text(allow_cached=False):
    """
    Fetch all data from database for 'text' input into
    wordcloud visualization
    """
    text = fetch_all("tweets", allow_cached)
    return text

if __name__ == "__main__":
    print(fetch_all_as_time_series(allow_cached=True))