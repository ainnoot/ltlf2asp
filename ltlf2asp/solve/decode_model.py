from typing import Dict, Tuple, Generator

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


@dataclass(frozen=True)
class Model:
    pi: Tuple[State, ...]

    def state(self, i: int) -> State:
        return self.pi[i]

    def __iter__(self) -> Generator[State, None, None]:
        yield from self.pi

    def __len__(self) -> int:
        return len(self.pi)

    @staticmethod
    def from_clingo_model(model: clingo.Model) -> "Model":
        trace_dict: Dict[int, Dict[str, bool]] = defaultdict(dict)
        for x in model.context.symbolic_atoms.by_signature("trace", 2):
            symbol = x.symbol
            t = symbol.arguments[0].number
            a = symbol.arguments[1].string
            trace_dict[t][a] = model.contains(symbol)

        return Model(tuple(State(trace_dict[i]) for i in range(len(trace_dict))))
