from ltlf2asp.parser.reify_as_object import ReifyFormulaAsObject
from ltlf2asp.parser.parser import _parse_formula
from ltlf2asp.parser.syntax import (
    Proposition,
    WeakNext,
    Faux,
    Last,
    Truth,
)
import pytest


class TestAtomicTokens:
    @pytest.mark.parametrize("token", ("true", "True", "TRUE"))
    def test_parse_true(self, token):
        dag = _parse_formula(token, "start", ReifyFormulaAsObject())
        assert dag == Truth()

    @pytest.mark.parametrize("token", ("false", "False", "FALSE"))
    def test_parse_false(self, token):
        dag = _parse_formula(token, "start", ReifyFormulaAsObject())
        assert dag == Faux()

    @pytest.mark.parametrize("token", ("last", "Last", "LAST", "end", "END", "End"))
    def test_parse_last(self, token):
        dag = _parse_formula(token, "start", ReifyFormulaAsObject())
        assert dag == Last()

    @pytest.mark.parametrize("token", ("Abc", "Ab2", "A23_xyzXW"))
    def test_uppercase_symbol(self, token):
        dag = _parse_formula(token, "start", ReifyFormulaAsObject())
        assert dag == Proposition(token)

    @pytest.mark.parametrize("token", ('"Abc"', '"Ab2"', '"A23_xyzXW"'))
    def test_quoted_symbol(self, token):
        dag = _parse_formula(token, "start", ReifyFormulaAsObject())
        assert dag == Proposition(token)

    @pytest.mark.parametrize("token", ("abc", "ab2", "a23_xyzXW"))
    def test_clingo_symbol(self, token):
        dag = _parse_formula(token, "start", ReifyFormulaAsObject())
        assert dag == Proposition(token)


class TestUnaryTokens:
    @pytest.mark.parametrize("token", ("a", "Abc", "x12_23"))
    def test_weak_next(self, token):
        dag = _parse_formula("WX {}".format(token), "start", ReifyFormulaAsObject())
        assert dag == WeakNext(Proposition(token))

    @pytest.mark.parametrize("token", ("a",))
    def test_weak_next_wrapped(self, token):
        dag = _parse_formula("WX ({})".format(token), "start", ReifyFormulaAsObject())
        assert dag == WeakNext(Proposition(token))
