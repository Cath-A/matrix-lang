"""Find the largest square matrix you can multiply in under 10 seconds."""

import sys
import os
import timeit
import random
import unittest

_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _root in sys.path:
    sys.path.remove(_root)
if _src not in sys.path:
    sys.path.insert(0, _src)

from matrix import Matrix

TIME_LIMIT = 10.0
TIMEIT_REPS = 3
START_SIZE = 200   # <-- change this to skip straight to a known ballpark
EXPONENT = 3     # <-- O(n^k): 2 for generation, 3 for multiplication, etc.


def make_random_matrix(size: int) -> Matrix:
    return Matrix([[random.random() for _ in range(size)] for _ in range(size)])


def time_mul(size: int) -> float:
    a = make_random_matrix(size)
    b = make_random_matrix(size)
    return timeit.timeit(lambda: a * b, number=TIMEIT_REPS) / TIMEIT_REPS


def project(size: int, t: float, target: float, exponent: float = EXPONENT) -> int:
    """Project what size would hit `target` seconds, assuming O(n^exponent) scaling."""
    return max(1, int(size * (target / t) ** (1 / exponent)))


class TestMultiplicationLimit(unittest.TestCase):

    def test_find_largest_multipliable_matrix(self):

        print(f"\n  Starting at n={START_SIZE}, time limit={TIME_LIMIT}s, O(n^{EXPONENT})")
        print(f"  {'─' * 44}")

        size = START_SIZE
        t = time_mul(size)
        status = "OVER" if t >= TIME_LIMIT else "UNDER"
        print(f"  [{status}] n={size:>5}  →  {t*1000:>8.0f}ms")

        if t >= TIME_LIMIT:
            lo = project(size, t, TIME_LIMIT * 0.5)
            hi = size
            print(f"  Overshot — projecting lo down to n={lo}")
        else:
            lo = size
            hi = project(size, t, TIME_LIMIT * 1.5)
            print(f"  Undershot — projecting hi up to n={hi}")

            t_hi = time_mul(hi)
            status = "OVER" if t_hi >= TIME_LIMIT else "UNDER"
            print(f"  [{status}] n={hi:>5}  →  {t_hi*1000:>8.0f}ms")

            while t_hi < TIME_LIMIT:
                lo = hi
                hi = project(hi, t_hi, TIME_LIMIT * 1.5)
                t_hi = time_mul(hi)
                status = "OVER" if t_hi >= TIME_LIMIT else "UNDER"
                print(f"  [{status}] n={hi:>5}  →  {t_hi*1000:>8.0f}ms  (nudging hi up)")

        print(f"  {'─' * 44}")
        print(f"  Binary search between n={lo} and n={hi}")
        print(f"  {'─' * 44}")

        while hi - lo > 1:
            mid = (lo + hi) // 2
            t_mid = time_mul(mid)
            status = "OVER" if t_mid >= TIME_LIMIT else "UNDER"
            bound = "→ hi" if t_mid >= TIME_LIMIT else "→ lo"
            print(f"  [{status}] n={mid:>5}  →  {t_mid*1000:>8.0f}ms  {bound}={mid}")
            if t_mid < TIME_LIMIT:
                lo = mid
            else:
                hi = mid

        print(f"  {'─' * 44}")
        t_final = time_mul(lo)
        print(f"\n  Largest multipliable matrix: {lo}x{lo}  —  {t_final*1000:.0f}ms")


if __name__ == '__main__':
    unittest.main(verbosity=2)
