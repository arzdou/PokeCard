from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import pandas as pd
import tweepy
import re

def extract_info(api, user):
    tweets = api.user_timeline(screen_name=user.screen_name,
                               count=200,
                               include_rts=True,
                               tweet_mode="extended"
                               )
    out_tweets = [[t.created_at,
                   clean_text(t.full_text)]
                   for t in tweets if t.lang=='es']

    df = pd.DataFrame(out_tweets, columns=["creation", "text_original"])

    translator = Translator()
    df["text"] = df["text_original"].apply(lambda t: translator.translate(t, src='es').text)

    analyzer = SentimentIntensityAnalyzer()
    df["sentiment"] = df["text"].apply(lambda t: analyzer.polarity_scores(t)['compound'])

    p = (df["sentiment"].to_numpy()>0).sum()
    n = (df["sentiment"].to_numpy()<0).sum()

    df.to_csv("test.csv", encoding='utf-8')
    return p, n, len(tweets)

def clean_text(text):
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = text.lower()
    return text

def get_sentiment(df):
    pass
