from lark import Lark, Transformer  # type: ignore
from pathlib import Path
from ltlf2asp.constants import Constants
from ltlf2asp.reify import ReifyFormula
from ltlf2asp.exceptions import ParsingError, UnsupportedOperator


class LTLfFlatTransformer(Transformer):
    def __init__(self):
        """Initialize."""
        super().__init__()
        self.reify = ReifyFormula()

    def start(self, args):
        self.reify.root(args[0])
        return self.reify.facts

    def ltlf_formula(self, args):
        return args[0]

    def ltlf_equivalence(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Release is not supported!")

            lhs, rhs = subformulas
            return self.reify.equivalence(lhs, rhs)

        raise ParsingError

    def ltlf_implication(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Implication is not supported!")
            lhs, rhs = subformulas
            return self.reify.implies(lhs, rhs)

        raise ParsingError

    def ltlf_or(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            return self.reify.disjunction(subformulas)

        raise ParsingError

    def ltlf_and(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            return self.reify.conjunction(subformulas)

        raise ParsingError

    def ltlf_until(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Until is not supported!")
            lhs, rhs = subformulas
            return self.reify.until(lhs, rhs)

        raise ParsingError

    def ltlf_weak_until(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic WeakUntil is not supported!")
            lhs, rhs = subformulas
            return self.reify.weak_until(lhs, rhs)

        raise ParsingError

    def ltlf_release(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Release is not supported!")
            lhs, rhs = subformulas
            return self.reify.release(lhs, rhs)

        raise ParsingError

    def ltlf_strong_release(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic StrongRelease is not supported!")
            lhs, rhs = subformulas
            return self.reify.strong_release(lhs, rhs)

        raise ParsingError

    def ltlf_always(self, args):
        if len(args) == 1:
            return args[0]

        return self.reify.always(args[1])

    def ltlf_eventually(self, args):
        if len(args) == 1:
            return args[0]

        return self.reify.eventually(args[1])

    def ltlf_next(self, args):
        if len(args) == 1:
            return args[0]

        return self.reify.next(args[1])

    def ltlf_weak_next(self, args):
        if len(args) == 1:
            return args[0]

        return self.reify.weak_next(args[1])

    def ltlf_not(self, args):
        if len(args) == 1:
            return args[0]

        return self.reify.negate(args[1])

    def ltlf_wrapped(self, args):
        if len(args) == 1:
            return args[0]
        return args[1]

    def symbol(self, args):
        string = "".join(x.value for x in args)
        return string.replace("'", '"')

    def ltlf_atom(self, args):
        if isinstance(args[0], int):
            return args[0]

        if isinstance(args[0], str):
            if args[0].lower() == Constants.TRUE:
                return self.ltlf_true(args)

            elif args[0].lower() == Constants.FALSE:
                return self.ltlf_false(args)

            elif args[0].lower() in (Constants.LAST, Constants.END):
                return self.ltlf_last(args)

            return self.reify.atomic_formula(args[0])

        raise ParsingError

    def ltlf_true(self, _args):
        return self.reify.true()

    def ltlf_false(self, _args):
        return self.reify.false()

    def ltlf_last(self, _args):
        return self.reify.last()


def parse_formula(formula_string: str, start_rule: str = "start"):
    GRAMMAR = Path(__file__).parent / "grammar.lark"
    parser = Lark(GRAMMAR.read_text(), parser="lalr", start=start_rule)
    transformer = LTLfFlatTransformer()
    tree = parser.parse(formula_string)
    return transformer.transform(tree)
