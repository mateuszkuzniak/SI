from minizinc import Instance, Model, Solver, Status
from minizinc.dzn import parse_dzn as pd

from typing import Optional, Tuple, Union, Dict, List
from dataclasses import dataclass
import re


def parse_dzn(filepath: str) -> Dict[str, Union[int, list, float]]:
    '''
        Converts '.dzn' to a model arguments dict.
    '''
    with open(filepath, 'r') as f:
        return pd(f.read())


def parse_arg_array2d(args: Dict[str, Union[int, list, float]]) -> List[List[int]]:
    '''
        Parse an array2d object into python list.
    '''
    match = re.search(r'\[((.|\s)*)\]', args['board'])

    if match:
        numbers = [int(e) for e in re.split(
            r'[\s,]', match.group(1)) if e.strip()]
    else:
        raise ValueError('invalid data structure')

    result = []
    temp = []
    row_len = 0

    for n in numbers:
        temp.append(n)
        row_len += 1

        if row_len >= args['columns']:
            row_len = 0
            result.append(temp)
            temp = []

    return result


@dataclass(order=True)
class SolverArguments:
    rows: int
    columns: int
    steps: int
    board: List[List[int]]

    @staticmethod
    def from_dzn(filepath: str) -> "SolverArguments":
        args = parse_dzn(filepath)
        board = parse_arg_array2d(args)

        return SolverArguments(args['rows'], args['columns'], args['steps'], board)

    def to_file_string(self) -> str:
        rows = [''.join([f"{cell}," for cell in row])
                for row in self.board]
        cells = '\n'.join(rows)

        return f"""\
rows = {self.rows};
columns = {self.columns};
steps = {self.steps};
board = array2d(1..rows, 1..columns,
[
{cells}
]);"""


@ dataclass(order=True)
class SolverResults:
    x_steps: List[int]
    y_steps: List[int]
    point_steps: List[int]
    points: List[int]
    init_time_ms: float
    solve_time_ms: float
    variables: int
    propagators: int
    propagations: int
    nodes: int
    failures: int
    restarts: int
    peak_depth: int

    @ staticmethod
    def from_minizinc_results(solution: Tuple[Status, Optional[Union[List[Dict], Dict]], Dict]) -> "SolverResults":
        return SolverResults(
            solution['row'],
            solution['column'],
            solution['points'],
            solution['sum_points'],
            solution.statistics['initTime'].total_seconds() / 1000,
            solution.statistics['solveTime'] .total_seconds() / 1000,
            solution.statistics['variables'],
            solution.statistics['propagators'],
            solution.statistics['propagations'],
            solution.statistics['nodes'],
            solution.statistics['failures'],
            solution.statistics['restarts'],
            solution.statistics['peakDepth'],
        )


def solve_rogo(args: SolverArguments, model_path: str = "./src/rogopuzzle.mzn", solver: str = 'gecode') -> SolverResults:
    '''
        Use system installation of mini-zinc to solve the rogo puzzle.
    '''
    model = Model(model_path)
    solver = Solver.lookup(solver)
    instance = Instance(solver, model)

    instance['board'] = args.board
    instance['steps'] = args.steps
    instance['columns'] = args.columns
    instance['rows'] = args.rows

    solution = instance.solve()
    return SolverResults.from_minizinc_results(solution)
