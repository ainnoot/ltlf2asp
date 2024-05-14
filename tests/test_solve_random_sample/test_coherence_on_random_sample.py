from pathlib import Path
from ltlf2asp.parser import parse_formula
from ltlf2asp.solve.decode_model import SolveStatus
from ltlf2asp.solve.solver_interface import Solver
import pytest
from subprocess import Popen, PIPE
from random import random

FORMULAS = [
    line.strip()
    for line in (Path(__file__).parent / "formulas.txt").read_text().split("\n")
]


def check_black_output(max_horizon, formula):
    cmd = ["black-sat", "solve", "-k", str(max_horizon), "--finite", "-f", formula]
    black = Popen(cmd, stdout=PIPE, stderr=PIPE)
    black.wait()
    ans = black.stdout.read().decode("ascii").strip()
    # "SAT" "UNSAT" "UNKNOWN (stopped at k = ...)
    return ans == "SAT"


@pytest.mark.parametrize("formula", sorted(FORMULAS, key=lambda x: random())[:50])
@pytest.mark.random
@pytest.mark.slow
def test_ltlf2asp_and_black_agree_on_random_sample(formula):
    facts = parse_formula(formula)

    static_solver = Solver(True, 16)
    static_result = static_solver.solve(facts)

    incremental_solver = Solver(True, 16)
    incremental_result = incremental_solver.solve(facts)

    sat_for_black = check_black_output(16, formula)
    sat_incremental = incremental_result.status == SolveStatus.SATISFIABLE
    sat_static = static_result.status == SolveStatus.SATISFIABLE
    assert sat_for_black == sat_incremental == sat_static
