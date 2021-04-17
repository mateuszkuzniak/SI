from typing import Callable, Tuple
import pygame as pg


class Color:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    ALPHA_BLACK = (0, 0, 0, 125)


class Button:
    def __init__(self, text: str, rect: pg.Rect, onclick: Callable, bg_color=Color.BLACK, text_color=Color.WHITE):
        self.rect = rect
        self.onclick = onclick
        self.text = pg.font\
            .SysFont('roboto', rect.height // 3 * 2, True)\
            .render(text, True, text_color)

        self.bg_color = bg_color
        self.hovered = False

    def draw(self, window: pg.Surface):
        pg.draw.rect(window, self.bg_color, self.rect)
        window.blit(self.text, self.text.get_rect(center=self.rect.center))

        if self.hovered:
            alpha = pg.Surface(self.rect.size, pg.SRCALPHA)
            pg.draw.rect(alpha, Color.ALPHA_BLACK, alpha.get_rect())
            window.blit(alpha, self.rect)

    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def handle_hover(self, mouse_pos: Tuple[int, int]):
        self.hovered = self.is_clicked(mouse_pos)

    def use(self) -> None:
        self.onclick()
