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
        name = user.name
    except Exception as e:
        name = "user"

    images_pokes = []
    for id_p in id_pokes:
        image = Image.open("images/pokemon/{:d}.png".format(id_p)).convert("RGBA")
        images_pokes.append(image.resize([s*1 for s in image.size]))

    image_trainer = Image.open("images/trainers/{}.png".format(id_trainer)).convert("RGBA")

    card_template = Image.open("images/card_template.png").convert("RGBA")
    card_template = card_template.resize([int(s*1) for s in card_template.size])

    card = Image.new("RGBA", card_template.size, 'white')

    for i, image in enumerate(images_pokes):
        x = 230 + 170*(i%3)
        y = 100 + 115*(i//3)
        card.paste(image, (int(x), int(y)), image)

    card.paste(image_trainer, (70,150), image_trainer)

    card.paste(card_template, (0, 0), card_template)

    draw = ImageDraw.Draw(card)
    draw.text = ((70, 190), "Heymacarena", (250,0,0))

    card.save("output.png")
    return card
