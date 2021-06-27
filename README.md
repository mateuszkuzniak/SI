### Solver łamigłówki Rogo przedstawionej jako problem spełniania ograniczeń w skończonej dziedzinie (CSP/FD)

#### Instalacja

1. Zainstaluj w systemie kompilator [MiniZinc](https://www.minizinc.org/software.html).
1. Dodaj folder instalacji kompilatora do ścieżki systemowej.
1. Zainstaluj w systemie interpreter [Python (3.8.10)](https://www.python.org/downloads/).
1. Dodaj folder instalacji interpretera do ścieżki systemowej.
1. Stwórz wirtualne środowisko interpretera Python i zainstaluj w nim biblioteki z pliku `requirements.txt`.

    * **Linux `Bash`:**
    ```bash
    # cd katalog główny repozytorium
    virtualenv -p python3 venv
    source ./venv/bin/activate
    pip install -r requirements.txt
    ```

    * **Windows `PowerShell`:**
    ```powershell
    # cd katalog główny repozytorium
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

1. Uruchom program (pamiętaj o każdorazowej aktywacji środowiska po restarcie powłoki - tak jak w poprzednim punkcie):

    ```bash
    # cd katalog główny repozytorium
    python -m src.app
    ```

#### Wygląd aplikacji

* Wynik poprawnego rozwiązania problemu
<p align="center">
  <img src="docs/final_report/images/1.png" width="500" title="Logo">
</p>

* Panel startowy
<p align="center">
  <img src="docs/final_report/images/2.png" width="500" title="Logo">
</p>

* Informacja o strukturze pliku
<p align="center">
  <img src="docs/final_report/images/3.png" width="500" title="Logo">
</p>

* Powiadomienie o błędach na planszy
<p align="center">
  <img src="docs/final_report/images/4.png" width="500" title="Logo">
</p>


> 2021 @ PUT - Sztuczna Inteligencja
