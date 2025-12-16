import sys
from importlib import import_module

day = sys.argv[1]
prob = sys.argv[2]
input = sys.argv[3] if len(sys.argv) > 3 else "real"
filename = f"inputs/day{day}/{input}.txt"
contents = open(filename).read().strip().split("\n")

mod = import_module(f".day{day}", package=__package__)
solver = getattr(mod, f"solve{prob}")
solver(contents)
