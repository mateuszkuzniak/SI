import pygame as pg
from pygame import locals as lcs

from .util import get_board
from .model.board import Board, Cell, State
from .model.misc import Color


class App:
    def __init__(self, size=(800, 600)) -> None:
        pg.init()

        x, y = size

        board_rect = pg.Rect(x // 3,  # left
                             y // 20,  # top
                             x - x // 3 - x // 20,  # width
                             y // 20 * 18)  # height

        with open('./res/pre.html', 'r') as f:
            html = f.read()
            state = get_board(html)

        self.board = Board(board_rect, state)
        self.window = pg.display.set_mode(size, 0, 32)
        self.clock = pg.time.Clock()

    def setTitle(self, title: str) -> None:
        pg.display.set_caption(title)

    def draw(self) -> None:
        self.window.fill(Color.BLACK)
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
