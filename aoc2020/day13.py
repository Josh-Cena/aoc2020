import numpy as np


def solve1(data: list[str]):
    time = int(data[0])
    buses = np.array([int(x) for x in data[1].split(",") if x != "x"])
    next_arrive = (np.ceil(time / buses) * buses).astype(int)
    next_arrive_bus = np.argmin(next_arrive)
    print(buses[next_arrive_bus] * (next_arrive[next_arrive_bus] - time))


# Need to find lowest t:
# t mod a1 == a1 - b1
# t mod a2 == a2 - b2
# t mod a3 == a3 - b3
# ...
# where an is the bus id, bn is the index of that bus
# This is just CRT
def solve2(data: list[str]):
    buses = [
        (int(x), int(x) - i) for (i, x) in enumerate(data[1].split(",")) if x != "x"
    ]
    t, m = 0, 1  # t mod 1 == 0
    for a, b in buses:
        # Find t such that t mod a_i == b_i while holding all previous equations
        # true; this is done by incrementing t by steps of m where m is the
        # product of previous moduli
        # (m * k) mod a_i == b_i - t
        k = ((b - t) * pow(m, -1, a)) % a
        t += m * k
        m *= a
        t %= m
    print(t)
