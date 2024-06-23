from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Sequence


@dataclass(frozen=True)
class Formula(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def symbol(self) -> str:
        pass


@dataclass(frozen=True)
class Atomic(Formula, ABC):
    def __str__(self) -> str:
        return self.symbol()


@dataclass(frozen=True)
class Truth(Atomic):
    def symbol(self) -> str:
        return "t"


@dataclass(frozen=True)
class Faux(Atomic):
    def symbol(self) -> str:
        return "f"


@dataclass(frozen=True)
class Last(Atomic):
    def symbol(self) -> str:
        return "@"


@dataclass(frozen=True)
class Proposition(Atomic):
    value: str

    def symbol(self) -> str:
        return self.value


@dataclass(frozen=True)
class Unary(Formula, ABC):
    f: Formula

    def __str__(self) -> str:
        return "({} {})".format(self.symbol(), self.f)


@dataclass(frozen=True)
class Next(Unary):
    def symbol(self) -> str:
        return "X"


@dataclass(frozen=True)
class WeakNext(Unary):
    def symbol(self) -> str:
        return "WX"


@dataclass(frozen=True)
class Negate(Unary):
    def symbol(self) -> str:
        return "~"


@dataclass(frozen=True)
class Eventually(Unary):
    def symbol(self) -> str:
        return "F"


@dataclass(frozen=True)
class Always(Unary):
    def symbol(self) -> str:
        return "G"


@dataclass(frozen=True)
class Binary(Formula, ABC):
    lhs: Formula
    rhs: Formula

    def __str__(self) -> str:
        return "({} {} {})".format(self.lhs, self.symbol(), self.rhs)


@dataclass(frozen=True)
class Release(Binary):
    def symbol(self) -> str:
        return "R"


@dataclass(frozen=True)
class Until(Binary):
    def symbol(self) -> str:
        return "U"


@dataclass(frozen=True)
class WeakUntil(Binary):
    def symbol(self) -> str:
        return "W"


@dataclass(frozen=True)
class StrongRelease(Binary):
    def symbol(self) -> str:
        return "M"


@dataclass(frozen=True)
class Implication(Binary):
    def symbol(self) -> str:
        return "->"


@dataclass(frozen=True)
class Equivalence(Binary):
    def symbol(self) -> str:
        return "="


@dataclass(frozen=True)
class Variadic(Formula, ABC):
    fs: Sequence[Formula]

    def __str__(self) -> str:
        return "({})".format((" " + self.symbol() + " ").join(str(x) for x in self.fs))


@dataclass(frozen=True)
class Conjunction(Variadic):
    def symbol(self) -> str:
        return "&"


@dataclass(frozen=True)
class Disjunction(Variadic):
    def symbol(self) -> str:
        return "|"
