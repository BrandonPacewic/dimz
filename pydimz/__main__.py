# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

"""
pydimz - CLI tool for counting the number of lines of code in any given project.
"""

import os
import json
import sys
import token
import tokenize

from dataclasses import dataclass
from tabulate import tabulate
from typing import List, Tuple

MODULE_DIR = os.path.dirname(__file__)
TOKEN_WHITELIST = [token.OP, token.NAME, token.NUMBER, token.STRING]


@dataclass
class FileData:
    filename: str
    line_count: int
    token_count: int
    token_per_line: float
    language: str

    def expand(self) -> List[str | int | float]:
        attrs = vars(self)
        return [x for x in attrs.values()]


def gen_filetypes() -> Tuple[set, dict[str, str]]:
    with open(f"{MODULE_DIR}/language_extensions.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    
    return set([x for x in data.keys()]), data


def gen_dim_table(dir: str = os.getcwd()) -> List[FileData]:
    valid_extensions, language_type = gen_filetypes()
    table: List[FileData] = []

    for path, _, files in os.walk(dir):
        for filename in files:
            file_extension = f".{filename.split('.')[-1]}"

            if not file_extension in valid_extensions:
                continue

            filepath = os.path.join(path, filename)
            relfilepath = os.path.relpath(filepath, dir)

            if len(relfilepath) > 50:
                relfilepath = f"...{relfilepath[-50:]}"

            try:
                with tokenize.open(filepath) as file:
                    tokenized = tokenize.generate_tokens(file.readline)
                    tokens = [t for t in tokenized if t.type in TOKEN_WHITELIST]
                    token_count = len(tokens)
                    line_count = len(set([t.start[0] for t in tokens]))
            except (tokenize.TokenError, IndentationError, SyntaxError):
                token_count = -1
                line_count = -1
            finally:
                table.append(FileData(
                    relfilepath,
                    line_count,
                    token_count,
                    token_count / line_count if line_count else 0,
                    language_type[file_extension],
                ))

    return sorted(table, key=lambda x: -x.line_count)


def main(args: List[str] = sys.argv[1:]) -> None:
    if len(args) > 1:
        print("Help: list <dir to give stats on>")
        sys.exit(1)

    headers = ["File Name", "Lines", "Tokens", "Tokens / Line", "Language"]
    table = gen_dim_table(args[0] if len(args) else os.getcwd())

    print(tabulate([headers] + [x.expand() for x in table], headers="firstrow", floatfmt=".2f"))
    print(f"\nFile count: {len(table)}")
    print(f"Total Line Count: {sum([x.line_count for x in table])}")
    print(f"Total Token Count: {sum([x.token_count for x in table])}")


if __name__ == "__main__":
    main()
