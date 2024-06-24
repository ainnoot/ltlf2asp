from typing import Optional, Tuple, List, Iterable
import clingo  # type: ignore
from ltlf2asp.solve.decode_model import State, SolveResult, SolveStatus, Model
from ltlf2asp.solve import SOLVE_INCREMENTAL


class Catch:
    def __init__(self) -> None:
        self.states: Optional[Tuple[State, ...]] = None

    def __call__(self, model: clingo.Model) -> bool:
        self.states = State.from_clingo_model(model)
        return False

    def get(self) -> Tuple[State, ...]:
        assert self.states is not None
        return self.states


def solve(f: Iterable[clingo.Symbol], max_horizon: int) -> SolveResult:
    a, b = 0, 1
    ctl = clingo.Control()

    with ctl.backend() as be:
        for symbol in f:
            be.add_rule([be.add_atom(symbol)], [])

    ctl.load(SOLVE_INCREMENTAL)
    parts: List[Tuple[str, List[clingo.Symbol]]] = [("base", []), ("formula", [])]
    while b <= max_horizon:
        for t in range(a, b):
            parts.append(("semantics", [clingo.Number(t)]))
        parts.append(("search", [clingo.Number(a), clingo.Number(b)]))
        # Ground
        ctl.ground(parts)
        parts.clear()

        # Set the valid segment to search for the last timepoint
        search = clingo.Function("search", [clingo.Number(a), clingo.Number(b)])
        ctl.assign_external(search, True)

        # Search, eventually capture model
        trace_cb = Catch()
        ans = ctl.solve(on_model=trace_cb)

        if ans.satisfiable:
            model = Model(trace_cb.get())
            return SolveResult(SolveStatus.SATISFIABLE, b, model)

        ctl.assign_external(search, False)
        a, b = b, 2 * b

    return SolveResult(SolveStatus.UNKNOWN, a, None)
