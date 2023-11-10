from pathlib import Path
import subprocess
import sys
import tempfile
import time

from utils.parse import parse
from utils.lexer import lex

def write_files_to_tempdir(sections):
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = Path(tempdir)
        filenames = {"python": "tmpfile.py", "c": "tmpfile.c"}

        (tempdir / "tmpfile.py").write_text(f"import ctypes; libtmpfile = ctypes.CDLL('{tempdir}/libtmpfile.so')\n")

        for section in sections:
            if section.language == 'c' and '(' in section.code:
                function_name = section.code.split('(')[0].split()[-1]
                with (tempdir / "tmpfile.py").open('a', encoding='utf-8') as f:
                    f.write(f'{function_name} = libtmpfile.{function_name}\n')

        for section in sections:
            with (tempdir / filenames[section.language]).open("a", encoding="utf-8") as f:
                f.write(section.code)

        subprocess.call(['gcc', '-shared', '-o', 'libtmpfile.so', '-fPIC', 'tmpfile.c'], cwd=tempdir)
        subprocess.call(['python3', 'tmpfile.py'], cwd=tempdir)

def main(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
        tokens = lex(code)
        sections = parse(tokens)
        write_files_to_tempdir(sections)

if __name__ == "__main__":
    main(sys.argv[1])
