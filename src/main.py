from minizinc import Instance, Model, Solver
from typing import Union, Dict

def parse_dzn(filepath: str) -> Dict[str, Union[int, list, float]]:
    from minizinc.dzn import parse_dzn as pd

    with open(filepath, 'r') as f:
        return pd(f.read())


if __name__ == '__main__':
    model = Model("./src/CavePuzzle.mzn")
    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)

    args = parse_dzn('./src/data.dzn')
    instance["puzzle_input"] = args["puzzle_input"]

    result = instance.solve()

    print(result["puzzle"])
