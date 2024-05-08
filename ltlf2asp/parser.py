from lark import Lark, Transformer
from pathlib import Path
import clingo  # type: ignore
from pysat.formula import IDPool  # type: ignore
from enum import IntEnum


class ParsingError(Exception):
    pass


class OperatorId(IntEnum):
    ATOMIC = 0
    NEXT = 1
    WEAK_NEXT = 2
    EVENTUALLY = 3
    ALWAYS = 4
    NEGATE = 5
    IMPLIES = 6
    CONJUNCTION = 7
    DISJUNCTION = 8
    EQUALS = 9
    UNTIL = 10
    RELEASE = 11


class LTLfFlatTransformer(Transformer):
    def __init__(self):
        """Initialize."""
        super().__init__()
        self.pool = IDPool()
        self.reification = set()

    def start(self, args):
        self.reification.add(clingo.Function("root", [clingo.Number(args[0])]))
        return self.reification

    def ltlf_formula(self, args):
        return args[0]

    def ltlf_equivalence(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            assert len(subformulas) == 2, "Variadic Release not supported!"
            lhs, rhs = subformulas
            id = self.pool.id((OperatorId.EQUALS, lhs, rhs))
            self.reification.add(
                clingo.Function(
                    "equivalent",
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
            assert len(subformulas) == 2, "Variadic Implies not supported!"
            lhs, rhs = subformulas
            id = self.pool.id((OperatorId.IMPLIES, lhs, rhs))
            self.reification.add(
                clingo.Function(
                    "implies",
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
            id = self.pool.id((OperatorId.DISJUNCTION, *subformulas))
            for x in subformulas:
                self.reification.add(
                    clingo.Function(
                        "disjunction", [clingo.Number(id), clingo.Number(x)]
                    )
                )
            return id

        raise ParsingError

    def ltlf_and(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            id = self.pool.id((OperatorId.CONJUNCTION, *subformulas))
            for x in subformulas:
                self.reification.add(
                    clingo.Function(
                        "conjunction", [clingo.Number(id), clingo.Number(x)]
                    )
                )
            return id

        raise ParsingError

    def ltlf_until(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            assert len(subformulas) == 2, "Variadic Release not supported!"
            lhs, rhs = subformulas
            id = self.pool.id((OperatorId.UNTIL, lhs, rhs))
            self.reification.add(
                clingo.Function(
                    "until", [clingo.Number(id), clingo.Number(lhs), clingo.Number(rhs)]
                )
            )
            return id

        raise ParsingError

    def ltlf_release(self, args):
        if len(args) == 1:
            return args[0]

        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            assert len(subformulas) == 2, "Variadic Release not supported!"
            lhs, rhs = subformulas
            id = self.pool.id((OperatorId.RELEASE, lhs, rhs))
            self.reification.add(
                clingo.Function(
                    "release",
                    [clingo.Number(id), clingo.Number(lhs), clingo.Number(rhs)],
                )
            )
            return id

        raise ParsingError

    def ltlf_always(self, args):
        if len(args) == 1:
            return args[0]

        id = self.pool.id((OperatorId.ALWAYS, args[1]))
        self.reification.add(
            clingo.Function("always", [clingo.Number(id), clingo.Number(args[1])])
        )
        return id

    def ltlf_eventually(self, args):
        if len(args) == 1:
            return args[0]

        id = self.pool.id((OperatorId.EVENTUALLY, args[1]))
        self.reification.add(
            clingo.Function("eventually", [clingo.Number(id), clingo.Number(args[1])])
        )
        return id

    def ltlf_next(self, args):
        if len(args) == 1:
            return args[0]

        id = self.pool.id((OperatorId.NEXT, args[1]))
        self.reification.add(
            clingo.Function("next", [clingo.Number(id), clingo.Number(args[1])])
        )
        return id

    def ltlf_weak_next(self, args):
        if len(args) == 1:
            return args[0]

        id = self.pool.id((OperatorId.WEAK_NEXT, args[1]))
        self.reification.add(
            clingo.Function("weak_next", [clingo.Number(id), clingo.Number(args[1])])
        )
        return id

    def ltlf_not(self, args):
        if len(args) == 1:
            return args[0]

        id = self.pool.id((OperatorId.NEGATE, args[1]))
        self.reification.add(
            clingo.Function("negate", [clingo.Number(id), clingo.Number(args[1])])
        )
        return id

    def ltlf_wrapped(self, args):
        if len(args) == 1:
            return args[0]
        return args[1]

    def ltlf_atom(self, args):
        if isinstance(args[0], int):
            return args[0]

        elif type(args[0]) == clingo.Symbol:
            id = self.pool.id((OperatorId.ATOMIC, args[0]))
            self.reification.add(
                clingo.Function("atomic", [clingo.Number(id), args[0]])
            )
            return id

        raise ParsingError

    def ltlf_true(self, _args):
        id = self.pool.id((OperatorId.ATOMIC, "true"))
        self.reification.add(clingo.Function("true", [clingo.Number(id)]))
        return id

    def ltlf_false(self, _args):
        id = self.pool.id((OperatorId.ATOMIC, "false"))
        self.reification.add(clingo.Function("false", [clingo.Number(id)]))
        return id

    def ltlf_last(self, _args):
        id = self.pool.id((OperatorId.ATOMIC, "last"))
        self.reification.add(clingo.Function("last", [clingo.Number(id)]))
        return id

    def quoted_symbol(self, args):
        print("Got quoted symbols:", args)
        return clingo.Function("quote", [clingo.String(args[0].value)])

    def clingo_symbol(self, args):
        if len(args) == 1:
            # TODO: Fix the grammar...
            if args[0].value in (
                "Last",
                "last",
                "True",
                "true",
                "False",
                "false",
                "TRUE",
                "FALSE",
                "LAST",
                "end",
                "END",
                "End",
            ):
                return self.uppercase_symbol(args)

            atom = clingo.Function(args[0].value)
            return atom

        atom = clingo.Function(
            args[0].value, [x for x in args[1:-1] if isinstance(x, clingo.Symbol)]
        )
        return atom

    def uppercase_symbol(self, args):
        if args[0].value in ("True", "true", "TRUE"):
            return self.ltlf_true(args)
        elif args[0].value in ("False", "false", "FALSE"):
            return self.ltlf_false(args)
        elif args[0].value in ("Last", "last", "End", "end", "LAST", "END"):
            return self.ltlf_last(args)

        return clingo.Function("uppercase_symbol", [clingo.String(args[0].value)])

    def clingo_term(self, args):
        return args[0]

    def integer(self, args):
        return clingo.Number(int(args[0].value))

    def string(self, args):
        return clingo.String(args[0].value)


def parse_formula(formula_string: str, start_rule: str = "start"):
    GRAMMAR = Path(__file__).parent / "grammar.lark"
    parser = Lark(GRAMMAR.read_text(), parser="lalr", start=start_rule)
    transformer = LTLfFlatTransformer()
    tree = parser.parse(formula_string)
    return transformer.transform(tree)
