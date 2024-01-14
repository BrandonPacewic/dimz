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


def gen_dim_table(dir: str | None) -> List[FileData]:
    valid_extensions, language_type = gen_filetypes()
    table: List[FileData] = []

    if dir:
        if dir[-1] != "/":
            sep = "/"
        else:
            sep = ""

        walk_path = dir
    else:
        walk_path = os.getcwd()

    for path, _, files in os.walk(walk_path):
        for filename in files:
            file_extension = f".{filename.split('.')[-1]}"

            if file_extension not in valid_extensions:
                continue

            filepath = os.path.join(path, filename)

            if dir:
                relfilepath = f"{dir}{sep}{os.path.relpath(filepath, walk_path)}"
            else:
                relfilepath = os.path.relpath(filepath, walk_path)

            if len(relfilepath) > 50:
                segments = []
                count = 0

                for x in reversed(relfilepath.split("/")):
                    if not len(segments):
                        segments.append(x)
                        count = len(x)
                        continue

                    if count + len(x) <= 45:
                        segments.append(x)
                        count += len(x)

                segments.append("...")
                relfilepath = "/".join(reversed(segments))

            try:
                with tokenize.open(filepath) as file:
                    tokenized = tokenize.generate_tokens(file.readline)
                    tokens = [t for t in tokenized if t.type in TOKEN_WHITELIST]
                    token_count = len(tokens)
                    line_count = len(set([t.start[0] for t in tokens]))
                    token_per_line = token_count / line_count if line_count else 0
            except (tokenize.TokenError, IndentationError, SyntaxError):
                token_count = -1
                line_count = -1
                token_per_line = -1
            finally:
                table.append(FileData(
                    relfilepath,
                    line_count,
                    token_count,
                    token_per_line,
                    language_type[file_extension],
                ))

    return sorted(table, key=lambda x: -x.line_count)


def main(args: List[str] = sys.argv[1:]) -> None:
    if len(args) > 1:
        print("Help: list <dir to give stats on>")
        sys.exit(1)

    headers = ["File Name", "Lines", "Tokens", "Tokens / Line", "Language"]
    table = gen_dim_table(args[0] if len(args) else None)
    file_count = len(table)

    print(tabulate([headers] + [x.expand() for x in table], headers="firstrow", floatfmt=".2f"))
    print(f"\nFile count: {file_count}")
    print(f"Total Line Count: {sum([x.line_count for x in table])}")
    print(f"Total Token Count: {sum([x.token_count for x in table])}")


if __name__ == "__main__":
    main()
