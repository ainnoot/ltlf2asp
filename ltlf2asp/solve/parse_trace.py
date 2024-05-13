from ltlf2asp.solve.decode_model import State
import json


def parse_state(state_dict):
    return State({x: (y.lower() == "true") for x, y in state_dict.items()})


def parse_trace(file: str):
    model = json.loads(file)
    states = model["model"]["states"]
    return tuple(parse_state(s) for s in states)
