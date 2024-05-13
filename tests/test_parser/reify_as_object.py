from typing import Optional

from ltlf2asp.parser.reify_interface import Reify
import ltlf2asp.parser.syntax as Syntax


class ReifyFormulaAsObject(Reify[Syntax.Formula, Optional[Syntax.Formula]]):
    def __init__(self) -> None:
        self.f: Optional[Syntax.Formula] = None

    def result(self) -> Optional[Syntax.Formula]:
        return self.f

    def true(self) -> Syntax.Formula:
        return Syntax.Truth()

    def false(self) -> Syntax.Formula:
        return Syntax.Faux()

    def last(self) -> Syntax.Formula:
        return Syntax.Last()

    def proposition(self, string: str) -> Syntax.Formula:
        return Syntax.Proposition(string)

    def next(self, f) -> Syntax.Formula:
        return Syntax.Next(f)

    def weak_next(self, f) -> Syntax.Formula:
        return Syntax.WeakNext(f)

    def until(self, lhs, rhs) -> Syntax.Formula:
        return Syntax.Until(lhs, rhs)

    def release(self, lhs, rhs) -> Syntax.Formula:
        return Syntax.Release(lhs, rhs)

    def weak_until(self, lhs, rhs) -> Syntax.Formula:
        return Syntax.WeakUntil(lhs, rhs)

    def strong_release(self, lhs, rhs) -> Syntax.Formula:
        return Syntax.StrongRelease(lhs, rhs)

    def equivalence(self, lhs, rhs) -> Syntax.Formula:
        return Syntax.Equivalence(lhs, rhs)

    def implies(self, lhs, rhs) -> Syntax.Formula:
        return Syntax.Implication(lhs, rhs)

    def eventually(self, f) -> Syntax.Formula:
        return Syntax.Eventually(f)

    def always(self, f) -> Syntax.Formula:
        return Syntax.Always(f)

    def negate(self, f) -> Syntax.Formula:
        return Syntax.Negate(f)

    def conjunction(self, fs) -> Syntax.Formula:
        return Syntax.Conjunction(fs)

    def disjunction(self, fs) -> Syntax.Formula:
        return Syntax.Disjunction(fs)

    def mark_as_root(self, f) -> None:
        self.f = f
