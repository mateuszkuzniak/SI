from enum import Enum
from typing import Tuple, Union, List
import pygame as pg

from .misc import Color


class State(Enum):
    EMPTY = 0
    PATH = -1
    WALL = -2


class Cell:
    def __init__(self, rect: pg.Rect, state: Union[State, int], font: pg.font.Font = None) -> None:
        self.state = state
        self.rect = rect
        self.font = font

    def draw(self, window: pg.Surface) -> None:
        if self.state == State.EMPTY:
            pg.draw.rect(window, Color.WHITE, self.rect)

        elif self.state == State.PATH:
            pg.draw.rect(window, Color.BLUE, self.rect)

        elif self.state == State.WALL:
            pg.draw.rect(window, Color.GREEN, self.rect)

        else:
            text = self.font.render(str(self.state), True, Color.BLACK)
            text_rect = text.get_rect(center=self.rect.center)

            pg.draw.rect(window, Color.BLUE, self.rect)
            window.blit(text, text_rect)

    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

    def switch_state(self):
        if self.state is State.EMPTY:
            self.state = State.PATH
        elif self.state is State.PATH:
            self.state = State.WALL
        elif self.state is State.WALL:
            self.state = State.EMPTY


class Board:
    def __init__(self, size: pg.Rect, initial_state: List[List[int]]) -> None:
        self.cell_font = pg.font.SysFont('roboto', size.width // 20, bold=True)
        self.size = size

        delta_x = size.width // 10
        delta_y = size.height // 10

        self.cells = []
        temp_y = size.top

        for row in initial_state:
            temp_x = size.left

            for state in row:
                rect = pg.Rect(temp_x, temp_y, delta_x, delta_y)
                if state == 0:
                    cell = Cell(rect, State.EMPTY)
                elif state == -1:
                    cell = Cell(rect, State.PATH)
                elif state == -2:
                    cell = Cell(rect, State.WALL)
                else:
                    cell = Cell(rect, state, self.cell_font)

                self.cells.append(cell)
                temp_x += delta_x

            temp_y += delta_y

    def draw(self, window: pg.Surface) -> None:
        for cell in self.cells:
            cell.draw(window)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> None:
        for cell in self.cells:
            if cell.is_clicked(mouse_pos):
                cell.switch_state()
