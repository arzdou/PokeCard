from src.card_scripts import create_card
from src.sentiment import extract_info
import tweepy, json

with open("keys.json", "r") as infile:
    api_key, api_skey, access_token, access_stoken = json.load(infile).values()

auth = tweepy.OAuthHandler(api_key, api_skey)
auth.set_access_token(access_token, access_stoken)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.get_user("arass42")

df = extract_info(api, user)
print(df)
