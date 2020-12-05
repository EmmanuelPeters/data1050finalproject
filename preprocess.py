"""This module defines a preprocess function to call to preprocess tweets before loading into a database."""

import re
import string
import pytest
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from xml.etree import ElementTree
import numpy as np

import nltk
nltk.download('punkt')
nltk.download('stopwords')


def preprocess_text(text):
    """Extracts lower-cased and stemmed tokens from input string and
    removes punctuation and stop words.

    1. Use `nltk.tokenize.sent_tokenize` and `.word_tokenize` for tokenizing
    2. Strip punctuations at both ends of words
    3. Stem words with the `stemmer`
    4. Filter stop words and empty words

    Use the given stemmer to stem each word. Use stop_words to filter out stop words.

    Args:
        text: str, one single str of text to be processed

    Returns:
        list of str, tokenized & stemmed words.
    """
    english_stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()
    text = nltk.tokenize.sent_tokenize(text)
    new_text = []
    for sentence in text:
        temp = nltk.tokenize.word_tokenize(sentence)
        temp = [stemmer.stem(word.lower()) for word in temp if word.isalnum() and word.lower() not in english_stop_words]
        new_text.append(temp)
    new_text = [item for sublist in new_text for item in sublist]
    return np.unique(new_text).tolist()


def test_processing_basic():
    assert preprocess_text("These are some sample sentences. Watch out!") == ['sampl', 'sentenc',
                                                                           'watch']
    assert preprocess_text("I could have any ? sentence here") == ['could', 'sentenc']

    assert preprocess_text("Look at this? Please! Cats in pajamas -.-. Short a Shorting Shorting.") == ['cat', 'look',
                                                                                                       'pajama',
                                                                                                       'pleas',
                                                                                                       'short']

