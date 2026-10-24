"""Unbounded minimum-coin change (not number of combinations).

O((k+1)*(amount+1)) time, O(amount+1) space. At most 1000 denominations,
each an integer in [1,10^9]; amount is an integer in [0,100000].
Duplicates are harmless. Return -1 when unreachable and 0 for amount zero.
"""


def min_coins(coins, amount):
    if type(amount) is not int or not 0 <= amount <= 100_000:
        raise ValueError("amount must be an integer in [0, 100000]")
    if not isinstance(coins, (list, tuple)) or len(coins) > 1000:
        raise ValueError("at most 1000 denominations required")
    if any(type(coin) is not int or not 1 <= coin <= 10**9 for coin in coins):
        raise ValueError("denominations must be integers in [1, 10^9]")
    unreachable = amount + 1
    best = [0] + [unreachable] * amount
    for coin in coins:
        for subtotal in range(coin, amount + 1):
            best[subtotal] = min(best[subtotal], best[subtotal - coin] + 1)
    return -1 if best[amount] == unreachable else best[amount]


def main():
    assert min_coins([1, 3, 4], 6) == 2
    assert min_coins([2], 3) == -1
    assert min_coins([], 0) == 0
    assert min_coins([], 5) == -1
    assert min_coins([2, 2], 4) == 2
    print("Minimum coins:", min_coins([1, 3, 4], 6))


if __name__ == "__main__":
    main()
