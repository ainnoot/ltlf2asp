from abc import ABC, abstractmethod

from typing import TypeVar, Generic, Sequence

T = TypeVar("T")
G = TypeVar("G")


class Reify(Generic[T, G], ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def result(self) -> G:
        pass

    @abstractmethod
    def true(self) -> T:
        pass

    @abstractmethod
    def false(self) -> T:
        pass

    @abstractmethod
    def last(self) -> T:
        pass

    @abstractmethod
    def proposition(self, string: str) -> T:
        pass

    @abstractmethod
    def next(self, f: T) -> T:
        pass

    @abstractmethod
    def weak_next(self, f: T) -> T:
        pass

    @abstractmethod
    def until(self, lhs: T, rhs: T) -> T:
        pass

    @abstractmethod
    def release(self, lhs: T, rhs: T) -> T:
        pass

    @abstractmethod
    def weak_until(self, lhs: T, rhs: T) -> T:
        pass

    @abstractmethod
    def strong_release(self, lhs: T, rhs: T) -> T:
        pass

    @abstractmethod
    def equivalence(self, lhs: T, rhs: T) -> T:
        pass

    @abstractmethod
    def implies(self, lhs: T, rhs: T) -> T:
        pass

    @abstractmethod
    def eventually(self, f: T) -> T:
        pass

    @abstractmethod
    def always(self, f: T) -> T:
        pass

    @abstractmethod
    def negate(self, f: T) -> T:
        pass

    @abstractmethod
    def conjunction(self, fs: Sequence[T]) -> T:
        pass

    @abstractmethod
    def disjunction(self, fs: Sequence[T]) -> T:
        pass

    @abstractmethod
    def mark_as_root(self, f: T) -> None:
        pass
