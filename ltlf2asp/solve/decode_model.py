from typing import Dict, Tuple, Generator, Optional

import clingo
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    sigma: Dict[str, bool]

    def __contains__(self, i: str) -> bool:
        return self.sigma[i]

    def __iter__(self) -> Generator[Tuple[str, bool], None, None]:
        for x, y in self.sigma.items():
            yield x, y

    @staticmethod
    def from_clingo_model(model: clingo.Model) -> Optional[Tuple["State", ...]]:
        if model is None:
            return None

        trace_dict: Dict[int, Dict[str, bool]] = defaultdict(dict)
        for x in model.context.symbolic_atoms.by_signature("trace", 2):
            symbol = x.symbol
            t = symbol.arguments[0].number
            a = symbol.arguments[1].string
            trace_dict[t][a] = model.contains(symbol)

        return tuple(State(trace_dict[i]) for i in range(len(trace_dict)))


@dataclass(frozen=True)
class Model:
    result: str
    k: int
    pi: Optional[Tuple[State, ...]]

    def state(self, i: int) -> State:
        return self.pi[i]

    def __iter__(self) -> Generator[State, None, None]:
        yield from self.pi

    def __len__(self) -> int:
        return len(self.pi)

    def json(self):
        import json

        if self.pi is None:
            unsat_json = {"result": self.result, "k": self.k}
            return json.dumps(unsat_json, indent=4)

        sat_json = {
            "result": self.result,
            "k": self.k,
            "model": {
                "size": len(self.pi),
                "states": [
                    {prop: str(value).lower() for prop, value in state}
                    for state in self.pi
                ],
            },
        }
        return json.dumps(sat_json, indent=4)
