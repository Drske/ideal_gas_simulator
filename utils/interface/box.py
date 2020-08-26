class Box:

    def __init__(self, text, value, x, y, font):
        self.text = text
        self.value = value
        self.x = x
        self.y = y
        self.font = font

    def draw(self, screen):
        box_text = self.font.render(
            self.text + ': ' + str(self.value), 1, (0, 255, 0))
        screen.blit(box_text, (self.x, self.y))
