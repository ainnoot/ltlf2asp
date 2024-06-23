from ltlf2asp.parser import parse_formula_object, tableaux_reify
from ltlf2asp.solve.tableaux import Reynolds


def check_on_tableaux(formula_string, horizon):
    obj = parse_formula_object(formula_string).to_nnf()
    tab = Reynolds(horizon, False)
    ans = tab.solve(tableaux_reify(obj))
    return ans


def test_has_model():
    formula_string = "G(a -> X a) & F(a)"
    ans = check_on_tableaux(formula_string, 20)
    assert ans.unsatisfiable


def test_no_finite_model():
    formula_string = "G(a -> X a) & F(a)"
    ans = check_on_tableaux(formula_string, 20)
    assert ans.unsatisfiable


def test_false():
    formula_string = "F(false)"
    ans = check_on_tableaux(formula_string, 20)
    assert ans.unsatisfiable


def test_true():
    formula_string = "G(true)"
    ans = check_on_tableaux(formula_string, 20)
    assert ans.satisfiable


def test_declare_inconsistency():
    formula_string = "G(a -> X b) & G(b -> X a) & F(a)"
    ans = check_on_tableaux(formula_string, 20)
    assert ans.unsatisfiable


def test_declare_looks_inconsistent_but_vacuous():
    formula_string = "G(a -> X b) & G(b -> X a) & F(c)"
    ans = check_on_tableaux(formula_string, 20)
    assert ans.satisfiable


def test_trivially_false():
    formula_string = "a & ~a"
    ans = check_on_tableaux(formula_string, 20)
    assert ans.unsatisfiable
