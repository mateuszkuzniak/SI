import tkinter as tk
from tkinter import ttk
from typing import Generator, List, Optional, Tuple, Callable, Union

from src.util import SolverResults


class Input:
    def __init__(self, root: tk.Tk, text: str, position: Tuple[int, int], placeholder: str = None) -> None:
        x, y = position

        label = ttk.Label(root, text=text)
        label.place(x=x, y=y)

        self.entry = ttk.Entry(root)
        self.entry.place(x=x+140, y=y, width=50)

        if placeholder:
            self.entry.insert(0, placeholder)

    def insert(self, text: str) -> None:
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)

    def get(self) -> str:
        return self.entry.get()


class Button:
    def __init__(self, root: tk.Tk, text: str, position: Tuple[int, int], on_click: Callable, primary=False, width=100) -> None:
        x, y = position

        if primary:
            self.btn = tk.Button(root, text=text, command=on_click,
                                 bg='red', fg='white')
        else:
            self.btn = ttk.Button(root, text=text, command=on_click)

        self.btn.place(x=x, y=y, width=width)

    def destroy(self) -> None:
        self.btn.destroy()


class Cell:
    def __init__(self, root: tk.Tk, position: Tuple[int, int], placeholder: str = None) -> None:
        x, y = position

        self.val = tk.StringVar()
        self.val.trace('w', self.on_change)

        self.entry = tk.Entry(
            root, font="Helvetica 15 bold", justify=tk.CENTER, textvariable=self.val)
        self.entry.place(x=x, y=y, width=30, height=30)

        if placeholder:
            self.entry.insert(0, placeholder)

    def is_valid(self) -> bool:
        is_valid = False
        try:
            is_valid = int(self.val.get()) >= -1
        except:
            is_valid = self.val.get().strip() == ''

        if not is_valid:
            self.entry.configure({'bg': 'red', 'fg': 'white'})
            return False

        return True

    def mark(self, clear=False) -> None:
        if not clear:
            self.entry.configure({'bg': 'green', 'fg': 'white'})
        else:
            self.on_change()

    def on_change(self, *_args) -> None:
        if self.val.get() == '-1':
            self.entry.configure({'bg': 'black', 'fg': 'white'})
        else:
            self.entry.configure({'bg': 'white', 'fg': 'black'})

    def destroy(self) -> None:
        self.entry.destroy()


class CellBoard:
    def __init__(self) -> None:
        self.cells: List[Cell] = []

    def is_empty(self) -> bool:
        return not self.cells

    def has_errors(self) -> bool:
        had_error = False
        for row in self.cells:
            for c in row:
                if not c.is_valid():
                    had_error = True

        return had_error

    def clear(self) -> None:
        for row in self.cells:
            for c in row:
                c.destroy()

        self.cells = []

    def new_row(self, cells: List[Cell]) -> None:
        self.cells.append(cells)

    def __mark_generator(self, results: SolverResults) -> Generator:
        points = zip(results.x_steps, results.y_steps)

        for x, y in points:
            yield self.cells[x-1][y-1].mark()

    def show_solution(self, results: SolverResults, step=False) -> Optional[Generator]:
        if step:
            return self.__mark_generator(results)

        else:
            list(self.__mark_generator(results))

    def remove_markings(self) -> None:
        for row in self.cells:
            for c in row:
                c.mark(clear=True)

    def as_values(self) -> List[List[int]]:
        return [
            [int(c.val.get()) if c.val.get().strip() else 0 for c in row]
            for row in self.cells
        ]


class ResultsView:
    def __init__(self, root: tk.Tk, results: SolverResults, on_animate: Callable) -> None:
        self.l1 = ttk.Label(root, text='Solving summary:',
                            font="Helvetica 20 bold")
        self.l1.place(x=40, y=200)

        self.l2 = ttk.Label(
            root, text=f'The best solution has {results.points} total points.')
        self.l2.place(x=15, y=240)

        self.l3 = ttk.Label(
            root, text=f'Initialization took {results.init_time} seconds.')
        self.l3.place(x=15, y=255)

        self.l4 = ttk.Label(
            root, text=f'Solving took {results.solve_time} seconds.')
        self.l4.place(x=15, y=270)

        self.l5 = ttk.Label(
            root, text=f'Detailed statistics: \n{results.details_to_string()}')
        self.l5.place(x=15, y=295)

        self.step_btn = Button(
            root, 'Show step by step', (85, 450), width=150, on_click=on_animate)

    def destroy(self):
        if self.l1:
            self.l1.destroy()

        if self.l2:
            self.l2.destroy()

        if self.l3:
            self.l3.destroy()

        if self.l4:
            self.l4.destroy()

        if self.l5:
            self.l5.destroy()

        if self.step_btn:
            self.step_btn.destroy()
