from typing import Tuple, Iterable

import clingo
from ltlf2asp.solve.decode_model import State
from ltlf2asp.solve import CHECK


def trace_2(t: int, value: str, positive: bool) -> clingo.Symbol:
    return clingo.Function("trace", [clingo.Number(t), clingo.String(value)], positive)


def time_1(t: int) -> clingo.Symbol:
    return clingo.Function("time", [clingo.Number(t)])


def check_trace(trace: Tuple[State, ...], formula: Iterable[clingo.Symbol]) -> bool:
    ctl = clingo.Control()
    ctl.load(CHECK)

    with ctl.backend() as be:
        for x in formula:
            lit = be.add_atom(x)
            be.add_rule([lit], [])

        for t, state in enumerate(trace):
            lit = be.add_atom(time_1(t))
            be.add_rule([lit], [])

            for p, val in state:
                lit = be.add_atom(trace_2(t, p, val))
                be.add_rule([lit], [])

    ctl.ground([("base", [])])
    ans = ctl.solve()

    return not (ans.satisfiable is None or not ans.satisfiable)
