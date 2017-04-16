import re
import subprocess


class PHPParser:
    def __init__(self):
        self.buf = b''

    def before(self, line, number):
        if len(line.strip()) == 0:
            typ = 'B'  # blanc
        else:
            typ = 'N'  # non-blanc
        linenumber = " //{0}{1:04}\n".format(typ, number).encode('utf8')
        return line[:-1] + linenumber

    def after(self, line, number):
        self.buf += line
        rows = []
        m = re.match(b'.* //([NB])(\d{4})$', line)
        if m:
            #print(m.group(1), line[:-9], len(line[:-9]))
            if len(line[:-9].strip()) == 0 and m.group(1) == b"N":
                self.buf = self.buf[:-1]  # remove introduced empty new-line
            #print('match')
            number += 1
            while (number < int(m.group(2))):
                #print("skipping")
                rows.append(None)
                number += 1
            rows.append(self.buf[:-9] + b"\n")
            self.buf = b''
        #print(i)
        return rows

    def check(self, lines):
        p = subprocess.Popen(
            ["phpcbf", "--standard=PSR2"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        for i, line in enumerate(lines):
            p.stdin.write(line)
        p.stdin.close()

        for line in p.stdout:
            yield line
