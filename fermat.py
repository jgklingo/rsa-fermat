import argparse
import random


# This is a convenience function for main(). You don't need to touch it.
def prime_test(N: int, k: int) -> tuple[str, str]:
    return fermat(N, k), miller_rabin(N, k)


# My original recursive implementation, was hitting recursion limits.
# def mod_exp(x: int, y: int, N: int) -> int:
#     if y == 0:
#         return 1
#     Z = mod_exp(x, y // 2, N)
#     if y % 2 == 0:
#         return Z ** 2 % N
#     else:
#         return Z ** 2 * x % N 


def mod_exp(x: int, y: int, N: int) -> int:
    res = 1
    base = x % N
    while y > 0:
        if y % 2 == 1:
            res = (res * base) % N
        base = (base ** 2) % N
        y //= 2
    return res


def fprobability(k: int) -> float:
    return 1 - (1 / 2 ** k)


def mprobability(k: int) -> float:
    return 1 - (1 / 4 ** k)


# Why is this correctly identifying Carmichael numbers too (if k is not low)?
def fermat(N: int, k: int) -> str:
    if N == 1:
        return "prime"

    for _ in range(k):
        rand = random.randint(1, N - 1)
        if mod_exp(rand, N - 1, N) != 1:
            return "composite"
    return "prime"


def miller_rabin(N: int, k: int) -> str:
    u = N - 1
    t = 0
    while u % 2 == 0:
        u //= 2
        t += 1

    for _ in range(k):
        rand = random.randint(2, N - 1)
        res = mod_exp(rand, u, N)
        if res == 1 or res == N - 1:
            # passes Fermat test
            continue
        for _ in range(t - 1):  # -1 because we've already done round 0 above
            res = mod_exp(res, 2, N)
            if res == N - 1:
                # likely prime
                break
        else:
            return "composite"
    return "prime"


def main(number: int, k: int):
    fermat_call, miller_rabin_call = prime_test(number, k)
    fermat_prob = fprobability(k)
    mr_prob = mprobability(k)

    print(f'Is {number} prime?')
    print(f'Fermat: {fermat_call} (prob={fermat_prob})')
    print(f'Miller-Rabin: {miller_rabin_call} (prob={mr_prob})')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    parser.add_argument('k', type=int)
    args = parser.parse_args()
    main(args.number, args.k)
