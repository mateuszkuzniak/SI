import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.constants import S
from tkinter.messagebox import showerror, showinfo
from typing import Any, Dict, Generator, List, Union
from pprint import pprint
from datetime import timedelta

import threading as thrd

from .util import parse_dzn, solve_rogo, parse_arg_array2d
from .components import Button, CellBoard, Input, Cell


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(800, 600)
        self.title('Rogo Puzzle Solver')

        self.board = CellBoard()
        self.has_summary = False
        self.is_animating = False
        self.is_solving = False

        self.rows_input = Input(self, 'Enter canvas rows:',
                                (10, 10), placeholder='10')
        self.columns_input = Input(self, 'Enter canvas columns:',
                                   (10, 40), placeholder='10')

        Button(self, 'Create canvas', (220, 25),
               on_click=self.create_board)

        ttk.Separator(self, orient=tk.HORIZONTAL).place(x=0, y=70, width=340)

        Button(self, 'Read canvas from file', (70, 78),
               on_click=self.select_file, width=200)

        Button(self, '?', (280, 78),
               on_click=App.file_info, width=30)

        Button(self, 'Save current canvas to file', (70, 110),
               on_click=self.save_to_file, width=200)

        ttk.Separator(self, orient=tk.HORIZONTAL) .place(x=0, y=145, width=340)

        self.steps_input = Input(self, 'Enter maximum steps:', (10, 158))

        Button(self, 'Solve puzzle', (220, 156),
               on_click=self.handle_solution_button, primary=True)

        ttk.Separator(self, orient=tk.HORIZONTAL) .place(x=0, y=192, width=340)

        ttk.Separator(self, orient=tk.VERTICAL).place(x=340, y=0, relheight=1)

    @staticmethod
    def file_info():
        showinfo(
            title='Canvas file structure',
            message="""\
Data file structure should look like this:
    rows = 5;
    cols = 9;
    max_steps = 12;
    problem = array2d(1..rows, 1..cols,
    [
    2, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 3, 0, 0, 1, 0, 0, 2, 0,
    0, 0, 0, 0, 0, 0, -1, 0, 2,
    0, 0, 2, -1, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 2, 0, 0, 1, 0,
    ]);
""")

    def save_to_file(self):
        try:
            args = self.get_args_from_app_state()
        except:
            showerror(
                title="Can't save current canvas",
                message="You have to create a canvas and fill all the inputs on the left panel to save it."
            )
            return

        if not self.board.is_empty():
            filename = fd.asksaveasfilename(
                title='Save current canvas to a file',
                initialdir='~/',
                defaultextension='.dzn',
                filetypes=(
                    ('DZN files', '*.dzn'),
                    ('Text files', '*.txt'),
                )
            )
            with open(filename, 'w') as f:
                rows = [''.join([f"{cell}," for cell in row])
                        for row in args['problem']]
                cells = '\n'.join(rows)

                f.write(f"""\
rows = {args['rows']};
cols = {args['cols']};
max_steps = {args['max_steps']};
problem = array2d(1..rows, 1..cols,
[
{cells}
]);""")

    def select_file(self):
        filename = fd.askopenfilename(
            title='Open a ROGO problem describing text file',
            initialdir='~/',
            filetypes=(
                ('DZN files', '*.dzn'),
                ('Text files', '*.txt'),
            ))

        args = parse_dzn(filename)

        self.rows_input.insert(args['rows'])
        self.columns_input.insert(args['cols'])
        self.steps_input.insert(args['max_steps'])

        self.create_board(canvas=parse_arg_array2d(args))

    def handle_solution_button(self):
        if self.is_animating:
            return

        if int(self.steps_input.get()) % 2 != 0:
            showerror(
                title="Uneven steps number",
                message="Uneven step number prevents creating a cell loop and therefore is not solvable."
            )
            return

        if self.has_summary:
            self.summary_lbl.destroy()
            self.summary_lbl1.destroy()
            self.step_btn.destroy()
            self.has_summary = False

        self.board.remove_mark()

        if self.board.has_errors():
            showinfo(
                title='Error', message='Canvas has some errors, they have been highlighted.')
            return

        args = self.get_args_from_app_state()
        self.solution = None

        if not self.is_solving:
            self.is_solving = True
            t = thrd.Thread(target=self.solve_rogo, args=(args,))
            t.start()

    def solve_rogo(self, args: Dict[str, Union[int, List[List[int]]]]):
        self.solution = solve_rogo(args)

        self.is_solving = False
        self.show_summary()

    def show_summary(self):
        if self.solution:
            pprint(self.solution)

            init_time = self.solution.statistics['initTime'] / timedelta(milliseconds=1)
            solve_time = self.solution.statistics['solveTime'] / timedelta(milliseconds=1)
            variables = self.solution.statistics['variables']
            propagators = self.solution.statistics['propagators']
            propagations = self.solution.statistics['propagations']
            nodes = self.solution.statistics['nodes']
            failures = self.solution.statistics['failures']
            restarts = self.solution.statistics['restarts']
            peak_depth = self.solution.statistics['peakDepth']

            self.board.show_solution(self.solution)
            max_points = self.solution['sum_points']

            self.summary_lbl = ttk.Label(self, text='Solving summary:',
                                         font="Helvetica 20 bold")
            self.summary_lbl.place(x=40, y=200)

            self.summary_lbl1 = ttk.Label(
                self, text=f'The best solution has {max_points} points.')
            self.summary_lbl1.place(x=15, y=240)

            self.step_btn = Button(
                self, 'Show step by step', (85, 320), width=150, on_click=lambda: self.handle_step(self.solution))
            self.has_summary = True

    def handle_step(self, solution: Dict[str, Any], timeout=300):
        if not self.is_animating:
            self.is_animating = True

            self.board.remove_mark()
            gen = self.board.show_solution(solution, step=True)

            self.after(timeout, lambda: self.go_handle_step(gen, timeout))

    def go_handle_step(self, gen: Generator, timeout: int):
        try:
            next(gen)
            self.after(timeout, lambda: self.go_handle_step(gen, timeout))
        except StopIteration:
            self.is_animating = False

    def get_args_from_app_state(self) -> Dict[str, Union[int, List[List[int]]]]:
        return {
            'rows': int(self.rows_input.get()),
            'cols': int(self.columns_input.get()),
            'max_steps': int(self.steps_input.get()),
            'problem': self.board.as_values(),
        }

    def create_board(self, canvas: List[List[int]] = None):
        size_x = int(self.rows_input.get())
        size_y = int(self.columns_input.get())

        self.board.clear()

        canvas_start_x = 360
        canvas_start_y = 20

        delta = 31

        temp_y = canvas_start_y
        for x in range(size_x):
            temp_x = canvas_start_x
            temp = []

            for y in range(size_y):
                point = (temp_x, temp_y)
                if not canvas:
                    c = Cell(self, point, placeholder=' ')

                else:
                    elem = canvas[x][y]
                    c = Cell(self, point, placeholder=elem)

                temp.append(c)

                temp_x += delta

            temp_y += delta
            self.board.new_row(temp)


if __name__ == "__main__":
    app = App()
    app.mainloop()
