from typing import Optional, Iterable
from ltlf2asp.solve.decode_model import Model
import clingo
from ltlf2asp.solve import SOLVE_STATIC


class Catch:
    def __init__(self) -> None:
        self.model: Optional[Model] = None

    def __call__(self, model: clingo.Model) -> bool:
        self.model = Model.from_clingo_model(model)
        return False

    def get(self) -> Optional[Model]:
        return self.model


def _solve(f: Iterable[clingo.Symbol], a: int, b: int):
    ctl = clingo.Control([
        f"-c a={a}", f"-c b={b}"
    ])
    with ctl.backend() as backend:
        for symbol in f:
            lit = backend.add_atom(symbol)
            backend.add_rule([lit], [])

    ctl.load(SOLVE_STATIC)
    ctl.ground([("base", [])])

    trap = Catch()
    ans = ctl.solve(on_model=trap)
    if ans.satisfiable:
        return trap.get()

    return None


def solve(f: Iterable[clingo.Symbol], max_horizon):
    a, b = 0, 1
    while b < max_horizon:
        model = _solve(f, a, b)
        if model is not None:
            return model

        a, b = b, b * 2

    return None
