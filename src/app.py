import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from typing import List, Tuple, Callable


def select_file():
    filetypes = (
        ('Text files', '*.txt'),
        ('DZN files', '*.dzn')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='~/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )


def file_info():
    showinfo(
        title='Canvas file structure',
        message='Should be like this: '
    )


class Input:
    def __init__(self, root: tk.Tk, text: str, position: Tuple[int, int], placeholder: str = None):
        x, y = position

        label = ttk.Label(root, text=text)
        label.place(x=x, y=y)

        self.entry = ttk.Entry(root)
        self.entry.place(x=x+140, y=y, width=50)

        if placeholder:
            self.entry.insert(0, placeholder)

    def get(self):
        return self.entry.get()


class Button:
    def __init__(self, root: tk.Tk, text: str, position: Tuple[int, int], on_click: Callable, primary=False, width=100):
        x, y = position

        if primary:
            btn = tk.Button(root, text=text, command=on_click,
                            bg='red', fg='white')
        else:
            btn = ttk.Button(root, text=text, command=on_click)

        btn.place(x=x, y=y, width=width)


class Cell:
    def __init__(self, root: tk.Tk, position: Tuple[int, int], placeholder: str = None):
        x, y = position

        self.entry = tk.Entry(
            root, font="Helvetica 15 bold", justify=tk.CENTER)
        self.entry.place(x=x, y=y, width=30, height=30)

        if placeholder:
            self.entry.insert(0, placeholder)

    def color(self, color: str):
        self.entry.configure({'background': color})

    def destroy(self):
        self.entry.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.geometry('1280x720')
        self.title('Rogo Puzzle Solver')

        self.cells: List[Cell] = []

        inp1 = Input(self, 'Enter canvas rows:', (10, 10), placeholder='10')
        inp2 = Input(self, 'Enter canvas columns:', (10, 40), placeholder='10')

        sep1 = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep1.place(x=0, y=70, width=340)

        Button(self,
               'Create canvas', (220, 25),
               on_click=lambda: self.create_board(int(inp1.get()), int(inp2.get())))

        Button(self,
               'Read canvas from file', (70, 78),
               on_click=select_file, width=200)

        Button(self,
               '?', (280, 78),
               on_click=file_info, width=30)

        sep2 = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep2.place(x=0, y=110, width=340)

        inp3 = Input(self, 'Enter maximum steps:', (10, 120))

        Button(self,
               'Solve puzzle', (220, 118),
               on_click=lambda: print(inp3.get()), primary=True)

        sep2 = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep2.place(x=0, y=152, width=340)

        self.draw_solve_info()

        sep3 = ttk.Separator(self, orient=tk.VERTICAL)
        sep3.place(x=340, y=0, relheight=1)

    def draw_solve_info(self):
        self.solutions = []
        index = 0

        ttk.Label(self, text='Solving summary:',
                  font="Helvetica 20 bold").place(x=40, y=160)

        ttk.Label(self, text=f'There are {len(self.solutions)} solutions.').place(x=15, y=200)

        ttk.Label(self, text=f'Currently showing {index + 1}.').place(x=15, y=220)

        Button(self, 'Previous solution', (10, 250), width=150, on_click=None)
        Button(self, 'Next solution', (180, 250), width=150, on_click=None)

    def create_board(self, size_x, size_y):
        for c in self.cells:
            c.destroy()

        self.cells = []

        canvas_start_x = 360
        canvas_start_y = 20

        delta = 31

        temp_x = canvas_start_x
        for _ in range(size_x):
            temp_y = canvas_start_y

            for _ in range(size_y):
                c = Cell(self, (temp_x, temp_y), placeholder='x')
                self.cells.append(c)

                temp_y += delta

            temp_x += delta


if __name__ == "__main__":
    app = App()
    app.mainloop()
