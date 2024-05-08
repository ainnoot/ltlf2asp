import clingo
from ltlf2asp.parser import parse_formula
import pytest


class TestAtomicTokens:
    @pytest.mark.parametrize("token", ("true", "True", "TRUE"))
    def test_parse_true(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert clingo.Function("true", [clingo.Number(1)]) in dag
        assert clingo.Function("root", [clingo.Number(1)]) in dag

    @pytest.mark.parametrize("token", ("false", "False", "FALSE"))
    def test_parse_false(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert clingo.Function("false", [clingo.Number(1)]) in dag
        assert clingo.Function("root", [clingo.Number(1)]) in dag

    @pytest.mark.parametrize("token", ("last", "Last", "LAST", "end", "END", "End"))
    def test_parse_last(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert clingo.Function("last", [clingo.Number(1)]) in dag
        assert clingo.Function("root", [clingo.Number(1)]) in dag

    @pytest.mark.parametrize("token", ("Abc", "Ab2", "A23_xyzXW"))
    def test_uppercase_symbol(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert (
            clingo.Function("atomic", [clingo.Number(1), clingo.String(token)]) in dag
        )
        assert clingo.Function("root", [clingo.Number(1)]) in dag

    @pytest.mark.parametrize("token", ('"Abc"', '"Ab2"', '"A23_xyzXW"'))
    def test_quoted_symbol(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert (
            clingo.Function("atomic", [clingo.Number(1), clingo.String(token)]) in dag
        )
        assert clingo.Function("root", [clingo.Number(1)]) in dag

    @pytest.mark.parametrize("token", ("abc", "ab2", "a23_xyzXW"))
    def test_clingo_symbol(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert (
            clingo.Function("atomic", [clingo.Number(1), clingo.String(token)]) in dag
        )
        assert clingo.Function("root", [clingo.Number(1)]) in dag


class TestUnaryTokens:
    @pytest.mark.parametrize("token", ("WX",))
    def test_weak_next(self, token):
        dag = parse_formula(f"{token} a")
        assert len(dag) == 3
        assert clingo.Function("weak_next", [clingo.Number(2), clingo.Number(1)]) in dag
        assert clingo.Function("root", [clingo.Number(2)]) in dag

    @pytest.mark.parametrize("token", ("WX",))
    def test_weak_next_wrapped(self, token):
        dag = parse_formula(f"{token}(a)")
        assert len(dag) == 3
        assert clingo.Function("weak_next", [clingo.Number(2), clingo.Number(1)]) in dag
        assert clingo.Function("root", [clingo.Number(2)]) in dag

    def test_until(self):
        dag = parse_formula("a U b")
        assert len(dag) == 4
        assert (
            clingo.Function(
                "until", [clingo.Number(3), clingo.Number(1), clingo.Number(2)]
            )
            in dag
        )
        assert clingo.Function("root", [clingo.Number(3)]) in dag

    def test_weak_until(self):
        dag = parse_formula("a W b")
        assert len(dag) == 4
        assert (
            clingo.Function(
                "weak_until", [clingo.Number(3), clingo.Number(1), clingo.Number(2)]
            )
            in dag
        )
        assert clingo.Function("root", [clingo.Number(3)]) in dag

    def test_release(self):
        dag = parse_formula("a R b")
        assert len(dag) == 4
        assert (
            clingo.Function(
                "release", [clingo.Number(3), clingo.Number(1), clingo.Number(2)]
            )
            in dag
        )
        assert clingo.Function("root", [clingo.Number(3)]) in dag

    def test_strong_release(self):
        dag = parse_formula("a M b")
        assert len(dag) == 4
        assert (
            clingo.Function(
                "strong_release", [clingo.Number(3), clingo.Number(1), clingo.Number(2)]
            )
            in dag
        )
        assert clingo.Function("root", [clingo.Number(3)]) in dag
