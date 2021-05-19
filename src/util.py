from minizinc import Instance, Model, Solver
from minizinc.dzn import parse_dzn as pd
from typing import Union, Dict, Any, List
import re


def parse_dzn(filepath: str) -> Dict[str, Union[int, list, float]]:
    '''
        Converts '.dzn' to a model arguments dict.
    '''

    with open(filepath, 'r') as f:
        return pd(f.read())


def solve_rogo(args: Dict[str, Union[int, list, float]]) -> Dict[str, Any]:
    '''
        Use system installation of mini-zinc to solve the rogo puzzle.
    '''

    model = Model("./src/ROGO.mzn")
    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)

    instance['problem'] = args['problem']
    instance['max_steps'] = args['max_steps']
    instance['cols'] = args['cols']
    instance['rows'] = args['rows']

    return instance.solve()


def parse_arg_array2d(args: Dict[str, Union[int, list, float]]) -> List[List[int]]:
    '''
        Parse an array2d object into python list.
    '''
    match = re.search(r'\[((.|\s)*)\]', args['problem'])

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

        if row_len >= args['cols']:
            row_len = 0
            result.append(temp)
            temp = []

    return result
