from typing import Optional, Sequence

from ltlf2asp.parser.reify_interface import Reify
from tests.test_parser import test_syntax as syntax
from tests.test_parser.test_syntax import Formula


class ReifyFormulaAsObject(Reify[syntax.Formula, Optional[syntax.Formula]]):
    def __init__(self) -> None:
        super().__init__()
        self.f: Optional[syntax.Formula] = None

    def result(self) -> Optional[syntax.Formula]:
        return self.f

    def true(self) -> syntax.Formula:
        return syntax.Truth()

    def false(self) -> syntax.Formula:
        return syntax.Faux()

    def last(self) -> syntax.Formula:
        return syntax.Last()

    def proposition(self, string: str) -> syntax.Formula:
        return syntax.Proposition(string)

    def next(self, f: syntax.Formula) -> syntax.Formula:
        return syntax.Next(f)

    def weak_next(self, f: syntax.Formula) -> syntax.Formula:
        return syntax.WeakNext(f)

    def until(self, lhs: syntax.Formula, rhs: syntax.Formula) -> syntax.Formula:
        return syntax.Until(lhs, rhs)

    def release(self, lhs: syntax.Formula, rhs: syntax.Formula) -> syntax.Formula:
        return syntax.Release(lhs, rhs)

    def weak_until(self, lhs: syntax.Formula, rhs: syntax.Formula) -> syntax.Formula:
        return syntax.WeakUntil(lhs, rhs)

    def strong_release(
        self, lhs: syntax.Formula, rhs: syntax.Formula
    ) -> syntax.Formula:
        return syntax.StrongRelease(lhs, rhs)

    def equivalence(self, lhs: syntax.Formula, rhs: syntax.Formula) -> syntax.Formula:
        return syntax.Equivalence(lhs, rhs)

    def implies(self, lhs: syntax.Formula, rhs: syntax.Formula) -> syntax.Formula:
        return syntax.Implication(lhs, rhs)

    def eventually(self, f: syntax.Formula) -> syntax.Formula:
        return syntax.Eventually(f)

    def always(self, f: syntax.Formula) -> syntax.Formula:
        return syntax.Always(f)

    def negate(self, f: syntax.Formula) -> syntax.Formula:
        return syntax.Negate(f)

    def conjunction(self, fs: Sequence[Formula]) -> syntax.Formula:
        return syntax.Conjunction(fs)

    def disjunction(self, fs: Sequence[Formula]) -> syntax.Formula:
        return syntax.Disjunction(fs)

    def mark_as_root(self, f: Formula) -> None:
        self.f = f
