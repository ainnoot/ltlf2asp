from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Sequence, List

import clingo


def integer_sequence():
    x = 1
    while True:
        yield x
        x += 1


__formula_id_sequence__ = integer_sequence()
__formula_ids__ = dict()


def tableaux_reify(f: "Formula"):
    facts = [clingo.Function("root", [f.id])]
    stack = [f]
    while len(stack) > 0:
        top = stack.pop()
        stack.extend(top.children())
        facts.extend(top.tableaux_reify())

    return facts


@dataclass(frozen=True)
class Formula(ABC):
    @abstractmethod
    def __code__(self):
        pass

    def __post_init__(self):
        h = self.__code__()
        if h not in __formula_ids__:
            i = next(__formula_id_sequence__)
            __formula_ids__[h] = i

    @property
    def id(self):
        return clingo.Number(__formula_ids__[self.__code__()])

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def symbol(self) -> str:
        pass

    @abstractmethod
    def children(self) -> List:
        pass

    @abstractmethod
    def negate(self):
        pass

    @abstractmethod
    def to_nnf(self):
        pass

    @abstractmethod
    def tableaux_reify(self):
        pass


@dataclass(frozen=True)
class Atomic(Formula, ABC):
    def __str__(self) -> str:
        return self.symbol()

    def children(self) -> List:
        return []

    def to_nnf(self):
        return self


@dataclass(frozen=True)
class Truth(Atomic):
    def __code__(self):
        return ("true",)

    @property
    def id(self):
        return clingo.Function("true")

    def symbol(self) -> str:
        return "#true"

    def negate(self):
        return Faux()

    def tableaux_reify(self):
        return []


@dataclass(frozen=True)
class Faux(Atomic):
    def __code__(self):
        return ("false",)

    @property
    def id(self):
        return clingo.Function("false")

    def symbol(self) -> str:
        return "#false"

    def negate(self):
        return Truth()

    def tableaux_reify(self):
        return []


@dataclass(frozen=True)
class Proposition(Atomic):
    value: str

    def __code__(self):
        return ("proposition", self.value)

    def symbol(self) -> str:
        return self.value

    def negate(self):
        return NegativeProposition(self.value)

    def tableaux_reify(self):
        return (clingo.Function("atomic", [self.id, clingo.Function(self.value)]),)


@dataclass(frozen=True)
class NegativeProposition(Atomic):
    value: str

    def __code__(self):
        return ("negative-proposition", self.value)

    def symbol(self) -> str:
        return "~" + self.value

    def negate(self):
        return Proposition(self.value)

    def tableaux_reify(self):
        return (
            clingo.Function(
                "atomic", [self.id, clingo.Function(self.value, positive=False)]
            ),
        )


@dataclass(frozen=True)
class Unary(Formula, ABC):
    f: Formula

    def dual(self):
        pass

    def __str__(self) -> str:
        return "({} {})".format(self.symbol(), self.f)

    def children(self) -> List:
        return [self.f]


@dataclass(frozen=True)
class Next(Unary):
    def __code__(self):
        return ("next", *self.f.__code__())

    def symbol(self) -> str:
        return "X"

    def negate(self):
        return WeakNext(self.f.negate())

    def to_nnf(self):
        return Next(self.f.to_nnf())

    def tableaux_reify(self):
        return (clingo.Function("next", [self.id, self.f.id]),)


@dataclass(frozen=True)
class WeakNext(Unary):
    def __code__(self):
        return ("weak-next", *self.f.__code__())

    def symbol(self) -> str:
        return "WX"

    def negate(self):
        return Next(self.f.negate())

    def to_nnf(self):
        return WeakNext(self.f.to_nnf())

    def tableaux_reify(self):
        return (clingo.Function("weak_next", [self.id, self.f.id]),)


@dataclass(frozen=True)
class Negate(Unary):
    def __code__(self):
        return ("negate", *self.f.__code__())

    def symbol(self) -> str:
        return "~"

    def negate(self):
        return self.f

    def to_nnf(self):
        if isinstance(self.f, Negate):
            return self.f.to_nnf()

        return self.f.negate().to_nnf()

    def tableaux_reify(self):
        # Negations are absorbed in NNF
        raise NotImplementedError


@dataclass(frozen=True)
class Binary(Formula, ABC):
    lhs: Formula
    rhs: Formula

    def __str__(self) -> str:
        return "({} {} {})".format(self.lhs, self.symbol(), self.rhs)

    def children(self) -> List:
        return [self.lhs, self.rhs]


