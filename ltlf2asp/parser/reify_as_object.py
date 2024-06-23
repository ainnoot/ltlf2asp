from typing import Optional, Sequence

from ltlf2asp.parser.reify_interface import Reify
from ltlf2asp.parser import syntax
from ltlf2asp.parser.syntax import Formula, FormulaBuilder


class ReifyFormulaAsObject(Reify[syntax.Formula, Optional[syntax.Formula]]):
    def __init__(self) -> None:
        super().__init__()
        self.f: Optional[syntax.Formula] = None

    def result(self) -> Optional[syntax.Formula]:
        return self.f.to_nnf()

    def true(self) -> syntax.Formula:
        return FormulaBuilder.true()

    def false(self) -> syntax.Formula:
        return FormulaBuilder.false()

    def last(self) -> syntax.Formula:
        return FormulaBuilder.last()

    def proposition(self, string: str) -> syntax.Formula:
        return FormulaBuilder.proposition(string)

    def next(self, f: syntax.Formula) -> syntax.Formula:
        return FormulaBuilder.next(f)

    def weak_next(self, f: syntax.Formula) -> syntax.Formula:
        return FormulaBuilder.weak_next(f)

    def until(self, lhs: syntax.Formula, rhs: syntax.Formula) -> syntax.Formula:
        return FormulaBuilder.until(lhs, rhs)

    def release(self, lhs: syntax.Formula, rhs: syntax.Formula) -> syntax.Formula:
        return FormulaBuilder.release(lhs, rhs)

    def weak_until(self, lhs: syntax.Formula, rhs: syntax.Formula) -> syntax.Formula:
        return FormulaBuilder.weak_until(lhs, rhs)

    def strong_release(
        self, lhs: syntax.Formula, rhs: syntax.Formula
    ) -> syntax.Formula:
        return FormulaBuilder.strong_release(lhs, rhs)

    def equivalence(self, lhs: syntax.Formula, rhs: syntax.Formula) -> syntax.Formula:
        return FormulaBuilder.equivalence(lhs, rhs)

    def implies(self, lhs: syntax.Formula, rhs: syntax.Formula) -> syntax.Formula:
        return FormulaBuilder.implication(lhs, rhs)

    def eventually(self, f: syntax.Formula) -> syntax.Formula:
        return FormulaBuilder.eventually(f)

    def always(self, f: syntax.Formula) -> syntax.Formula:
        return FormulaBuilder.always(f)

    def negate(self, f: syntax.Formula) -> syntax.Formula:
        return FormulaBuilder.negate(f)

    def conjunction(self, fs: Sequence[Formula]) -> syntax.Formula:
        return syntax.Conjunction(fs)

    def disjunction(self, fs: Sequence[Formula]) -> syntax.Formula:
        return syntax.Disjunction(fs)

    def mark_as_root(self, f: Formula) -> None:
        self.f = f
