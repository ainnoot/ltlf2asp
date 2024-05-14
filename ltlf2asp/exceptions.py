class ParsingError(Exception):
    pass


class UnsupportedOperator(Exception):
    def __init__(self, string: str) -> None:
        self.string: str = string

    def message(self) -> str:
        return self.string
