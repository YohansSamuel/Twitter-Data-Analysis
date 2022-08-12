import unittest
import pandas as pd
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join("../..")))
sys.path.append(".")

from extract_dataframe import read_json
from extract_dataframe import TweetDfExtractor

# For unit testing the data reading and processing codes, 
# we will need about 5 tweet samples. 
# Create a sample not more than 10 tweets and place it in a json file.
# Provide the path to the samples tweets file you created below
sampletweetsjsonfile = "./tests/sampletweets.json"   #put here the path to where you placed the file e.g. ./sampletweets.json. 
_, tweet_list = read_json(sampletweetsjsonfile)