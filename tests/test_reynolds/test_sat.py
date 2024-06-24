import pytest

from ltlf2asp.parser import parse_formula_object, tableaux_reify
from ltlf2asp.solve.tableaux import Reynolds


def check_on_tableaux(formula_string, horizon):
    obj = parse_formula_object(formula_string).to_nnf()
    tab = Reynolds(False)
    facts = tableaux_reify(obj)
    print(" ".join(str(x) for x in facts))
    ans = tab.solve(facts, horizon)
    return ans


@pytest.mark.parametrize(
    "f",
    (
        "a",
        "~a",
        "a & b",
        "WX a",
        "X b",
        "(a U b) & (~a) & X(~a)",
        "F(a) & F(~a)",
        "G(a) & F(a)",
        "G(WX(a))",
    ),
)
def test_satisfiable_formulae(f):
    ans = check_on_tableaux(f, 25)
    print(ans)
    assert ans.satisfiable
