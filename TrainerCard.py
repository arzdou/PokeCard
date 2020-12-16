from random import sample
from PIL import Image

class TrainerCard:
    def __init__(self):
        self.px = 96
        self.id_pokes = sample(range(151), 6)

    def create_card(self):
        images_pokes = []
        for id_p in self.id_pokes:
            image = Image.open("images/pokemon/{:d}.png".format(id_p)).convert("RGBA")
            # composite = Image.composite(image, Image.new('RGBA', image.size, 'white'), image)
            images_pokes.append(image)

        self.card_template = Image.open("images/card_template.png").convert("RGBA")
        self.card = Image.new("RGBA", self.card_template.size, 'white')
        for i, image in enumerate(images_pokes):
            self.card.paste(image, (self.px*i, 0), image)

    def show_card(self):
        try:
            self.card.show()
            self.card.save("output.png")
        except AttributeError:
            print("The card has not been created yet")


tc = TrainerCard()
tc.create_card()
tc.show_card()