@dataclass(frozen=True)
class Release(Binary):
    def __code__(self):
        return ("release", (self.lhs.__code__(), self.rhs.__code__()))

    def symbol(self) -> str:
        return "R"

    def negate(self):
        return Until(self.lhs.negate(), self.rhs.negate())

    def to_nnf(self):
        return Release(self.lhs.to_nnf(), self.rhs.to_nnf())

    def tableaux_reify(self):
        return (clingo.Function("release", [self.id, self.lhs.id, self.rhs.id]),)


@dataclass(frozen=True)
class Until(Binary):
    def __code__(self):
        return ("until", (self.lhs.__code__(), self.rhs.__code__()))

    def symbol(self) -> str:
        return "U"

    def negate(self):
        return Release(self.lhs.negate(), self.rhs.negate())

    def to_nnf(self):
        return Until(self.lhs.to_nnf(), self.rhs.to_nnf())

    def tableaux_reify(self):
        return (clingo.Function("until", [self.id, self.lhs.id, self.rhs.id]),)


@dataclass(frozen=True)
class Variadic(Formula, ABC):
    fs: Sequence[Formula]

    def __str__(self) -> str:
        return "({})".format((" " + self.symbol() + " ").join(str(x) for x in self.fs))

    def children(self) -> List:
        return list(self.fs)


@dataclass(frozen=True)
class Conjunction(Variadic):
    def __code__(self):
        return ("conjunction", *[f.__code__() for f in self.fs])

    def symbol(self) -> str:
        return "&"

    def negate(self):
        return Disjunction([f.negate() for f in self.fs])

    def to_nnf(self):
        return Conjunction([f.to_nnf() for f in self.fs])

    def tableaux_reify(self):
        return tuple([clingo.Function("conjunction", [self.id, f.id]) for f in self.fs])


@dataclass(frozen=True)
class Disjunction(Variadic):
    def __code__(self):
        return ("disjunction", *[f.__code__() for f in self.fs])

    def symbol(self) -> str:
        return "|"

    def negate(self):
        return Conjunction([f.negate() for f in self.fs])

    def to_nnf(self):
        return Disjunction([f.to_nnf() for f in self.fs])

    def tableaux_reify(self):
        return tuple([clingo.Function("disjunction", [self.id, f.id]) for f in self.fs])


class FormulaBuilder:
    @staticmethod
    def proposition(value: str):
        return Proposition(value)

    @staticmethod
    def negative_proposition(value: str):
        return NegativeProposition(value)

    @staticmethod
    def last():
        return WeakNext(Faux())

    @staticmethod
    def true():
        return Truth()

    @staticmethod
    def false():
        return Faux()

    @staticmethod
    def next(f: Formula):
        return Next(f)

    @staticmethod
    def always(f: Formula):
        # G(a)
        # ~F(~a)
        # ~(true U ~a)
        # false R a
        return Release(Faux(), f)

    @staticmethod
    def eventually(f: Formula):
        return Until(Truth(), f)

    @staticmethod
    def weak_next(f: Formula):
        return WeakNext(f)

    @staticmethod
    def negate(f: Formula):
        return Negate(f)

    @staticmethod
    def until(f: Formula, g: Formula):
        return Until(f, g)

    @staticmethod
    def release(f: Formula, g: Formula):
        return Release(f, g)

    @staticmethod
    def weak_until(f: Formula, g: Formula):
        # a W b
        # G(a) | (a U b)
        return Disjunction([FormulaBuilder.always(f), FormulaBuilder.until(f, g)])

    @staticmethod
    def strong_release(f: Formula, g: Formula):
        # ~(~a W ~b)
        # ~(G(~a) | (~a U ~b))
        # ~((false R ~a) | (~a U ~b))
        # true U a & (a R b))
        return Conjunction(
            [FormulaBuilder.until(Truth(), f), FormulaBuilder.release(f, g)]
        )

    @staticmethod
    def implication(f: Formula, g: Formula):
        # a -> b
        # ~a | b
        return Disjunction([Negate(f), g])

    @staticmethod
    def equivalence(f: Formula, g: Formula):
        return Conjunction(
            [FormulaBuilder.implication(f, g), FormulaBuilder.implication(g, f)]
        )

    @staticmethod
    def conjunction(fs: List[Formula]):
        return Conjunction(fs)

    @staticmethod
    def disjunction(fs: List[Formula]):
        return Disjunction(fs)
