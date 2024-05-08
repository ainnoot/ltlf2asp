import clingo
from ltlf2asp.parser import parse_formula
import pytest

class TestAtomicTokens:
    @pytest.mark.parametrize('token', ('true', 'True', 'TRUE'))
    def test_parse_true(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert clingo.Function('true', [clingo.Number(1)]) in dag
        assert clingo.Function('root', [clingo.Number(1)]) in dag

    @pytest.mark.parametrize('token', ('false', 'False', 'FALSE'))
    def test_parse_false(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert clingo.Function('false', [clingo.Number(1)]) in dag
        assert clingo.Function('root', [clingo.Number(1)]) in dag

    @pytest.mark.parametrize('token', ('last', 'Last', 'LAST', 'end', 'END', 'End'))
    def test_parse_last(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert clingo.Function('last', [clingo.Number(1)]) in dag
        assert clingo.Function('root', [clingo.Number(1)]) in dag

    @pytest.mark.parametrize('token', ('Abc', 'Ab2', 'A23_xyzXW'))
    def test_uppercase_symbol(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert clingo.Function('atomic', [clingo.Number(1), clingo.parse_term('uppercase_symbol("{}")'.format(token))]) in dag
        assert clingo.Function('root', [clingo.Number(1)]) in dag

    @pytest.mark.parametrize('token', ('"Abc"', '"Ab2"', '"A23_xyzXW"'))
    def test_quoted_symbol(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert clingo.Function('atomic', [clingo.Number(1), clingo.parse_term('quote("{}")'.format(token[1:-1]))]) in dag
        assert clingo.Function('root', [clingo.Number(1)]) in dag

    @pytest.mark.parametrize('token', ('abc', 'ab2', 'a23_xyzXW'))
    def test_clingo_symbol(self, token):
        dag = parse_formula(token)
        assert len(dag) == 2
        assert clingo.Function('atomic', [clingo.Number(1), clingo.parse_term(token)]) in dag
        assert clingo.Function('root', [clingo.Number(1)]) in dag

class TestUnaryTokens:
    @pytest.mark.parametrize('token', ('WX',))
    def test_weak_next(self, token):
        dag = parse_formula(f'{token} a')
        assert len(dag) == 3
        assert clingo.Function('weak_next', [clingo.Number(2), clingo.Number(1)]) in dag
        assert clingo.Function('root', [clingo.Number(2)]) in dag

    @pytest.mark.parametrize('token', ('WX',))
    def test_weak_next_wrapped(self, token):
        dag = parse_formula(f'{token}(a)')
        assert len(dag) == 3
        assert clingo.Function('weak_next', [clingo.Number(2), clingo.Number(1)]) in dag
        assert clingo.Function('root', [clingo.Number(2)]) in dag