from minizinc.dzn import parse_dzn as pd
from bs4 import BeautifulSoup
from typing import List, Union, Dict

def parse_dzn(filepath: str) -> Dict[str, Union[int, list, float]]:
    '''
        Konwertuje '.dzn' na słownik argumentów dla modelu.
    '''

    with open(filepath, 'r') as f:
        return pd(f.read())

def get_board(html: str) -> List[List[int]]:
    '''
        Odczytuje planszę z htmla strony http://www.tectonicpuzzel.eu/cave-corral-puzzle-online.html
        Sztywny przykład w folderze res

        0  - puste pole
        1+ - wymaganie ze ścieżką
        -1 - ścieżka
        -2 - ściana
    '''
    soup = BeautifulSoup(html, features="html.parser")
    grid = soup.find(id='grid')

    board = []

    PATH = 'url("grint.jpg");'
    WALL = 'url("gras.jpg");'

    for row in grid.find_all("tr"):
        temp = []
        for cell in row.find_all("td", style=True):
            if cell.text.strip():
                temp.append(int(cell.text))

            else:
                cell_styles = cell['style'].split()

                if PATH in cell_styles:
                    temp.append(-1)
                elif WALL in cell_styles:
                    temp.append(-2)
                else:
                    temp.append(0)

        board.append(temp)

    assert len(board) == 10 and all([len(r) == 10 for r in board])

    return board


if __name__ == '__main__':
    '''
        Przykład odczytu planszy.
    '''
    with open('./res/post.html', 'r') as f:
        board = get_board(f.read())
        print(board)
