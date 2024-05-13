from pathlib import Path
from re import sub

FORMULAS = [
    line.strip()
    for line in (Path(__file__).parent / "spot.txt").read_text().split("\n")
    if not line.startswith("%")
]

FALSE_RE = r"\(0\)"
TRUE_RE = r"\(1\)"


def fix(f: str):
    if f == "0":
        return "False"
    elif f == "1":
        return "True"

    f = sub(FALSE_RE, "False", f)
    f = sub(TRUE_RE, "True", f)
    return f


if __name__ == "__main__":
    output = Path(__file__).parent / "formulas.txt"
    with output.open("w") as f:
        for formula in FORMULAS:
            if len(formula.strip()) > 0:
                f.write(fix(formula))
                f.write("\n")
