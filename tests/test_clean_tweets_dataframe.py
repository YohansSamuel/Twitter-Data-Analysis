import unittest
import pandas as pd
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join("../..")))
sys.path.append(".")

from extract_dataframe import read_json
from extract_dataframe import TweetDfExtractor
from clean_tweets_dataframe import Clean_Tweets

# For unit testing the data reading and processing codes, 
# we will need about 5 tweet samples. 
# Create a sample not more than 10 tweets and place it in a json file.
# Provide the path to the samples tweets file you created below
sampletweetsjsonfile = "./tests/sampletweets.json"   #put here the path to where you placed the file e.g. ./sampletweets.json. 
_, tweet_list = read_json(sampletweetsjsonfile)

class TestCleanTweetsDataFrame(unittest.TestCase):
    """
		A class for unit-testing function in the fix_clean_tweets_dataframe.py file

		Args:
        -----
			unittest.TestCase this allows the new class to inherit
			from the unittest module
	"""

    def setUp(self) -> pd.DataFrame:
        self.extracted = TweetDfExtractor(tweet_list[:5])
        self.df = self.extracted.get_tweet_df()
        self.clean_df = Clean_Tweets(self.df)
    
    #
    def test_extract_twitter_source(self):
        vals = ['Twitter for Android','Twitter for Android','Twitter for Android',
        'Twitter for Android','Twitter for iPhone']
        returned_source = self.df["source"].apply(self.clean_df.extract_twitter_source)
        self.assertEqual([x for x in returned_source], vals)

    #
    def test_remove_non_english_tweets(self):
        self.assertEqual(len(self.clean_df.remove_non_english_tweets(self.df)), len(self.df))
    #
    def test_remove_place_characters(self):
        vals =['','','Netherlands','Netherlands', 'Ayent Schweiz']
        returned_place = [x for x in self.clean_df.remove_place_characters(self.df)['place']]
        self.assertEqual(returned_place, vals)

    #
    def test_convert_to_numbers(self):
        df = self.clean_df.convert_to_numbers(self.df)
        vals = ['float64','float64', 'int64', 'int64', 'int64']
        returned_types = [df['polarity'].dtype,df['subjectivity'].dtype,df['retweet_count'].dtype,
            df['favorite_count'].dtype,df['followers_count'].dtype,]
        self.assertEqual(returned_types, vals)
    #
    def test_convert_to_datetime(self):
        df = self.clean_df.convert_to_datetime(self.df)
        self.assertEqual(df['created_at'].dtype, 'datetime64[ns, UTC]')
    
    #
    def test_drop_duplicate(self):
        df = self.clean_df.drop_duplicate(self.df)
        self.assertEqual(len(df), 5)
    #




if __name__ == "__main__":
    unittest.main()