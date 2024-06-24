from typing import Iterable

import clingo

from ltlf2asp.solve.decode_model import SolveResult, SolveStatus
from ltlf2asp.solve.static_solve_loop import _solve as search_model_in_segment
from ltlf2asp.solve.tableaux import Reynolds


def solve(
    f: Iterable[clingo.Symbol], g: Iterable[clingo.Symbol], max_horizon: int
) -> SolveResult:
    tableaux = Reynolds(False)

    a, b = 0, 8
    while b <= max_horizon:
        model = search_model_in_segment(f, a, b)

        if model is not None:
            return SolveResult(SolveStatus.SATISFIABLE, b, model)

        ans = tableaux.solve(g, b)
        if ans.unsatisfiable:
            return SolveResult(SolveStatus.UNSATISFIABLE, b, None)

        a, b = b, b * 2

    return SolveResult(SolveStatus.UNKNOWN, a, None)
