# :100: pydimz

CLI tool for counting the number of lines of code in any given directory.

```
$ dimz
File Name                Lines    Tokens    Tokens / Line
---------------------  -------  --------  ---------------
pydimz/__main__.py          38       326             8.58
setup.py                    35       134             3.83
tools/autopep8_all.py       15        83             5.53
pydimz/__init__.py           3         9             3.00

Total Line Count: 91
```

> [!NOTE]
> pydimz only counts actual lines of not. Not whitespace. This means that if it tells you that you have a 100,000 line C project, you really did write 100,000 lines of C.

## License

Copyright (c) Brandon Pacewic

SPDX-License-Identifier: MIT
