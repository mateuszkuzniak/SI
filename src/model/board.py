from enum import Enum
from typing import Tuple, Union, List
from dataclasses import dataclass
import pygame as pg

from .misc import Color


class State(Enum):
    EMPTY = 0
    PATH = -1
    WALL = -2


class Cell:
    EMPTY_IMG = pg.image.load('./res/gray.png')
    PATH_IMG = pg.image.load('./res/white.png')
    WALL_IMG = pg.image.load('./res/black.png')

    def __init__(self, rect: pg.Rect, state: Union[State, int], font: pg.font.Font = None) -> None:
        self.state = state
        self.rect = rect
        self.font = font
        self.hovered = False

    def __transform_bg(self, background: pg.Surface):
        return pg.transform.scale(background, (self.rect.width, self.rect.width))

    def draw(self, window: pg.Surface) -> None:
        if self.state == State.EMPTY:
            window.blit(self.__transform_bg(Cell.EMPTY_IMG), self.rect)

        elif self.state == State.PATH:
            window.blit(self.__transform_bg(Cell.PATH_IMG), self.rect)

        elif self.state == State.WALL:
            window.blit(self.__transform_bg(Cell.WALL_IMG), self.rect)

        else:
            text = self.font.render(str(self.state), True, Color.BLACK)
            text_rect = text.get_rect(center=self.rect.center)

            window.blit(self.__transform_bg(Cell.PATH_IMG), self.rect)
            window.blit(text, text_rect)

        if self.hovered:
            alpha = pg.Surface(self.rect.size, pg.SRCALPHA)
            pg.draw.rect(alpha, Color.ALPHA_BLACK, alpha.get_rect())
            window.blit(alpha, self.rect)

        self.hovered = False

    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

    def switch_state(self):
        if self.state is State.EMPTY:
            self.state = State.PATH
        elif self.state is State.PATH:
            self.state = State.WALL
        elif self.state is State.WALL:
            self.state = State.EMPTY


@dataclass(order=True)
class Line:
    start: Tuple[int, int]
    end: Tuple[int, int]
    color: Color
    thickness: int

    def draw(self, window: pg.Surface) -> None:
        pg.draw.line(window, self.color, self.start, self.end, self.thickness)


class Board:
    def __init__(self, size: pg.Rect, initial_state: List[List[int]]) -> None:
        self.cell_font = pg.font.SysFont('roboto', size.width // 20, bold=True)
        self.size = size
        self.state = initial_state

        self.reset_cells()

        self.lines = []
        self.__init_lines()

    def reset_cells(self):
        self.cells = []
        self.__init_cells()

    def __init_cells(self) -> None:
        delta_x = self.size.width // 10
        delta_y = self.size.height // 10

        temp_y = self.size.top
        for row in self.state:
            temp_x = self.size.left

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

    def __init_lines(self, outside_thick=2, inside_thick=1, color=Color.WHITE) -> None:
        delta_x = self.size.width // 10
        delta_y = self.size.height // 10
        temp_x = self.size.left
        temp_y = self.size.top

        actual_topright = (temp_x + 10 * delta_x, temp_y)
        actual_bottomleft = (temp_x, temp_y + 10 * delta_y)
        actual_bottomright = (actual_topright[0], actual_bottomleft[1])

        self.lines = [
            Line(self.size.topleft, actual_topright, color, outside_thick),
            Line(self.size.topleft, actual_bottomleft, color, outside_thick),
            Line(actual_topright, actual_bottomright, color, outside_thick),
            Line(actual_bottomleft, actual_bottomright, color, outside_thick),
        ]

        temp_x = self.size.left
        temp_y = self.size.top + delta_y

        for _ in range(len(self.state) - 1):
            self.lines.append(
                Line((temp_x, temp_y), (actual_topright[0], temp_y), color, inside_thick))
            temp_y += delta_y

        temp_x = self.size.left + delta_x
        temp_y = self.size.top

        for _ in range(len(self.state) - 1):
            self.lines.append(
                Line((temp_x, temp_y), (temp_x, actual_bottomleft[1]), color, inside_thick))
            temp_x += delta_x

    def draw(self, window: pg.Surface) -> None:
        for cell in self.cells:
            cell.draw(window)

        for line in self.lines:
            line.draw(window)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> None:
        for cell in self.cells:
            if cell.is_clicked(mouse_pos):
                cell.switch_state()

    def handle_hover(self, mouse_pos: Tuple[int, int]) -> None:
        for cell in self.cells:
            cell.hovered = cell.is_clicked(mouse_pos) and isinstance(cell.state, State)
