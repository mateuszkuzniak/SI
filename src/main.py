from minizinc import Instance, Model, Solver

from .util import get_board, parse_dzn

if __name__ == '__main__':
    model = Model("./src/BagPuzzle.mzn")
    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)

    args = parse_dzn('./src/data.dzn')
    instance["puzzle_input"] = args["sudoku_input"]

    # with open('./res/pre.html', 'r') as f:
    #     html = f.read()
    #     instance["puzzle_input"] = get_board(html)

    result = instance.solve()

    print(result["puzzle"])
