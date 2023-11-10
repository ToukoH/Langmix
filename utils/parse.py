import sys
from collections import deque
from .lexer import Decorator, CodeBlock
from dataclasses import dataclass


class Parse:
    def __init__(self) -> None:
        pass

@dataclass
class Section:
    language: str
    code: str

def parse(tokens) -> list[Section]:
    result = []
    tokens = deque(tokens)

    while tokens:
        if (
            len(tokens) < 2
            or not isinstance(tokens[0], Decorator)
            or not isinstance(tokens[1], CodeBlock)
        ):
            sys.exit(f"line {tokens[0].lineno}: decorators and code blocks must alternate")

        if tokens[0].language_name not in ('python', 'c'):
            sys.exit(f"line {tokens[0].lineno}: unsupported language: {tokens[0].language_name}")

        result.append(Section(tokens[0].language_name, tokens[1].code))
        del tokens[0]
        del tokens[0]

    return result
