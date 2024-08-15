from dataclasses import dataclass
from typing import Iterable
import clingo
from ltlf2asp.solve import REYNOLDS
import json
from ltlf2asp.solve.decode_model import SolveStatus


@dataclass(frozen=True)
class TableauxResult:
    k: int
    status: SolveStatus

    @property
    def satisfiable(self):
        return self.status == SolveStatus.SATISFIABLE

    @property
    def unsatisfiable(self):
        return self.status == SolveStatus.UNSATISFIABLE

    @property
    def unknown(self):
        return self.status == SolveStatus.UNKNOWN

    def json(self):
        return json.dumps({"max_depth": self.k, "result": self.status.value}, indent=2)


class Catch:
    def __init__(self, verbose) -> None:
        self.status_ = SolveStatus.UNKNOWN
        self.verbose = verbose

    def __call__(self, model: clingo.Model) -> bool:
        if self.verbose:
            print(
                " Branch #{} - Cost {}".format(model.number, model.cost).center(80, "%")
            )
            sorted_symbols = sorted(
                model.symbols(shown=True), key=lambda x: x.arguments[0].number
            )
            print("\n".join(str(x) for x in sorted_symbols))
            print("".center(80, "%"))

        if model.optimality_proven:
            has_open_branch = model.cost[0] > 0
            if has_open_branch:
                self.status_ = SolveStatus.UNKNOWN

            elif model.cost[1] > 0:
                self.status_ = SolveStatus.UNSATISFIABLE

            else:
                self.status_ = SolveStatus.SATISFIABLE

            return False
        return True

    @property
    def status(self):
        return self.status_


class Reynolds:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose

    def solve(self, f: Iterable[clingo.Symbol], depth: int) -> TableauxResult:
        ctl = clingo.Control(
            ["-c depth={}".format(depth), "--opt-mode=optN", "--models=0"]
        )
        ctl.load(REYNOLDS)

        with ctl.backend() as be:
            for symbol in f:
                be.add_rule([be.add_atom(symbol)], [])

        cb = Catch(self.verbose)
        ctl.ground([("base", [])])
        _ = ctl.solve(on_model=cb)

        return TableauxResult(depth, cb.status)
