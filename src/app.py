import tkinter as tk

from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo

from typing import Generator, List

import threading as thrd

from .util import solve_rogo, SolverResults, SolverArguments
from .components import Button, CellBoard, Input, Cell, ResultsView


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(800, 600)
        self.title('Rogo Puzzle Solver')

        self.board = CellBoard()
        self.results: ResultsView = None

        self.is_animating = False
        self.is_solving = False

        self.create_main_menu()

    def create_main_menu(self) -> None:
        self.rows_input = Input(self, 'Enter canvas rows:',
                                (10, 10), placeholder='10')
        self.columns_input = Input(self, 'Enter canvas columns:',
                                   (10, 40), placeholder='10')

        Button(self, 'Create canvas', (220, 25),
               on_click=self.create_board)

        ttk.Separator(self, orient=tk.HORIZONTAL).place(x=0, y=70, width=340)

        Button(self, 'Read canvas from file', (70, 78),
               on_click=self.open_board_from_file, width=200)

        Button(self, '?', (280, 78),
               on_click=self.file_info, width=30)

        Button(self, 'Save current canvas to file', (70, 110),
               on_click=self.save_to_file, width=200)

        ttk.Separator(self, orient=tk.HORIZONTAL) .place(x=0, y=145, width=340)

        self.steps_input = Input(self, 'Enter maximum steps:', (10, 158))

        Button(self, 'Solve puzzle', (220, 156),
               on_click=self.handle_solution_button, primary=True)

        ttk.Separator(self, orient=tk.HORIZONTAL) .place(x=0, y=192, width=340)

        ttk.Separator(self, orient=tk.VERTICAL).place(x=340, y=0, relheight=1)

    def file_info(self) -> None:
        showinfo(
            title='Canvas file structure',
            message="""\
Data file structure should look like this:

rows = 5;
columns = 9;
steps = 12;
board = array2d(1..rows, 1..columns,
[
2, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 1, 0, 0, 2, 0,
0, 0, 0, 0, 0, 0, -1, 0, 2,
0, 0, 2, -1, 0, 0, 0, 0, 0,
0, 0, 0, 0, 2, 0, 0, 1, 0,
]);
""")

    def save_to_file(self) -> None:
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
                f.write(args.to_file_string())

    def open_board_from_file(self) -> None:
        filename = fd.askopenfilename(
            title='Open a ROGO problem describing text file',
            initialdir='~/',
            filetypes=(
                ('DZN files', '*.dzn'),
                ('Text files', '*.txt'),
            ))

        args = SolverArguments.from_dzn(filename)

        self.rows_input.insert(str(args.rows))
        self.columns_input.insert(str(args.columns))
        self.steps_input.insert(str(args.steps))

        self.create_board(canvas=args.board)

    def handle_solution_button(self):
        if self.is_animating:
            return

        if int(self.steps_input.get()) % 2 != 0:
            showerror(
                title="Uneven steps number",
                message="Uneven step number prevents creating a cell loop and therefore is not solvable."
            )
            return

        if self.results:
            self.results.destroy()

        self.board.remove_markings()

        if self.board.has_errors():
            showinfo(
                title='Error', message='Canvas has some errors, they have been highlighted.')
            return

        args = self.get_args_from_app_state()

        if not self.is_solving:
            self.is_solving = True

            thrd.Thread(target=self.handle_rogo_solve, args=(args,)).start()

    def handle_rogo_solve(self, args: SolverArguments):
        self.config(cursor='wait')
        self.update()

        self.solution = None
        self.solution = solve_rogo(args)

        self.is_solving = False
        self.config(cursor='')
        self.show_summary()

    def show_summary(self):
        self.board.show_solution(self.solution)

        self.results = ResultsView(self, self.solution,
                                   on_animate=lambda: self.animate_solution(self.solution))

    def animate_solution(self, solution: SolverResults, timeout=300):
        if not self.is_animating:
            self.is_animating = True

            self.board.remove_markings()
            gen = self.board.show_solution(solution, step=True)

            self.after(timeout, lambda: self.__handle_step(gen, timeout))

    def __handle_step(self, gen: Generator, timeout: int) -> None:
        try:
            next(gen)
            self.after(timeout, lambda: self.__handle_step(gen, timeout))
        except StopIteration:
            self.is_animating = False

    def get_args_from_app_state(self) -> SolverArguments:
        return SolverArguments(
            int(self.rows_input.get()),
            int(self.columns_input.get()),
            int(self.steps_input.get()),
            self.board.as_values()
        )

    def create_board(self, canvas: List[List[int]] = None) -> None:
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
