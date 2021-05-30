import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from typing import Any, Dict, Generator, List


from .util import parse_dzn, solve_rogo, parse_arg_array2d
from .components import Button, CellBoard, Input, Cell


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(800, 600)
        self.title('Rogo Puzzle Solver')

        self.board = CellBoard()
        self.has_summary = False

        self.cols_in = Input(self, 'Enter canvas columns:',
                             (10, 10), placeholder='10')
        self.rows_in = Input(self, 'Enter canvas rows:',
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

        self.steps_in = Input(self, 'Enter maximum steps:', (10, 158))

        Button(self, 'Solve puzzle', (220, 156),
               on_click=self.handle_solution_button, primary=True)

        ttk.Separator(self, orient=tk.HORIZONTAL) .place(x=0, y=192, width=340)

        ttk.Separator(self, orient=tk.VERTICAL).place(x=340, y=0, relheight=1)

    @staticmethod
    def file_info():
        showinfo(
            title='Canvas file structure',
            message="""
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
            """
        )

    def save_to_file(self):
        # TODO
        pass

    def select_file(self):
        filename = fd.askopenfilename(
            title='Open a ROGO problem describing text file',
            initialdir='~/',
            filetypes=(
                ('DZN files', '*.dzn'),
                ('Text files', '*.txt'),
            ))

        args = parse_dzn(filename)

        self.cols_in.insert(args['rows'])
        self.rows_in.insert(args['cols'])
        self.steps_in.insert(args['max_steps'])

        self.create_board(canvas=parse_arg_array2d(args))

    def handle_solution_button(self):
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

        self.solutions = [solve_rogo(args)]
        print(self.solutions)

        index = 0
        self.board.show_solution(self.solutions[index])
        max_points = self.solutions[index]['sum_points']

        self.summary_lbl = ttk.Label(self, text='Solving summary:',
                                     font="Helvetica 20 bold")
        self.summary_lbl.place(x=40, y=200)

        if len(self.solutions) <= 1:
            self.summary_lbl1 = ttk.Label(
                self, text=f'There is one best solution of {max_points} points.')
            self.summary_lbl1.place(x=15, y=240)
        else:
            self.summary_lbl1 = ttk.Label(
                self, text=f'There are {len(self.solutions)} best solutions with a sum of {max_points} points. Currently showing {index + 1}.')
            self.summary_lbl1.place(x=15, y=240)

        self.step_btn = Button(
            self, 'Show step by step', (85, 320), width=150, on_click=lambda: self.handle_step(self.solutions[index]))
        self.has_summary = True

    def handle_step(self, solution: Dict[str, Any], timeout=300):
        self.board.remove_mark()
        gen = self.board.show_solution(solution, step=True)
        last_id = ''

        try:
            last_id = self.after(
                timeout, lambda: self.go_handle_step(gen, timeout, last_id))

        except StopIteration:
            pass

    def go_handle_step(self, gen: Generator, timeout: int, last_id: str):
        next(gen)
        last_id = self.after(
            timeout, lambda: self.go_handle_step(gen, timeout, last_id))

    def get_args_from_app_state(self):
        return {
            'rows': int(self.cols_in.get()),
            'cols': int(self.rows_in.get()),
            'max_steps': int(self.steps_in.get()),
            'problem': self.board.as_values(),
        }

    def create_board(self, canvas: List[List[int]] = None):
        size_x = int(self.cols_in.get())
        size_y = int(self.rows_in.get())

        self.board.clear()

        canvas_start_x = 360
        canvas_start_y = 20

        delta = 31

        temp_x = canvas_start_x
        for x in range(size_x):
            temp_y = canvas_start_y
            temp = []

            for y in range(size_y):
                point = (temp_x, temp_y)
                if not canvas:
                    c = Cell(self, point, placeholder=' ')

                else:
                    elem = canvas[x][y]
                    c = Cell(self, point, placeholder=elem)

                temp.append(c)

                temp_y += delta

            temp_x += delta
            self.board.new_row(temp)


if __name__ == "__main__":
    app = App()
    app.mainloop()
