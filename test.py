from src.card_scripts import create_card
from src.sentiment import *
import tweepy
import json


def login():
    with open("keys.json", "r") as infile:
        api_key, api_skey, access_token, access_stoken = json.load(infile).values()
    auth = tweepy.OAuthHandler(api_key, api_skey)
    auth.set_access_token(access_token, access_stoken)
    twitter_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return twitter_api


api = login()
user = api.get_user("arzdou")
create_card(user).show()