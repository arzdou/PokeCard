from random import sample
from PIL import Image

def create_card(user=None):
    id_pokes = sample(range(1,152), 6)

    images_pokes = []
    for id_p in id_pokes:
        image = Image.open("images/pokemon/{:d}.png".format(id_p)).convert("RGBA")
        images_pokes.append(image)

    card_template = Image.open("images/card_template.png").convert("RGBA")
    card = Image.new("RGBA", card_template.size, 'white')

    x0, y0 = image.size
    for i, image in enumerate(images_pokes):
        x = 250 + 1.8*x0*(i%3)
        y = 100 + 1.3*y0*(i//3)
        card.paste(image, (int(x), int(y)), image)
    card.paste(card_template, (0, 0), card_template)
    card.save("output.png")

