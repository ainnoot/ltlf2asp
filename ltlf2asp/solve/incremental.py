from typing import Set, Optional
import clingo
from ltlf2asp.solve.decode_model import Model
from ltlf2asp.solve import INCREMENTAL


class Catch:
    def __init__(self):
        self.model: Optional[Model] = None

    def __call__(self, model: clingo.Model):
        self.model = Model.from_clingo_model(model)
        return False

    def get(self):
        return self.model


def solve(f: Set[clingo.Symbol], max_horizon, strategy):
    a, b = 0, 1
    ctl = clingo.Control()

    with ctl.backend() as be:
        for symbol in f:
            be.add_rule([be.add_atom(symbol)], [])

    ctl.load(INCREMENTAL)
    parts = [("base", []), ("formula", [])]
    while b <= max_horizon:
        for t in range(a, b):
            parts.append(("semantics", [clingo.Number(t)]))

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
            return trace_cb.get()

        ctl.assign_external(search, False)
        a, b = strategy(a, b)

    return None
