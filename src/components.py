import tkinter as tk
from tkinter import ttk

from typing import Any, Dict, List, Tuple, Callable


class Input:
    def __init__(self, root: tk.Tk, text: str, position: Tuple[int, int], placeholder: str = None):
        x, y = position

        label = ttk.Label(root, text=text)
        label.place(x=x, y=y)

        self.entry = ttk.Entry(root)
        self.entry.place(x=x+140, y=y, width=50)

        if placeholder:
            self.entry.insert(0, placeholder)

    def insert(self, text: str):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)

    def get(self):
        return self.entry.get()


class Button:
    def __init__(self, root: tk.Tk, text: str, position: Tuple[int, int], on_click: Callable, primary=False, width=100):
        x, y = position

        if primary:
            self.btn = tk.Button(root, text=text, command=on_click,
                                 bg='red', fg='white')
        else:
            self.btn = ttk.Button(root, text=text, command=on_click)

        self.btn.place(x=x, y=y, width=width)

    def destroy(self):
        self.btn.destroy()


class Cell:
    def __init__(self, root: tk.Tk, position: Tuple[int, int], placeholder: str = None):
        x, y = position

        self.val = tk.StringVar()
        self.val.trace('w', self.on_change)

        self.entry = tk.Entry(
            root, font="Helvetica 15 bold", justify=tk.CENTER, textvariable=self.val)
        self.entry.place(x=x, y=y, width=30, height=30)

        if placeholder:
            self.entry.insert(0, placeholder)

    def is_valid(self):
        is_valid = False
        try:
            is_valid = int(self.val.get()) >= -1
        except:
            is_valid = self.val.get().strip() == ''

        if not is_valid:
            self.entry.configure({'bg': 'red', 'fg': 'white'})
            return False

        return True

    def mark(self, clear=False):
        if not clear:
            self.entry.configure({'bg': 'green', 'fg': 'white'})
        else:
            self.on_change()

    def on_change(self, *_args):
        if self.val.get() == '-1':
            self.entry.configure({'bg': 'black', 'fg': 'white'})
        else:
            self.entry.configure({'bg': 'white', 'fg': 'black'})

    def destroy(self):
        self.entry.destroy()


class CellBoard:
    def __init__(self):
        self.cells: List[Cell] = []

    def is_empty(self):
        return not self.cells

    def has_errors(self):
        had_error = False
        for row in self.cells:
            for c in row:
                if not c.is_valid():
                    had_error = True

        return had_error

    def clear(self):
        for row in self.cells:
            for c in row:
                c.destroy()

        self.cells = []

    def new_row(self, cells: List[Cell]):
        self.cells.append(cells)

    def __mark_generator(self, solution: Dict[str, Any]):
        points = zip(solution['x'], solution['y'])

        for x, y in points:
            yield self.cells[x-1][y-1].mark()

    def show_solution(self, solution: Dict[str, Any], step=False):
        print(solution)

        if step:
            return self.__mark_generator(solution)

        else:
            list(self.__mark_generator(solution))

    def remove_mark(self):
        for row in self.cells:
            for c in row:
                c.mark(clear=True)

    def as_values(self) -> List[List[int]]:
        return [
            [int(c.val.get()) if c.val.get().strip() else 0 for c in row]
            for row in self.cells
        ]
