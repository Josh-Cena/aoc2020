# Advent of Code 2020

Language: ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) (3.9)
Package Manager: [pip](https://pypi.org/project/pip/) with [venv](https://docs.python.org/3/library/venv.html)

You first need to start the virtual environment:

```bash
python3.9 -m venv aoc2020-env
source aoc2020-env/bin/activate
```

The only dependencies are `numpy` and `tqdm`.

This repo uses my standard AoC setup. Inputs are stored as `inputs/day{n}/{name}.txt`. By default `name` is `real` (the real question). To run a specific day's solution, use the following command:

```bash
python -m aoc2020 {day} {part} {name}
```

For example, to run the solution for day 1, part 2 with the example input:

```bash
python -m aoc2020 1 2 ex
```

(And make sure that `inputs/day1/ex.txt` exists.)
