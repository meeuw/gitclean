import re
import subprocess
import sys


class PyParser:
    def __init__(self):
        self.buf = b''

    def before(self, line, number):
        if len(line.strip()) == 0:
            return line
        else:
            linenumber = "  #{0:04}\n".format(number).encode('utf8')
            return line[:-1] + linenumber

    def after(self, line, number):
        self.buf += line
        rows = []
        m = re.match(b'.*#(\d{4})$', line)
        if m:
            number += 1
            # if we are ahead, remove whitespace
            while int(m.group(1)) > number:
                if len(rows) > 0 and len(rows[-1]) == 0:
                    rows.pop()
                else:
                    break

            # if we are behind, add dummy rows
            while (number < int(m.group(1))):
                #print("skipping")
                rows.append(None)
                number += 1
            rows.append(self.buf[:-8] + b"\n")
            self.buf = b''
        elif len(line.strip()) == 0:
            number += 1
            rows.append(self.buf)
            self.buf = b''
        #print(line, number, rows)
        return rows

    def check(self, lines):
        p = subprocess.Popen(
            [sys.executable, "-m", "yapf"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        for i, line in enumerate(lines):
            p.stdin.write(line)
        p.stdin.close()

        for line in p.stdout:
            yield line
