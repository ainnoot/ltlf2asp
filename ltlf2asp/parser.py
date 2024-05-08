from lark import Lark, Transformer  # type: ignore
from pathlib import Path
import clingo  # type: ignore
from pysat.formula import IDPool  # type: ignore
from ltlf2asp.constants import Constants


class ParsingError(Exception):
    pass


class UnsupportedOperator(Exception):
    def __init__(self, string):
        self.string = string

    def message(self):
        return self.string


class LTLfFlatTransformer(Transformer):
    def __init__(self):
        """Initialize."""
        super().__init__()
        self.pool = IDPool()
        self.reification = set()

    def start(self, args):
        self.reification.add(clingo.Function(Constants.ROOT, [clingo.Number(args[0])]))
        return self.reification

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
            id = self.pool.id((Constants.EQUALS, lhs, rhs))
            self.reification.add(
                clingo.Function(
                    Constants.EQUALS,
                    [clingo.Number(id), clingo.Number(lhs), clingo.Number(rhs)],
                )
            )
            return id

        raise ParsingError

    def ltlf_implication(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Implication is not supported!")
            lhs, rhs = subformulas
            id = self.pool.id((Constants.IMPLIES, lhs, rhs))
            self.reification.add(
                clingo.Function(
                    Constants.IMPLIES,
                    [clingo.Number(id), clingo.Number(lhs), clingo.Number(rhs)],
                )
            )
            return id

        raise ParsingError

    def ltlf_or(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            id = self.pool.id((Constants.DISJUNCTION, *subformulas))
            for x in subformulas:
                self.reification.add(
                    clingo.Function(
                        Constants.DISJUNCTION, [clingo.Number(id), clingo.Number(x)]
                    )
                )
            return id

        raise ParsingError

    def ltlf_and(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            id = self.pool.id((Constants.CONJUNCTION, *subformulas))
            for x in subformulas:
                self.reification.add(
                    clingo.Function(
                        Constants.CONJUNCTION, [clingo.Number(id), clingo.Number(x)]
                    )
                )
            return id

        raise ParsingError

    def ltlf_until(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Until is not supported!")
            lhs, rhs = subformulas
            id = self.pool.id((Constants.UNTIL, lhs, rhs))
            self.reification.add(
                clingo.Function(
                    Constants.UNTIL,
                    [clingo.Number(id), clingo.Number(lhs), clingo.Number(rhs)],
                )
            )
            return id

        raise ParsingError

    def ltlf_weak_until(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic WeakUntil is not supported!")
            lhs, rhs = subformulas
            id = self.pool.id((Constants.WEAK_UNTIL, lhs, rhs))
            self.reification.add(
                clingo.Function(
                    Constants.WEAK_UNTIL,
                    [clingo.Number(id), clingo.Number(lhs), clingo.Number(rhs)],
                )
            )
            return id

        raise ParsingError

    def ltlf_release(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic Release is not supported!")
            lhs, rhs = subformulas
            id = self.pool.id((Constants.RELEASE, lhs, rhs))
            self.reification.add(
                clingo.Function(
                    Constants.RELEASE,
                    [clingo.Number(id), clingo.Number(lhs), clingo.Number(rhs)],
                )
            )
            return id

        raise ParsingError

    def ltlf_strong_release(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            if len(subformulas) != 2:
                raise UnsupportedOperator("Variadic StrongRelease is not supported!")
            lhs, rhs = subformulas
            id = self.pool.id((Constants.RELEASE, lhs, rhs))
            self.reification.add(
                clingo.Function(
                    Constants.STRONG_RELEASE,
                    [clingo.Number(id), clingo.Number(lhs), clingo.Number(rhs)],
                )
            )
            return id

        raise ParsingError

    def ltlf_always(self, args):
        if len(args) == 1:
            return args[0]

        id = self.pool.id((Constants.ALWAYS, args[1]))
        self.reification.add(
            clingo.Function(
                Constants.ALWAYS, [clingo.Number(id), clingo.Number(args[1])]
            )
        )
        return id

    def ltlf_eventually(self, args):
        if len(args) == 1:
            return args[0]

        id = self.pool.id((Constants.EVENTUALLY, args[1]))
        self.reification.add(
            clingo.Function(
                Constants.EVENTUALLY, [clingo.Number(id), clingo.Number(args[1])]
            )
        )
        return id

    def ltlf_next(self, args):
        if len(args) == 1:
            return args[0]

        id = self.pool.id((Constants.NEXT, args[1]))
        self.reification.add(
            clingo.Function(Constants.NEXT, [clingo.Number(id), clingo.Number(args[1])])
        )
        return id

    def ltlf_weak_next(self, args):
        if len(args) == 1:
            return args[0]

        id = self.pool.id((Constants.WEAK_NEXT, args[1]))
        self.reification.add(
            clingo.Function(
                Constants.WEAK_NEXT, [clingo.Number(id), clingo.Number(args[1])]
            )
        )
        return id

    def ltlf_not(self, args):
        if len(args) == 1:
            return args[0]

        id = self.pool.id((Constants.NEGATE, args[1]))
        self.reification.add(
            clingo.Function(
                Constants.NEGATE, [clingo.Number(id), clingo.Number(args[1])]
            )
        )
        return id

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

            if args[0].lower() == Constants.FALSE:
                return self.ltlf_false(args)

            if args[0].lower() in (Constants.LAST, Constants.END):
                return self.ltlf_last(args)

            id = self.pool.id((Constants.ATOMIC, args[0]))
            self.reification.add(
                clingo.Function(
                    Constants.ATOMIC, [clingo.Number(id), clingo.String(args[0])]
                )
            )
            return id

        raise ParsingError

    def ltlf_true(self, _args):
        id = self.pool.id(Constants.TRUE)
        self.reification.add(clingo.Function(Constants.TRUE, [clingo.Number(id)]))
        return id

    def ltlf_false(self, _args):
        id = self.pool.id(Constants.FALSE)
        self.reification.add(clingo.Function(Constants.FALSE, [clingo.Number(id)]))
        return id

    def ltlf_last(self, _args):
        id = self.pool.id(Constants.LAST)
        self.reification.add(clingo.Function(Constants.LAST, [clingo.Number(id)]))
        return id


def parse_formula(formula_string: str, start_rule: str = "start"):
    GRAMMAR = Path(__file__).parent / "grammar.lark"
    parser = Lark(GRAMMAR.read_text(), parser="lalr", start=start_rule)
    transformer = LTLfFlatTransformer()
    tree = parser.parse(formula_string)
    return transformer.transform(tree)


if __name__ == "__main__":
    while True:
        GRAMMAR = Path(__file__).parent / "grammar.lark"
        parser = Lark(GRAMMAR.read_text(), parser="lalr", start="start")
        formula_string = input("> ")
        tree = parser.parse(formula_string)
        trans = LTLfFlatTransformer()
        atoms = trans.transform(tree)
        print([str(x) for x in atoms])
