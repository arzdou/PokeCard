from random import sample
from PIL import Image, ImageFont, ImageDraw
import json
import tweepy

def create_card(user=None):
    with open("images/trainers/trainers.txt", "r") as file:
        trainers = file.read()[:-1].split("\n")
    id_trainer = sample(trainers, 1)[0]
    id_pokes = sample(range(1,152), 6)

    try:
        name = user.screen_name
    except Exception as e:
        print("Name error: ", e)
        name = "user"

    images_pokes = []
    for id_p in id_pokes:
        image = Image.open("images/pokemon/{:d}.png".format(id_p)).convert("RGBA")
        image_cropped = image.crop(image.getbbox())
        images_pokes.append(image_cropped)

    image_trainer = Image.open("images/trainers/{}.png".format(id_trainer)).convert("RGBA")

    card_template = Image.open("images/card_template.png").convert("RGBA")
    resize_factor = 0.7
    card_template = card_template.resize([int(s*resize_factor) for s in card_template.size])

    card = Image.new("RGBA", card_template.size, 'white')

    for i, image in enumerate(images_pokes):
        x =resize_factor*(300 + 170*(i%3)) - image.size[0]//2
        y = resize_factor*(150 + 115*(i//3)) - image.size[1]//2
        card.paste(image, (int(x), int(y)), image)

    x_trainer = resize_factor*60
    y_trainer = resize_factor*150
    card.paste(image_trainer, (int(x_trainer), int(y_trainer)), image_trainer)

    card.paste(card_template, (0, 0), card_template)

    font = ImageFont.truetype('images/fonts/LEMONMILK-Regular.otf', 16)
    draw = ImageDraw.Draw(card)
    draw.text((resize_factor*450, resize_factor*45), name, (0,0,0), font=font)

    card.save("output.png")
    return card
