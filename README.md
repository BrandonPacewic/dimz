# :100: dimz

CLI tool for counting the number of lines of code in any given directory.

```
$ dimz
File Name                Lines    Tokens    Tokens / Line  Language
---------------------  -------  --------  ---------------  ----------
dimz/__main__.py            93       635             6.83  Python
dimz/test.py                39       255             6.54  Python
setup.py                    35       134             3.83  Python
tools/autopep8_all.py       15        83             5.53  Python
dimz/__init__.py             3         9             3.00  Python
push_pypi.sh                 2        11             5.50  Shell
test.sh                      2         4             2.00  Shell

File count: 7
Total Line Count: 189
Total Token Count: 1131
```

> [!NOTE]
> dimz only counts actual lines of code. Not whitespace. This means that if it tells you that you have a 100,000 line C project, you really did write 100,000 lines of C.

## License

Copyright (c) Brandon Pacewic

SPDX-License-Identifier: MIT
