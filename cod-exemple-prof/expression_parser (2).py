"""Implement a simple expression evaluator parses."""

# For easier connection with class examples, we use names such as E or T_prime.
# pylint: disable=invalid-name

# Language definition:
#
# E = TE'
# E' = +TE' | - TE' | &
# T = FT'
# T' = * FT' | / FT' | &
# F = ( E ) | num
# num = [+-]?([0-9]+(.[0-9]+)?|.[0-9]+)(e[0-9]+)+)?)

import re


class ParserError(Exception):
    """An error exception for parser errors."""


class Lexer:
    """Implements the expression lexer."""

    OPEN_PAR = 1
    CLOSE_PAR = 2
    OPERATOR = 3
    NUM = 4

    def __init__(self, data):
        """Initialize object."""
        self.data = data
        self.current = 0
        self.previous = -1
        self.num_re = re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)(e\d+)?")

    def __iter__(self):
        """Start the lexer iterator."""
        self.current = 0
        return self

    def error(self, msg=None):
        """Generate a Lexical Errro."""
        err = (
            f"Error at pos {self.current}: "
            f"{self.data[self.current - 1:self.current + 10]}"
        )
        if msg is not None:
            err = f"{msg}\n{err}"
        raise ParserError(err)

    def put_back(self):
        # At most une token can be put back in the stream.
        self.current = self.previous

    def peek(self):
        if self.current < len(self.data):
            current = self.current
            while self.data[current] in " \t\n\r":
                current += 1
            previous = current
            char = self.data[current]
            current += 1
            if char == "(":
                return (Lexer.OPEN_PAR, char, current)
            if char == ")":
                return (Lexer.CLOSE_PAR, char, current)
            # Do not handle minus operator.
            if char in "+/*":
                return (Lexer.OPERATOR, char, current)
            match = self.num_re.match(self.data[current - 1 :])
            if match is None:
                # If there is no match we may have a minus operator
                if char == "-":
                    return (Lexer.OPERATOR, char, current)
                # If we get here, there is an error an unexpected char.
                raise Exception(
                    f"Error at {current}: "
                    f"{self.data[current - 1:current + 10]}"
                )
            current += match.end() - 1
            return (Lexer.NUM, match.group().replace(" ", ""), current)
        return (None, None, self.current)

    def __next__(self):
        """Retrieve the next token."""
        token_id, token_value, current = self.peek()
        if token_id is not None:
            self.previous = self.current
            self.current = current
            return (token_id, token_value)
        raise StopIteration()


def parse_E(data):
    """Parse rule E."""
    # print("E -> TE'")
    # E -> TE'  { $0 = T + E' }
    T = parse_T(data)
    E_prime = parse_E_prime(data)
    return T + (E_prime or 0)


def parse_E_prime(data):
    """Parse rule E'."""
    # print("E' -> +TE' | -TE'| &")
    try:
        token, operator = next(data)
    except StopIteration:
        # E' -> &  { $0 = 0 }
        return 0
    if token == Lexer.OPERATOR and operator in "+-":
        # E' -> +TE' { $0 = T + E' } | -TE' { $0 = T - E' }
        T = parse_T(data)
        E_prime = parse_E_prime(data)
        return (T if operator == "+" else -1 * T) + (E_prime or 0)

    if token not in [Lexer.OPERATOR, Lexer.OPEN_PAR, Lexer.CLOSE_PAR]:
        data.error(f"Invalid character: {operator}")

    # E' -> &  { $0 = 0 }
    data.put_back()
    return 0


def parse_T(data):
    """Parse rule T."""
    # print("T -> FT'")
    # T -> FT'  { $0 = F * T' }
    F = parse_F(data)
    T_prime = parse_T_prime(data)
    return F * (T_prime or 1)


def parse_T_prime(data):
    """Parse rule T'."""
    # print("T' -> *FT' | /FT'| &")
    try:
        token, operator = next(data)
    except StopIteration:
        # T' -> &  { $0 = 1 }
        return 1
    if token == Lexer.OPERATOR and operator in "*/":
        # T' -> *FT' { $0 = F*T' } | /FT' {$0 = F*(1/T')}
        F = parse_F(data)
        T_prime = parse_T_prime(data)
        return (F if operator == "*" else 1 / F) * T_prime

    if token not in [Lexer.OPERATOR, Lexer.OPEN_PAR, Lexer.CLOSE_PAR]:
        data.error(f"Invalid character: {operator}")

    # T' -> &  { $0 = 1 }
    data.put_back()
    return 1


def parse_F(data):
    """Parse rule F."""
    # print("F -> num | (E)")
    try:
        token, value = next(data)
    except StopIteration:
        raise Exception("Unexpected end of source.") from None
    if token == Lexer.OPEN_PAR:
        # F -> (E)  { $0 = E }
        E = parse_E(data)
        try:
            if next(data) != (Lexer.CLOSE_PAR, ")"):
                data.error("Unbalanced parenthesis.")
        except StopIteration:
            data.error("Unbalanced parenthesis.")
        return E
    if token == Lexer.NUM:
        # F -> num   { $0 = float(num) }
        return float(value)
    raise data.error(f"Unexpected token: {value}.")


def parse(source_code):
    """Parse the source code."""
    lexer = Lexer(source_code)
    return parse_E(lexer)


if __name__ == "__main__":
    expressions = [
        ("1 + 1", 1 + 1),
        ("2 * 3", 2 * 3),
        ("5 / 4", 5 / 4),
        ("2 * 3 + 1", 2 * 3 + 1),
        ("1 + 2 * 3", 1 + 2 * 3),
        ("(2 * 3) + 1", (2 * 3) + 1),
        ("2 * (3 + 1)", 2 * (3 + 1)),
        ("(2 + 1) * 3", (2 + 1) * 3),
        ("-2 + 3", -2 + 3),
        ("5 + (-2)", 5 + (-2)),
        ("5 * -2", 5 * -2),
        ("-1 - -2", -1 - -2),
        ("-1 - 2", -1 - 2),
        ("4 - 5", 4 - 5),
        ("1 - 2", 1 - 2),
        ("3 - ((8 + 3) * -2)", 3 - ((8 + 3) * -2)),
        ("2.01e2 - 200", 2.01e2 - 200),
        ("2*3*4", 2 * 3 * 4),
        ("2 + 3 + 4 * 3 * 2 + 2", 2 + 3 + 4 * 3 * 2 * 2),
        ("10 + 11", 10 + 11),
    ]

    for expression, expected in expressions:
        result = "PASS" if parse(expression) == expected else "FAIL"
        print(f"Expression: {expression} - {result}")

    try:
        print("Expression: 1 1 1")
        print(parse("1 1 1"))
    except ParserError as perr:
        print(perr)

    try:
        print("Expression: (1")
        print(parse("(1"))
    except ParserError as perr:
        print(perr)
