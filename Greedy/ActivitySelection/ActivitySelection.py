"""Maximum-cardinality compatible activities, O(N log N) time/O(N) space.

Activities are integer (start, finish) pairs with start < finish; negative
times are valid. Touching endpoints are compatible (next start >= finish).
Return original indices in scheduled order, ties by (finish, start, index).
Empty -> []; invalid intervals raise ValueError. Input is not modified.
"""


def activity_selection(activities):
    ordered = []
    for index, (start, finish) in enumerate(activities):
        if type(start) is not int or type(finish) is not int or start >= finish:
            raise ValueError("integer times with start < finish required")
        ordered.append((finish, start, index))
    ordered.sort()
    selected = []
    last_finish = None
    for finish, start, index in ordered:
        if last_finish is None or start >= last_finish:
            selected.append(index)
            last_finish = finish
    return selected


if __name__ == "__main__":
    result = activity_selection([(5, 9), (1, 2), (3, 4), (0, 6), (5, 7), (8, 9)])
    assert result == [1, 2, 4, 5]
    assert activity_selection([]) == []
    assert activity_selection([(-4, -2), (-2, 0)]) == [0, 1]
    try:
        activity_selection([(2, 2)])
    except ValueError:
        pass
    else:
        raise AssertionError("empty interval accepted")
    print("Selected indices:", result)
