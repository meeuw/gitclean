#!/usr/bin/python
import subprocess
import re
import sys
import click

from vcscheck.pyparser import PyParser
from vcscheck.phpparser import PHPParser
from vcscheck.jsparser import JSParser


class GIT:
    def cat(self, ref, filename):
        if ref is None:
            with open(filename, 'rb') as f:
                for line in f:
                    yield line
        else:
            p = subprocess.Popen(
                ["git", "show", ref + ":" + filename], stdout=subprocess.PIPE)
            for line in p.stdout:
                yield line

    def diff(self, ref):
        p = subprocess.Popen(
            ['git', 'diff', '-p', '-U0', ref], stdout=subprocess.PIPE)
        for line in p.stdout:
            yield line

    def ref_to(self, ref):
        s = ref.split('..')
        if len(s) > 1:
            return s[1]


def dos2unix(s):
    if s[-2:] == b'\r\n':
        return s[:-2] + b'\n'
    else:
        return s


def preprocess(s):
    if s is None:
        s = ""
    else:
        s = s.decode('utf8')
    return s.replace(' ', '·').replace('\t', '  ⇥ ').replace('\n', '⏎\n')


def vcscheck(vcs, ref):
    diff = vcs.diff(ref)
    ref_to = vcs.ref_to(ref)

    files = {}
    for line in diff:
        line = dos2unix(line)
        m = re.match(b'^[+-]{3} ([ab])/(.*)', line)
        if m and m.group(1) == b'b':
            filename = m.group(2).decode('utf8')
            if not filename in files:
                files[filename] = []
        m = re.match(b'^@@ -([0-9,]+) \+([0-9,]+) @@', line)
        if m:
            s = m.group(2).decode('utf8').split(",")
            start = int(s[0])
            if len(s) == 2:
                count = int(s[1])
            else:
                count = 1
            files[filename] += list(range(start, start + count))

    for filename, ranges in files.items():
        if not filename.endswith('.php') and not filename.endswith(
                '.py') and not filename.endswith('.js'):
            continue
        if filename.endswith('.php'):
            parser = PHPParser()
        if filename.endswith('.py'):
            parser = PyParser()
        if filename.endswith('.js'):
            parser = JSParser()

        target = vcs.cat(ref_to, filename)
        with_linenumbers = (parser.before(dos2unix(line), i + 1)
                            for i, line in enumerate(target))
        checked = parser.check(with_linenumbers)

        i = 0
        rows = []
        for line in checked:
            line = dos2unix(line)
            row = parser.after(line, i)
            i += len(row)
            rows += row

        table_data = []
        problem = False
        for i, line in enumerate(vcs.cat(ref_to, filename)):
            line = dos2unix(line)
            if rows[i] != line and i + 1 in ranges:
                problem = True
                table_data.append(
                    [i + 1, preprocess(line), preprocess(rows[i])])

        if problem:
            for d in table_data:
                print("{0}:{1}".format(filename, d[0]))
                print(d[1])
                print(d[2])
        else:
            print(filename, "OK")


@click.command()
@click.argument('ref', default='HEAD')
def gitcheck(ref):
    git = GIT()
    vcscheck(git, ref)
