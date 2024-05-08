from ltlf2asp.parser import parse_formula
import sys
from pathlib import Path

contents = sys.argv[1]

ans = parse_formula(contents)

print(" ".join(str(x) for x in ans))