from typing import Set, Iterable

import clingo  # type: ignore
from pysat.formula import IDPool  # type: ignore
from ltlf2asp.parser.constants import Constants
from ltlf2asp.parser.reify_interface import Reify


def clingo_symbol(name, args):
    return clingo.Function(name, [clingo.Number(x) for x in args])


def add_in_backend(b: clingo.Backend, symbol: clingo.Symbol):
    lit = b.add_atom(symbol)
    b.add_rule([lit], [])


class ReifyFormulaAsFacts(Reify[int, Set[clingo.Symbol]]):
    def __init__(self):
        self.pool = IDPool()
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

    def reify_variadic(self, fs: Iterable[int], name: str):
        id = self.pool.id((name, *fs))
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
        return self.reify_unary(f, Constants.WEAK_NEXT)

    def until(self, lhs, rhs) -> int:
        return self.reify_binary(lhs, rhs, Constants.UNTIL)

    def release(self, lhs, rhs) -> int:
        return self.reify_binary(lhs, rhs, Constants.RELEASE)

    def weak_until(self, lhs, rhs) -> int:
        return self.reify_binary(lhs, rhs, Constants.WEAK_UNTIL)

    def strong_release(self, lhs, rhs) -> int:
        return self.reify_binary(lhs, rhs, Constants.STRONG_RELEASE)

    def equivalence(self, lhs, rhs) -> int:
        return self.reify_binary(lhs, rhs, Constants.EQUALS)

    def implies(self, lhs, rhs) -> int:
        return self.reify_binary(lhs, rhs, Constants.IMPLIES)

    def eventually(self, f) -> int:
        return self.reify_unary(f, Constants.EVENTUALLY)

    def always(self, f) -> int:
        return self.reify_unary(f, Constants.ALWAYS)

    def negate(self, f) -> int:
        return self.reify_unary(f, Constants.NEGATE)

    def conjunction(self, fs) -> int:
        return self.reify_variadic(fs, Constants.CONJUNCTION)

    def disjunction(self, fs) -> int:
        return self.reify_variadic(fs, Constants.DISJUNCTION)

    def mark_as_root(self, f) -> None:
        self.facts.add(clingo_symbol(Constants.ROOT, [f]))