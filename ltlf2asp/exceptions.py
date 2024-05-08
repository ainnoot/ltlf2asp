class ParsingError(Exception):
    pass


class UnsupportedOperator(Exception):
    def __init__(self, string):
        self.string = string

    def message(self):
        return self.string
