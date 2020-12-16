import tweepy
import json

def main():
    with open("keys.json", "r") as infile:
        api_key, api_skey, access_token, access_stoken = json.load(infile).values()

    auth = tweepy.OAuthHandler(api_key, api_skey)
    auth.set_access_token(access_token, access_stoken)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

if __name__=="__main__":
    main()
