import pygame as pg

pg.init()  # for fonts


class Font:
    NORMAL = pg.font.SysFont('roboto', 48, bold=True)


class Color:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
