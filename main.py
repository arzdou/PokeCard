#!/usr/bin/env python3
from src.card_scripts import create_card
from src.sentiment import extract_info
import tweepy
import json


class TweetsListener(tweepy.StreamListener):

    def __init__(self,  api):
        super().__init__()
        self.api = api

    def on_connect(self):
        print("Estoy conectado")

    def on_status(self, status):
        if status.in_reply_to_status_id is not None: return

        create_card(status.user)
        info = extract_info(self.api, status.user)

        card_media = self.api.media_upload("output.png")
        string = "Aquí tienes @{}!\nAdemás he detectado {} tweets positivos y " \
                 "{} tweets negativos en tus últimos 200 tweets".format(status.user.screen_name, *info)
        self.api.update_status(string, status.id,
                               media_ids = [card_media.media_id],
                               auto_populate_reply_metadata=True)
        print("Tarjeta creada para "+status.user.name)

    def on_error(self, status_code):
        print("Oh no, ha ocurrido un error", status_code)


def main():
    with open("keys.json", "r") as infile:
        api_key, api_skey, access_token, access_stoken = json.load(infile).values()

    auth = tweepy.OAuthHandler(api_key, api_skey)
    auth.set_access_token(access_token, access_stoken)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)


    stream = TweetsListener(api)
    sreamingApi = tweepy.Stream(auth=api.auth, listener=stream)

    sreamingApi.filter(
        track=["@PokeCard_bot"]
    )

if __name__=="__main__":
    main()
