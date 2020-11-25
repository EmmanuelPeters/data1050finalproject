'''This module interacts with MongoDB database'''
# A logger is used to record the changes happen in database (i.e., reading data, insertion of new data, etc.)
import os
import logging
import pymongo
# ExpriringDict works as a cache. See https://www.pluralsight.com/guides/explore-python-libraries:-in-memory-caching-using-expiring-dict
from expiringdict import ExpiringDict
from utils import setup_logger


client = pymongo.MongoClient(os.environ.get("MONGO"))
logger = logging.Logger(__name__)
setup_logger(logger, 'db.log')
RESULT_CACHE_EXPIRATION = 200             # seconds
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
    else:
        collection.insert_one(data)
    logger.info(f"{data['timestamp']} inserted data {data}")


def fetch_all_from_db(collec):
    """
    Fetch data from MongoDB database as list of dict.
    """
    db = client.get_database("tweetstorm")
    collection = db.get_collection(collec)
    ret = list(collection.find())
    logger.info(str(len(ret)) + ' documents read from the db')
    return ret

def fetch_all(allow_cached=False):
    """Converts list of dicts returned by `fetch_all_bpa` to DataFrame with ID removed
    Actual job is done in `_worker`. When `allow_cached`, attempt to retrieve timed cached from
    `_fetch_all_cache`; ignore cache and call `_work` if cache expires or `allow_cached`
    is False.
    """
    def _work():
        data = fetch_all_from_db()
        if len(data) == 0:
            return None
        return data

    if allow_cached:
        try:
            return _fetch_all_cache['cache']
        except KeyError:
            pass
    ret = _work()
    _fetch_all_cache['cache'] = ret
    return ret

if __name__ == "__main__":
    print(fetch_all())