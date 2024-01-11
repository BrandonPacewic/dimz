# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import setuptools
import sys

try:
    import lines
except ImportError:
    print("Error importing pylines")
    sys.exit(1)

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


def main() -> None:
    setuptools.setup(
        name="pylines",
        version=lines.__version__,
        author="Brandon Pacewic",
        description="",
        long_description_content_type="text/markdown",
        long_description=long_description,
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],
        url="https://github.com/BrandonPacewic/pylines",
        packages=["pylines"],
        entry_points={
            "console_scripts": [
                "lines=lines.__main__:main",
            ],
        },
        python_requires=">=3.10",
        include_package_data=True,
    )


if __name__ == "__main__":
    main()
