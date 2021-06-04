### Solver łamigłówki Rogo przedstawionej jako problem spełniania ograniczeń w skończonej dziedzinie (CSP/FD)

#### Instalacja

1. Zainstaluj w systemie [MiniZinc](https://www.minizinc.org/)
1. Dodaj folder instalacji do ścieżki systemowej
1. Stwórz virtualenv o nazwie `venv` z paczkami z pliku `requirements.txt`, np:

    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

1. Uruchom program:

    ```powershell
    (venv) PS D:\RogoPuzzle> python -m src.app
    ```
