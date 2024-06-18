import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Sequence

from ltlf2asp.solve.solver_interface import Solver
from ltlf2asp.parser import parse_formula
from dataclasses import dataclass
from ltlf2asp.solve.check_model import check_trace
from ltlf2asp.solve.parse_trace import parse_trace


@dataclass(frozen=True)
class SolveArguments:
    formula: Path
    incremental: bool
    quiet: bool
    search_horizon: int

    def __post_init__(self) -> None:
        if not self.formula.is_file():
            raise RuntimeError("Formula does not exist.")

        if self.search_horizon <= 0:
            raise RuntimeError("Search horizon must be a positive integer.")


@dataclass(frozen=True)
class CheckArguments:
    formula: Path
    trace: Path

    def __post_init__(self) -> None:
        if not self.formula.is_file():
            raise RuntimeError("Formula file does not exist.")

        if not self.trace.is_file():
            raise RuntimeError("Trace file does not exist.")


def parse_check_args(argv: Sequence[str]) -> CheckArguments:
    p = ArgumentParser()
    p.add_argument("trace", type=Path)
    p.add_argument("formula", type=Path)

    args = p.parse_args(argv)
    return CheckArguments(**args.__dict__)


def parse_solve_args(argv: Sequence[str]) -> SolveArguments:
    p = ArgumentParser()
    p.add_argument("formula", type=Path)
    p.add_argument("search_horizon", type=int)
    p.add_argument("-i", "--incremental", action="store_true")
    p.add_argument("-q", "--quiet", action="store_true")

    args = p.parse_args(argv)

    return SolveArguments(**args.__dict__)


def solve(args: SolveArguments) -> int:
    formula = parse_formula(args.formula.read_text())
    solver = Solver(args.incremental, args.search_horizon)
    result = solver.solve(formula)

    if args.quiet:
        print(result)
        return 0

    print(result.json())
    return 0


def check(args: CheckArguments) -> int:
    formula = parse_formula(args.formula.read_text())
    trace = parse_trace(args.trace.read_text())

    ans = check_trace(trace, formula)
    print(ans)
    return 0


def run() -> int:
    argv = sys.argv[1:]
    if len(argv) <= 2:
        print("Usage:")
        print("* ltlf2asp solve [-i --incremental] [formula: Path] [horizon: int]")
        print("* ltlf2asp check [trace: Path] [formula: Path]")
        sys.exit(1)

    # TODO: Make a parameter, or fix the grammar...
    sys.setrecursionlimit(2056)
    command, args = argv[0], argv[1:]
    match command:
        case "check":
            return check(parse_check_args(args))
        case "solve":
            return solve(parse_solve_args(args))

    raise RuntimeError("Unknown command!")
