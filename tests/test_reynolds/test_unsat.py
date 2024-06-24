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
    ("a & (a -> G(~b)) & F(b)", "~a & a", "X(True) & (WX a) & G(a -> X(a))", "G(X(a))"),
)
def test_satisfiable_formulae(f):
    ans = check_on_tableaux(f, 25)
    print(ans)
    assert ans.unsatisfiable
