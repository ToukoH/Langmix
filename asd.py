import subprocess
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path
import tempfile
import re


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

    # Tokenit:
    #     dekoraattoririvi @c, @python
    #     dekoraattoririvin jälkeen koodipätkä, voi olla '}' lopussa
    #     tyhjä rivi
    #     mitä vaan muuta on virhe
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
            raise RuntimeError("wat")

    return result


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


def write_files_to_tempdir(sections):
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = Path(tempdir)
        filenames = {"python": "filu.py", "c": "filu.c"}

        (tempdir / "filu.py").write_text(f"import ctypes; libfilu = ctypes.CDLL('{tempdir}/libfilu.so')\n")

        for section in sections:
            if section.language == 'c' and '(' in section.code:
                function_name = section.code.split('(')[0].split()[-1]
                with (tempdir / "filu.py").open('a', encoding='utf-8') as f:
                    f.write(f'{function_name} = libfilu.{function_name}\n')

        for section in sections:
            with (tempdir / filenames[section.language]).open("a", encoding="utf-8") as f:
                f.write(section.code)

        subprocess.call(['gcc', '-shared', '-o', 'libfilu.so', '-fPIC', 'filu.c'], cwd=tempdir)
        subprocess.call(['python3', 'filu.py'], cwd=tempdir)

        print(tempdir)
        import time; time.sleep(60)


with open(sys.argv[1], "r", encoding="utf-8") as file:
    code = file.read()
    tokens = lex(code)
    sections = parse(tokens)
    write_files_to_tempdir(sections)
