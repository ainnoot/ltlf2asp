from collections import defaultdict
from typing import Set, Dict, Tuple

import clingo  # type: ignore
from ltlf2asp.parser.constants import Constants
from ltlf2asp.parser.reify_interface import Reify


def clingo_symbol(name, args):
    return clingo.Function(name, [clingo.Number(x) for x in args])


def add_in_backend(b: clingo.Backend, symbol: clingo.Symbol):
    lit = b.add_atom(symbol)
    b.add_rule([lit], [])


class IDPool:
    def __init__(self) -> None:
        self.objects: Dict[object, int] = defaultdict(lambda: self._next_id())
        self.i_: int = 1

    def _next_id(self) -> int:
        i = self.i_
        self.i_ += 1
        return i

    def id(self, obj: object) -> int:
        return self.objects[obj]


class ReifyFormulaAsFacts(Reify[int, Set[clingo.Symbol]]):
    def __init__(self) -> None:
        self.pool: IDPool = IDPool()
        self.facts: Set[clingo.Symbol] = set()

    def result(self) -> Set[clingo.Symbol]:
        return self.facts

    def constant(self, name: str):
        id = self.pool.id((name,))
        self.facts.add(clingo_symbol(name, [id]))
        return id

    def reify_unary(self, f: int, name: str):
        id = self.pool.id((name, f))
        self.facts.add(clingo_symbol(name, [id, f]))
        return id

    def reify_binary(self, lhs: int, rhs: int, name: str):
        id = self.pool.id((name, lhs, rhs))
        self.facts.add(clingo_symbol(name, [id, lhs, rhs]))
        return id

    def reify_variadic(self, fs: Tuple[int, ...], name: str):
        id = self.pool.id((name, *sorted(fs)))
        for f in fs:
            self.facts.add(clingo_symbol(name, [id, f]))
        return id

    def true(self) -> int:
        return self.constant(Constants.TRUE)

    def false(self) -> int:
        return self.constant(Constants.FALSE)

    def last(self) -> int:
        return self.constant(Constants.LAST)

    def proposition(self, string: str) -> int:
        id = self.pool.id((Constants.ATOMIC, string))
        self.facts.add(
            clingo.Function(
                Constants.ATOMIC, [clingo.Number(id), clingo.String(string)]
            )
        )
        return id

    def next(self, f: int) -> int:
        return self.reify_unary(f, Constants.NEXT)

    def weak_next(self, f) -> int:
        # return self.reify_unary(f, Constants.WEAK_NEXT)
        return self.disjunction((self.last(), self.next(f)))

    def until(self, lhs, rhs) -> int:
        return self.reify_binary(lhs, rhs, Constants.UNTIL)

    def release(self, lhs, rhs) -> int:
        return self.reify_binary(lhs, rhs, Constants.RELEASE)

    def weak_until(self, lhs, rhs) -> int:
        # return self.reify_binary(lhs, rhs, Constants.WEAK_UNTIL)
        return self.disjunction((self.until(lhs, rhs), self.always(lhs)))

    def strong_release(self, lhs, rhs) -> int:
        # return self.reify_binary(lhs, rhs, Constants.STRONG_RELEASE)
        return self.conjunction((self.release(lhs, rhs), self.eventually(lhs)))

    def equivalence(self, lhs, rhs) -> int:
        # return self.reify_binary(lhs, rhs, Constants.EQUALS)
        return self.conjunction((self.implies(lhs, rhs), self.implies(rhs, lhs)))

    def implies(self, lhs, rhs) -> int:
        # return self.reify_binary(lhs, rhs, Constants.IMPLIES)
        return self.disjunction((self.negate(lhs), rhs))

    def eventually(self, f) -> int:
        # return self.reify_unary(f, Constants.EVENTUALLY)
        return self.until(self.true(), f)

    def always(self, f) -> int:
        # return self.reify_unary(f, Constants.ALWAYS)
        return self.release(self.false(), f)

    def negate(self, f) -> int:
        return self.reify_unary(f, Constants.NEGATE)

    def conjunction(self, fs: Tuple[int, ...]) -> int:
        return self.reify_variadic(fs, Constants.CONJUNCTION)

    def disjunction(self, fs: Tuple[int, ...]) -> int:
        return self.reify_variadic(fs, Constants.DISJUNCTION)

    def mark_as_root(self, f) -> None:
        self.facts.add(clingo_symbol(Constants.ROOT, [f]))
