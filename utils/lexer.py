import re
import sys
from collections import deque
from dataclasses import dataclass

class Lexer:
    def __init__(self) -> None:
        pass

@dataclass
class Decorator:
    lineno: int
    language_name: str

@dataclass
class CodeBlock:
    lineno: int
    code: str

def lex(code):
    code += '\n'
    regex = '|'.join([
        r'(?P<decorator>@\w+\n)',
        r'(?P<code_block>[^ ].*\n(?: .*\n|\n)+)(?:\}\n)?',
        r'(?P<blank_line>\n)',
        r'(?P<error>.)',
    ])

    result = []
    for match in re.finditer(regex, code):
        lineno = code[:match.start()].count('\n') + 1
        if match.lastgroup == "decorator":
            result.append(Decorator(lineno, match.group().strip('@\n')))
        elif match.lastgroup == "code_block":
            result.append(CodeBlock(lineno, match.group()))
        elif match.lastgroup == 'blank_line':
            pass
        elif match.lastgroup == 'error':
            sys.exit(f"line {lineno}: syntax error")
        else:
            raise RuntimeError("Unknown error")

    return result
