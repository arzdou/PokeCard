from sentiment_analysis_spanish import sentiment_analysis
import pandas as pd
import tweepy
import re

def extract_info(api, user):
    tweets = api.user_timeline(screen_name=user.screen_name,
                               count=200,
                               include_rts=True
                               )
    out_tweets = [[t.created_at,
                   clean_text(t).text]
                   for t in tweets if t.lang=='es']

    df = pd.DataFrame(out_tweets, columns=["creation", "text"])
    return df

def clean_text(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = text.lower()
    return text

def get_sentiment(df):
    pass
