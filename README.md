## Langmix

Langmix is a tool which allows you to run C and Python within the same file. I can't really think any real life situation where this might be helpful, but I see this more as a fun and educative way to experiment with different topics of software engineering.

### Syntax

- **Decorators**: Start with an `@` symbol followed by the name of the programming language. Decorators must be placed at the beginning of a line, ending with a newline.
- **Code Blocks**: Decorators are followed by code blocs. They start with a non-space character and consist of lines that start with a space (tab). Blocks are separated by blank lines and can optionally end with a `}` on a new line.

### Instructions

- **Setup**: In addition to Python3 you'll need a couple of additional dependencies. These can be found from requirements.txt and installed by running:
`$ python3 -m pip install -r requirements.txt`.

- **Running Examples**: Explore the `./examples` directory for sample files. To run a file, use:
`$ python3 main.py ${filename.txt}`
