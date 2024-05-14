from typing import Dict, Tuple, Generator, Optional

import clingo
from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum


class SolveStatus(StrEnum):
    SATISFIABLE = "SAT"
    UNSATISFIABLE = "UNSAT"


@dataclass(frozen=True)
class SolveResult:
    status: SolveStatus
    k: int
    model: Optional["Model"]

    def __str__(self) -> str:
        return "{}[{}]".format(self.status.value, self.k)

    def __repr__(self) -> str:
        return self.__repr__()

    def json(self) -> str:
        import json

        if self.status == SolveStatus.UNSATISFIABLE:
            unsat_json = {"result": self.status, "k": self.k}

            return json.dumps(unsat_json, indent=4)

        assert self.model is not None
        sat_json = {
            "result": self.status,
            "k": self.k,
            "model": {
                "size": len(self.model.pi),
                "states": [
                    {prop: str(value).lower() for prop, value in state}
                    for state in self.model.pi
                ],
            },
        }
        return json.dumps(sat_json, indent=4)


@dataclass(frozen=True)
class State:
    sigma: Dict[str, bool]

    def __contains__(self, i: str) -> bool:
        return self.sigma[i]

    def __iter__(self) -> Generator[Tuple[str, bool], None, None]:
        for x, y in self.sigma.items():
            yield x, y

    @staticmethod
    def from_clingo_model(model: clingo.Model) -> Tuple["State", ...]:
        trace_dict: Dict[int, Dict[str, bool]] = defaultdict(dict)
        for x in model.context.symbolic_atoms.by_signature("trace", 2):
            symbol = x.symbol
            t = symbol.arguments[0].number
            a = symbol.arguments[1].string
            trace_dict[t][a] = model.contains(symbol)

        return tuple(State(trace_dict[i]) for i in range(len(trace_dict)))


@dataclass(frozen=True)
class Model:
    pi: Tuple[State, ...]

    def state(self, i: int) -> State:
        return self.pi[i]

    def __iter__(self) -> Generator[State, None, None]:
        yield from self.pi

    def __len__(self) -> int:
        return len(self.pi)
