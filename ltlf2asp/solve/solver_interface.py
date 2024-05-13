from typing import Iterable

from ltlf2asp.solve.decode_model import SolveResult
from ltlf2asp.solve.incremental_solve_loop import solve as solve_incremental
from ltlf2asp.solve.static_solve_loop import solve as solve_static
import clingo  # type: ignore


class Solver:
    def __init__(self, is_incremental: bool, max_horizon: int) -> None:
        self.max_horizon = max_horizon
        self.is_incremental = is_incremental

    def solve(self, f: Iterable[clingo.Symbol]) -> SolveResult:
        if self.is_incremental:
            return solve_incremental(f, self.max_horizon)
        else:
            return solve_static(f, self.max_horizon)
