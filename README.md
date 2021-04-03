### Solver łamigłówki Bag Puzzle (aka Coral Puzzle, Cave Puzzle) przedstawionej jako problem spełniania ograniczeń w skończonej dziedzinie (CSP/FD)

#### Instalacja

1. Zainstaluj w systemie [MiniZinc](https://www.minizinc.org/)
1. Dodaj folder instalacji do ścieżki systemowej
1. Stwórz virtualenv o nazwie `venv` z paczkami z pliku `requirements.txt`, np:

    ```powershell
    python -m venv venv
    venv/Scripts/activate
    pip install -r requirements.txt
    ```

1. Lecisz:

    ```powershell
    (venv) PS D:\Repos\SI> python .\src\main.py
    [[5, 3, 1, 4, 8, 9, 6, 2, 7], [6, 4, 9, 7, 5, 2, 8, 1, 3], ...
    ```
