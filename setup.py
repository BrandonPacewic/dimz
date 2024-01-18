# Copyright (c) Brandon Pacewic
# SPDX-License-Identifier: MIT

import setuptools
import sys

try:
    import dimz
except ImportError:
    print("Error importing pylines")
    sys.exit(1)

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

    # Remove emoji from pypi package readme.
    long_description = f"#{long_description[7:]}"


def main() -> None:
    setuptools.setup(
        name="dimz",
        version=dimz.__version__,
        author="Brandon Pacewic",
        description="",
        long_description_content_type="text/markdown",
        long_description=long_description,
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],
        url="https://github.com/BrandonPacewic/dimz",
        packages=["dimz"],
        entry_points={
            "console_scripts": [
                "dimz=dimz.__main__:main",
            ],
        },
        python_requires=">=3.10",
        include_package_data=True,
    )


if __name__ == "__main__":
    main()
