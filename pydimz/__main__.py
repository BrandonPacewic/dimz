# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
pydimz - CLI tool for counting the number of lines of code in any given project.
"""

import os
import sys
import token
import tokenize

from tabulate import tabulate
from typing import List

TOKEN_WHITELIST = [token.OP, token.NAME, token.NUMBER, token.STRING]


def gen_line_table(dir: str = os.getcwd()) -> List[List[str | int]]:
    table: List[List[str | int]] = []

    for path, _, files in os.walk(dir):
        for filename in files:
            if not filename.endswith(".py"):
                continue

            filepath = os.path.join(path, filename)
            relfilepath = os.path.relpath(filepath, dir)

            with tokenize.open(filepath) as file:
                tokens = [t for t in tokenize.generate_tokens(file.readline) if t.type in TOKEN_WHITELIST]
                token_count, line_count = len(tokens), len(set([t.start[0] for t in tokens]))
                table.append([relfilepath, line_count, token_count / line_count])

    return table


def main(args: List[str] = sys.argv[1:]) -> None:
    if len(args) > 1:
        print("Help: list <dir to give stats on>")
        sys.exit(1)

    headers = ["File Name", "Lines", "Tokens / Line"]
    table = gen_line_table(args[0] if len(args) else os.getcwd())

    print(tabulate([headers] + sorted(table, key=lambda x: -x[1]), headers="firstrow", floatfmt=".2f") + "\n")
    print(f"Total Line Count: {sum([x[1] for x in table])}")


if __name__ == "__main__":
    main()
