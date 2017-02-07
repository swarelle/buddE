# -*- coding: utf-8 -*-
from pymongo import MongoClient
from sentiment_request import *

# Script for importing quotes from a cleaned text to the appropriate database after
# determining the quote's sentiments

# Sets up the database
client = MongoClient()
coll = client.buddE.motivational_quotes

# Opens and reads all lines of the cleaned text file (1 quote per line)
f = open('cleaned_text.txt', 'r')
lines = f.readlines()
f.close()

def getSentiment(s):
    """ gets sentiment score from Microsoft Text Analysis API """
    result = RequestSentiment(s).get_sentiment()
    print(result)
    score = ''
    for character in result:
        if character.isdigit():
            score += character
            if len(score) == 1:
                score += '.'
    score = float(score)
    return score

# Add all quotes with a sentiment score above the cut-off to the database
curr = 0
while curr < len(lines):
    quote = lines[curr]
    print(quote)
    score = getSentiment(quote)
    if score > 0.9:
        try:
            coll.insert_one({"_id": quote})
        except Exception as e:
            print("This error occurred:", e)
            pass
    curr += 1
