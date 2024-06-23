from dataclasses import dataclass
from typing import Iterable
from enum import StrEnum
import clingo
from ltlf2asp.solve import REYNOLDS
import json


class TableauxStatus(StrEnum):
    UNKNOWN = "UNKNOWN"
    UNSATISFIABLE = "UNSATISFIABLE"
    SATISFIABLE = "SATISFIABLE"


@dataclass(frozen=True)
class TableauxResult:
    k: int
    status: TableauxStatus

    @property
    def satisfiable(self):
        return self.status == TableauxStatus.SATISFIABLE

    @property
    def unsatisfiable(self):
        return self.status == TableauxStatus.UNSATISFIABLE

    @property
    def unknown(self):
        return self.status == TableauxStatus.UNKNOWN

    def json(self):
        return json.dumps({"max_depth": self.k, "result": self.status.value}, indent=2)


class Catch:
    def __init__(self, verbose) -> None:
        self.status_ = TableauxStatus.UNKNOWN
        self.verbose = verbose

    def __call__(self, model: clingo.Model) -> bool:
        if self.verbose:
            print(" Branch #{} ".format(model.number).center(80, "%"))
            sorted_symbols = sorted(
                model.symbols(shown=True), key=lambda x: x.arguments[0].number
            )
            print("\n".join(str(x) for x in sorted_symbols))
            print("".center(80, "%"))

        if model.optimality_proven:
            if model.cost == [0]:
                self.status_ = TableauxStatus.SATISFIABLE

            else:
                self.status_ = TableauxStatus.UNSATISFIABLE

            return False

        return True

    @property
    def status(self):
        return self.status_


class Reynolds:
    def __init__(self, depth: int, verbose: bool) -> None:
        self.depth = depth
        self.verbose = verbose

    def solve(self, f: Iterable[clingo.Symbol]) -> TableauxResult:
        ctl = clingo.Control(
            ["-c depth={}".format(self.depth), "--opt-mode=optN", "--models=0"]
        )
        ctl.load(REYNOLDS)

        with ctl.backend() as be:
            for symbol in f:
                be.add_rule([be.add_atom(symbol)], [])

        cb = Catch(self.verbose)
        ctl.ground([("base", [])])
        _ = ctl.solve(on_model=cb)

        return TableauxResult(self.depth, cb.status)
