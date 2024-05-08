import clingo

from ltlf2asp.parser.reify_as_atoms import InjectIntoBackend
from ltlf2asp.parser.parser import _parse_formula
import sys

contents = sys.argv[1]

ctl = clingo.Control()
with ctl.backend() as backend:
    _parse_formula(contents, "start", InjectIntoBackend(backend))
ctl.ground([("base", [])])

for x in ctl.symbolic_atoms:
    print(str(x.symbol))