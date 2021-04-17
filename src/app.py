import pygame as pg
from pygame import locals as lcs

from .model.cell import Cell
from .model.misc import Font, Color


class App:
    def __init__(self, size=(800, 600)):
        pg.init()
        self.window = pg.display.set_mode(size, 0, 32)

    def setTitle(self, title):
        pg.display.set_caption(title)

    def draw(self):
        text = Font.NORMAL.render('HELLO WORLD', True, Color.WHITE)
        textRect = text.get_rect()
        textRect.centerx = self.window.get_rect().centerx
        textRect.centery = self.window.get_rect().centery

        # Draw the white background onto the surface
        self.window.fill(Color.BLACK)

        # Draw a blue poligon onto the surface
        pg.draw.polygon(self.window, Color.BLUE, ((250, 0),
                                                  (500, 200), (250, 400), (0, 200)))

        # Draw a green poligon onto the surface
        pg.draw.polygon(self.window, Color.GREEN, ((125, 100),
                                                   (375, 100), (375, 300), (125, 300)))

        # Draw a red circle onto the surface
        pg.draw.circle(self.window, Color.RED, (250, 200), 125)

        # Get a pixel array of the surface
        pixArray = pg.PixelArray(self.window)
        pixArray[480][380] = Color.WHITE
        del pixArray

        # Draw the text onto the surface
        self.window.blit(text, textRect)

    def run(self):
        pg.display.update()

        for event in pg.event.get():
            if event.type == lcs.QUIT:
                pg.quit()
                return False

        return True


if __name__ == '__main__':
    app = App()
    app.setTitle('some title')

    while app.run():
        app.draw()
