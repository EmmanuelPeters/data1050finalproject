'''This module interacts with MongoDB database'''
# A logger is used to record the changes happen in database (i.e., reading data, insertion of new data, etc.)
import logging
import pymongo
import pandas as pds
# ExpriringDict works as a cache. See https://www.pluralsight.com/guides/explore-python-libraries:-in-memory-caching-using-expiring-dict
from expiringdict import ExpiringDict
from utils import setup_logger

client = pymongo.MongoClient()
logger = logging.Logger(__name__)
setup_logger(logger, 'db.log')
RESULT_CACHE_EXPIRATION = 10             # seconds
# Set up time limited cache for data fetching from MongoDB database
_fetch_all_as_df_cache = ExpiringDict(max_len=1, max_age_seconds=RESULT_CACHE_EXPIRATION)

def upsert(df):
    """
    Update MongoDB database with the given `DataFrame`.
    """
    pass

def fetch_all_bpa():
    """
    Fetch data from MongoDB database as list or dict.
    """
    pass

def fetch_all_as_df(allow_cached=False):
    """Converts list of dicts returned by `fetch_all_bpa` to DataFrame with ID removed
    Actual job is done in `_worker`. When `allow_cached`, attempt to retrieve timed cached from
    `_fetch_all_as_df_cache`; ignore cache and call `_work` if cache expires or `allow_cached`
    is False.
    """
    pass

if __name__ == "__main__":
    print(fetch_all_as_df())