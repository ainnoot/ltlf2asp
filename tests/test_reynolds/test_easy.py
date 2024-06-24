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


def test_unsat_over_next():
    formula_string = "X(~a) & X(a)"
    ans = check_on_tableaux(formula_string, 20)
    assert ans.unsatisfiable


def test_unsat_over_next_and_eventually():
    formula_string = "F(a & b) & G(a -> ~c) & G(b -> c)"
    ans = check_on_tableaux(formula_string, 20)
    assert ans.unsatisfiable


def test_unsat_over_until():
    formula_string = "~b & (a U b) & G(a -> ~c) & G(~c -> X(d)) & G(d & b)"
    ans = check_on_tableaux(formula_string, 50)
    assert ans.unsatisfiable


def test_unsat_over_until_2():
    formula_string = "~b & (a U b) & G(a -> X(a))"
    ans = check_on_tableaux(formula_string, 50)
    assert ans.unsatisfiable


def test_unsat_over_disjunction():
    formula_string = (
        "(a | b | c) & G(a -> X(a)) & (F(b) <-> F(c)) & (b -> G(~c)) & (c -> G(~b))"
    )
    ans = check_on_tableaux(formula_string, 50)
    assert ans.unsatisfiable


def test_sat_empty_model():
    formula_string = "G(a -> (WX a))"
    ans = check_on_tableaux(formula_string, 50)
    assert ans.satisfiable
