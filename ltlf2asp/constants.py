from enum import StrEnum


class Constants(StrEnum):
    TRUE = "true"
    FALSE = "false"
    LAST = "last"
    END = "end"
    ROOT = "root"
    ATOMIC = "atomic"
    NEXT = "next"
    WEAK_NEXT = "weak_next"
    EVENTUALLY = "eventually"
    ALWAYS = "always"
    NEGATE = "negate"
    IMPLIES = "implies"
    CONJUNCTION = "conjunction"
    DISJUNCTION = "disjunction"
    EQUALS = "equivalent"
    UNTIL = "until"
    WEAK_UNTIL = "weak_until"
    RELEASE = "release"
    STRONG_RELEASE = "strong_release"
