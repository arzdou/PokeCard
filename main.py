from card_scripts import create_card
from time import sleep
import tweepy
import json


class TweetsListener(tweepy.StreamListener):

    def __init__(self,  api):
        self.api = api

    def on_connect(self):
        print("Estoy conectado")

    def on_status(self, status):
        print("Creando trajeta para "+status.user.name)
        create_card(status)
        print("Carta creada")
        card_media = self.api.media_upload("output.png")
        sleep(10)
        self.api.update_status("Aquí tienes @{}!".format(status.user.screen_name),
                               status.id,
                               media_ids = [card_media.media_id],
                               auto_populate_reply_metadata=True)
        print("Se ha enviado el tweet")

    def on_error(self, status_code):
        print("Oh no, ha ocurrido un error", status_code)


def main():
    with open("keys.json", "r") as infile:
        api_key, api_skey, access_token, access_stoken = json.load(infile).values()

    auth = tweepy.OAuthHandler(api_key, api_skey)
    auth.set_access_token(access_token, access_stoken)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    api.update_status("Jaime que feo eres @Arzdou")
    stream = TweetsListener(api)
    sreamingApi = tweepy.Stream(auth=api.auth, listener=stream)

    sreamingApi.filter(
        track=["@PokeCard_bot"]
    )

if __name__=="__main__":
    main()
