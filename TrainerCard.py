from random import sample
from PIL import Image

class TrainerCard:
    def __init__(self):
        self.id_pokes = sample(range(1,152), 6)

    def create_card(self):
        images_pokes = []
        for id_p in self.id_pokes:
            image = Image.open("images/pokemon/{:d}.png".format(id_p)).convert("RGBA")
            # composite = Image.composite(image, Image.new('RGBA', image.size, 'white'), image)
            images_pokes.append(image)

        card_template = Image.open("images/card_template.png").convert("RGBA")
        self.card = Image.new("RGBA", card_template.size, 'white')

        x0, y0 = image.size
        for i, image in enumerate(images_pokes):
            x = 250 + 1.8*x0*(i%3)
            y = 100 + 1.3*y0*(i//3)
            self.card.paste(image, (int(x), int(y)), image)
        self.card.paste(card_template, (0, 0), card_template)

    def show_card(self):
        try:
            self.card.show()
            self.card.save("output.png")
        except AttributeError:
            print("The card has not been created yet")


tc = TrainerCard()
tc.create_card()
tc.show_card()

