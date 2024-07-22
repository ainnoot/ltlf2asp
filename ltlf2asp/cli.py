import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Sequence

from ltlf2asp.solve.solver_interface import Solver
from ltlf2asp.parser import parse_formula, parse_formula_object, tableaux_reify
from dataclasses import dataclass
from ltlf2asp.solve.check_model import check_trace
from ltlf2asp.solve.parse_trace import parse_trace
from ltlf2asp.solve.tableaux import Reynolds
from ltlf2asp.solve.hybrid_solve import solve as hybrid_solve


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
class HybridArguments:
    formula: Path
    search_horizon: int

    def __post_init__(self) -> None:
        if not self.formula.is_file():
            raise RuntimeError("Formula does not exist.")

        if self.search_horizon <= 0:
            raise RuntimeError("Search horizon must be a positive integer.")


@dataclass(frozen=True)
class TableauxArguments:
    formula: Path
    depth: int
    verbose: bool

    def __post_init__(self) -> None:
        if not self.formula.is_file():
            raise RuntimeError("Formula does not exist.")

        if self.depth <= 0:
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


@dataclass(frozen=True)
class ParseArgs:
    formula: Path
    method: str

    def __post_init__(self) -> None:
        if not self.formula.is_file():
            raise RuntimeError("Formula file does not exist.")

        if self.method not in ["dag", "tableaux"]:
            raise RuntimeError("Unknown representation method: {}".format(self.method))


def parse_check_args(argv: Sequence[str]) -> CheckArguments:
    p = ArgumentParser()
    p.add_argument("trace", type=Path)
    p.add_argument("formula", type=Path)

    args = p.parse_args(argv)
    return CheckArguments(**args.__dict__)


def parse_tableaux_args(argv: Sequence[str]) -> TableauxArguments:
    p = ArgumentParser()
    p.add_argument("formula", type=Path)
    p.add_argument("depth", type=int)
    p.add_argument("--verbose", "-v", action="store_true")

    args = p.parse_args(argv)
    return TableauxArguments(**args.__dict__)


def parse_solve_args(argv: Sequence[str]) -> SolveArguments:
    p = ArgumentParser()
    p.add_argument("formula", type=Path)
    p.add_argument("search_horizon", type=int)
    p.add_argument("-i", "--incremental", action="store_true")
    p.add_argument("-q", "--quiet", action="store_true")

    args = p.parse_args(argv)

    return SolveArguments(**args.__dict__)


def parse_hybrid_args(argv: Sequence[str]) -> HybridArguments:
    p = ArgumentParser()
    p.add_argument("formula", type=Path)
    p.add_argument("search_horizon", type=int)

    args = p.parse_args(argv)

    return HybridArguments(**args.__dict__)


def parse_parse_args(argv: Sequence[str]) -> ParseArgs:
    p = ArgumentParser()
    p.add_argument("formula", type=Path)
    p.add_argument("-m", "--method", choices=["dag", "tableaux"], default="dag")

    args = p.parse_args(argv)

    return ParseArgs(**args.__dict__)


def tableaux(args: TableauxArguments):
    formula = parse_formula_object(args.formula.read_text())
    tableaux = Reynolds(args.verbose)
    facts = tableaux_reify(formula.to_nnf())
    result = tableaux.solve(facts, args.depth)

    print(result.json())
    return 0


def solve(args: SolveArguments) -> int:
    formula = parse_formula(args.formula.read_text())
    solver = Solver(args.incremental, args.search_horizon)
    result = solver.solve(formula)

    if args.quiet:
        print(result)
        return 0

    print(result.json())
    return 0


def hybrid(args: HybridArguments) -> int:
    # TODO: Fix this!
    formula_tableaux = parse_formula_object(args.formula.read_text()).to_nnf()
    formula_ltl2sat = parse_formula(args.formula.read_text())
    ans = hybrid_solve(
        formula_ltl2sat, tableaux_reify(formula_tableaux), args.search_horizon
    )

    print(ans.json())
    return 0


def parse(args: ParseArgs) -> int:
    # TODO: Fix this!
    if args.method == "tableaux":
        formula_tableaux = parse_formula_object(args.formula.read_text())
        for fact in tableaux_reify(formula_tableaux):
            print(str(fact) + ".")

    elif args.method == "dag":
        formula_ltl2sat = parse_formula(args.formula.read_text())
        for fact in formula_ltl2sat:
            print(str(fact) + ".")

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
        print("* ltlf2asp reynolds [formula: Path] [depth: int]")
        print("* ltlf2asp hybrid [formula: Path] [depth: int]")
        print("* ltlf2asp parse [formula: Path] [-m DAG|TABLEAUX]")
        sys.exit(1)

    # TODO: Make a parameter, or fix the grammar...
    sys.setrecursionlimit(2056)
    command, args = argv[0], argv[1:]
    match command:
        case "check":
            return check(parse_check_args(args))
        case "solve":
            return solve(parse_solve_args(args))
        case "reynolds":
            return tableaux(parse_tableaux_args(args))
        case "hybrid":
            return hybrid(parse_hybrid_args(args))
        case "parse":
            return parse(parse_parse_args(args))

    raise RuntimeError("Unknown command!")
