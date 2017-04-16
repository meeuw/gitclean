def test_parser(parser, code):
    def add_linenumbers(code):
        for i, line in enumerate(code.splitlines()):
            line += b"\n"
            yield parser.before(line, i + 1)

    i = 0
    checked = parser.check(add_linenumbers(code))
    for line in checked:
        rows = parser.after(line, i)
        i += len(rows)
        rows = list(filter(lambda row: row is not None, rows))
        if len(rows) == 0:
            continue
        yield b"\n".join(rows)


def splitlines(code):
    for line in code.splitlines():
        yield line + b"\n"
