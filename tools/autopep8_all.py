# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import os

FORMAT_COMMAND = "autopep8 --in-place --aggressive --aggressive"
FILE_TARGETS = ["pydimz/*.py", "tools/*.py", "setup.py"]


def main():
    for file_target in FILE_TARGETS:
        if os.path.isdir(file_target):
            for root, _, files in os.walk(file_target):
                for file in files:
                    if file.endswith(".py"):
                        os.system(
                            f"{FORMAT_COMMAND} {os.path.join(root, file)}")
        else:
            os.system(f"{FORMAT_COMMAND} {file_target}")


if __name__ == "__main__":
    main()
