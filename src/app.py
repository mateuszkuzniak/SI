import pygame as pg
from pygame import locals as lcs

from .util import get_board
from .model.board import Board
from .model.misc import Color


class App:
    def __init__(self, size=(800, 600)) -> None:
        pg.init()

        x, y = size
        square_width = min([x - x // 3 - x // 20, y // 20 * 18])

        board_rect = pg.Rect(x // 3,
                             y // 20,
                             square_width,
                             square_width)

        with open('./res/pre.html', 'r') as f:
            html = f.read()
            state = get_board(html)

        self.board = Board(board_rect, state)
        self.window = pg.display.set_mode(size, 0, 32)
        self.clock = pg.time.Clock()
        self.background = pg.transform.scale(
            pg.image.load('./res/background.png'), size)

    def setTitle(self, title: str) -> None:
        pg.display.set_caption(title)

    def draw(self) -> None:
        self.window.fill(Color.BLACK)
        self.window.blit(self.background, (0, 0))

        self.board.draw(self.window)

    def run(self) -> bool:
        for event in pg.event.get():
            if event.type == lcs.QUIT:
                pg.quit()
                return False

            elif event.type == pg.MOUSEBUTTONUP:
                self.board.handle_click(pg.mouse.get_pos())

        pg.display.update()
        self.clock.tick(30)
        return True


if __name__ == '__main__':
    app = App()
    app.setTitle('Bag Puzzle')

    while app.run():
        app.draw()
