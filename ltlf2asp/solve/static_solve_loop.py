from typing import Optional, Iterable, Tuple
from ltlf2asp.solve.decode_model import Model, State, SolveResult, SolveStatus
import clingo  # type: ignore
from ltlf2asp.solve import SOLVE_STATIC


class Catch:
    def __init__(self) -> None:
        self.states: Optional[Tuple[State, ...]] = None

    def __call__(self, model: clingo.Model) -> bool:
        self.states = State.from_clingo_model(model)
        return False

    def get(self) -> Tuple[State, ...]:
        assert self.states is not None
        return self.states


def _solve(f: Iterable[clingo.Symbol], a: int, b: int) -> Optional[Model]:
    ctl = clingo.Control([f"-c a={a}", f"-c b={b}"])
    with ctl.backend() as backend:
        for symbol in f:
            lit = backend.add_atom(symbol)
            backend.add_rule([lit], [])

    ctl.load(SOLVE_STATIC)
    ctl.ground([("base", [])])

    trap = Catch()
    ans = ctl.solve(on_model=trap)
    if ans.satisfiable:
        return Model(trap.get())

    return None


def solve(f: Iterable[clingo.Symbol], max_horizon) -> SolveResult:
    a, b = 0, 1
    while b <= max_horizon:
        model = _solve(f, a, b)
        if model is not None:
            return SolveResult(SolveStatus.SATISFIABLE, b, model)

        a, b = b, b * 2

    return SolveResult(SolveStatus.UNSATISFIABLE, a, None)
