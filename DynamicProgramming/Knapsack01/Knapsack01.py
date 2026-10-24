"""0/1 knapsack maximum value, O((n+1)*(capacity+1)) time, O(capacity+1) space.

At most 1000 items; capacity 0..100000; integer weights/values 0..10^9.
Each item is used at most once, including zero-weight items. Empty input
returns zero. Inputs are not mutated; invalid inputs raise ValueError.
"""


def knapsack_01(weights, values, capacity):
    if type(capacity) is not int or not 0 <= capacity <= 100_000:
        raise ValueError("capacity must be an integer in [0, 100000]")
    if not isinstance(weights, (list, tuple)) or not isinstance(values, (list, tuple)):
        raise ValueError("weights and values must be lists or tuples")
    if len(weights) != len(values) or len(weights) > 1000:
        raise ValueError("equal lengths of at most 1000 required")
    if any(type(x) is not int or not 0 <= x <= 10**9
           for sequence in (weights, values) for x in sequence):
        raise ValueError("weights and values must be integers in [0, 10^9]")
    best = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        # Descending capacities prohibit reuse; weight=0 updates each slot once.
        for room in range(capacity, weight - 1, -1):
            best[room] = max(best[room], best[room - weight] + value)
    return best[capacity]


def main():
    assert knapsack_01([10, 20, 30], [60, 100, 120], 50) == 220
    assert knapsack_01([0, 0, 1], [5, 7, 100], 0) == 12
    assert knapsack_01([], [], 10) == 0
    assert knapsack_01([2], [3], 4) == 3
    print("Maximum value:", knapsack_01([10, 20, 30], [60, 100, 120], 50))


if __name__ == "__main__":
    main()
