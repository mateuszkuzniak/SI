import pygame as pg
from pygame import locals as lcs

from .util import get_board
from .model.board import Board
from .model.misc import Color, Button


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
        self.size = size

        self.background = pg.transform.scale(
            pg.image.load('./res/background.png'), size)

        self.buttons = []
        self.__init_buttons()

    def __init_buttons(self, button_width=200, button_height=50):
        x, y = self.size
        button_x = x // 6 - button_width // 2

        self.buttons = [
            Button('RESET', pg.Rect(button_x, y // 10, button_width,
                                    button_height), onclick=self.board.reset_cells),
            Button('CHECK', pg.Rect(button_x, y // 10 * 2, button_width,
                                    button_height), onclick=lambda: None),
            Button('SOLVE', pg.Rect(button_x, y // 10 * 3, button_width,
                                    button_height), onclick=lambda: None),
            Button('<', pg.Rect(button_x, y // 10 * 4, button_width // 2,
                                button_height), onclick=lambda: None),
            Button('>', pg.Rect(button_x + button_width // 2, y // 10 * 4, button_width // 2,
                                button_height), onclick=lambda: None)
        ]

    def setTitle(self, title: str) -> None:
        pg.display.set_caption(title)

    def draw(self) -> None:
        self.window.fill(Color.BLACK)
        self.window.blit(self.background, (0, 0))

        self.board.draw(self.window)

        for b in self.buttons:
            b.draw(self.window)

    def run(self) -> bool:
        mouse_pos = pg.mouse.get_pos()
        self.board.handle_hover(mouse_pos)

        for b in self.buttons:
            b.handle_hover(mouse_pos)

        for event in pg.event.get():
            if event.type == lcs.QUIT:
                pg.quit()
                return False

            elif event.type == pg.MOUSEBUTTONUP:
                for b in self.buttons:
                    if b.is_clicked(mouse_pos):
                        b.use()
                        break

                else:
                    self.board.handle_click(mouse_pos)

        pg.display.update()
        self.clock.tick(30)
        return True


if __name__ == '__main__':
    app = App()
    app.setTitle('Bag Puzzle')

    while app.run():
        app.draw()
