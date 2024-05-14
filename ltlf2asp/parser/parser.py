from typing import TypeVar, Set, Type, Sequence

import clingo
import lark
from lark import Lark, Transformer
from pathlib import Path
from ltlf2asp.parser.constants import Constants
from ltlf2asp.parser.reify_as_atoms import ReifyFormulaAsFacts
from ltlf2asp.exceptions import ParsingError, UnsupportedOperator
from ltlf2asp.parser.reify_interface import Reify


T = TypeVar("T")
G = TypeVar("G")


class LTLfFlatTransformer(Transformer[T]):
    def __init__(self, reification_cls: Type[Reify[T, G]]) -> None:
        """Initiaflize."""
        super().__init__()
        self.reify: Reify[T, G] = reification_cls()

    def start(self, args: Sequence[T]) -> G:  # type: ignore
        self.reify.mark_as_root(args[0])
        return self.reify.result()

    def ltlf_formula(self, args: Sequence[T]) -> T:
        return args[0]

    def ltlf_equivalence(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Release is not supported!")

            lhs, rhs = subformulas
            return self.reify.equivalence(lhs, rhs)

        raise ParsingError

    def ltlf_implication(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Implication is not supported!")
            lhs, rhs = subformulas
            return self.reify.implies(lhs, rhs)

        raise ParsingError

    def ltlf_or(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            return self.reify.disjunction(subformulas)

        raise ParsingError

    def ltlf_and(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            return self.reify.conjunction(subformulas)

        raise ParsingError

    def ltlf_until(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Until is not supported!")
            lhs, rhs = subformulas
            return self.reify.until(lhs, rhs)

        raise ParsingError

    def ltlf_weak_until(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic WeakUntil is not supported!")
            lhs, rhs = subformulas
            return self.reify.weak_until(lhs, rhs)

        raise ParsingError

    def ltlf_release(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Release is not supported!")
            lhs, rhs = subformulas
            return self.reify.release(lhs, rhs)

        raise ParsingError

    def ltlf_strong_release(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic StrongRelease is not supported!")
            lhs, rhs = subformulas
            return self.reify.strong_release(lhs, rhs)

        raise ParsingError

    def ltlf_always(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        return self.reify.always(args[1])

    def ltlf_eventually(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        return self.reify.eventually(args[1])

    def ltlf_next(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        return self.reify.next(args[1])

    def ltlf_weak_next(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        return self.reify.weak_next(args[1])

    def ltlf_not(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]

        return self.reify.negate(args[1])

    def ltlf_wrapped(self, args: Sequence[T]) -> T:
        if len(args) == 1:
            return args[0]
        return args[1]

    def symbol(self, args: Sequence[lark.Token]) -> str:
        string = "".join(x.value for x in args)
        return string.replace("'", '"')

    def ltlf_atom(self, args: Sequence[str]) -> T:
        print("Got:", args, type(args[0]))
        if args[0].lower() == Constants.TRUE:
            return self.ltlf_true(args)

        elif args[0].lower() == Constants.FALSE:
            return self.ltlf_false(args)

        elif args[0].lower() in (Constants.LAST, Constants.END):
            return self.ltlf_last(args)

        else:
            return self.reify.proposition(args[0])

    def ltlf_true(self, _args: Sequence[str]) -> T:
        return self.reify.true()

    def ltlf_false(self, _args: Sequence[str]) -> T:
        return self.reify.false()

    def ltlf_last(self, _args: Sequence[str]) -> T:
        return self.reify.last()


def _parse_formula(formula_string: str, start_rule: str, reify: Type[Reify[T, G]]) -> G:
    GRAMMAR = Path(__file__).parent / "grammar.lark"
    parser = Lark(GRAMMAR.read_text(), parser="lalr", start=start_rule)
    transformer = LTLfFlatTransformer(reify)
    tree = parser.parse(formula_string)
    return transformer.transform(tree)  # type: ignore


def parse_formula(formula_string: str) -> Set[clingo.Symbol]:
    return _parse_formula(formula_string, "start", ReifyFormulaAsFacts)
