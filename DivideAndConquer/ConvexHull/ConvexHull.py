"""Andrew's monotone chain hull, NOT a divide-and-conquer hull algorithm.

O(n log n) time, O(n) space. Up to 100000 integer (x,y) pairs with
coordinates in [-10^9,10^9]. Return distinct extreme vertices CCW from
the lexicographically smallest, without repeating the first. Collinear
boundary interiors are omitted; all-collinear input yields its endpoints.
Empty input returns []. Inputs are not changed. Exact integer orientation.
"""


def convex_hull(points):
    if not isinstance(points, (list, tuple)) or len(points) > 100_000:
        raise ValueError("at most 100000 points required")
    for point in points:
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise ValueError("each point must contain two coordinates")
        if any(type(coordinate) is not int or abs(coordinate) > 10**9 for coordinate in point):
            raise ValueError("coordinates must be integers in [-10^9,10^9]")
    # Sort before deduplication: no hash-table worst case in the O(n log n) bound.
    ordered = []
    for point in sorted(map(tuple, points)):
        if not ordered or point != ordered[-1]:
            ordered.append(point)
    if len(ordered) <= 1:
        return ordered

    def cross(origin, a, b):
        return ((a[0] - origin[0]) * (b[1] - origin[1])
                - (a[1] - origin[1]) * (b[0] - origin[0]))

    lower = []
    for point in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(ordered):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def main():
    points = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1), (0, 0), (1, 0)]
    assert convex_hull(points) == [(0, 0), (2, 0), (2, 2), (0, 2)]
    assert convex_hull([]) == []
    assert convex_hull([(1, 1), (1, 1)]) == [(1, 1)]
    assert convex_hull([(2, 2), (0, 0), (1, 1)]) == [(0, 0), (2, 2)]
    big = 10**9
    assert convex_hull([(-big, -big), (big, -big), (big, big), (-big, big)]) == [
        (-big, -big), (big, -big), (big, big), (-big, big)]
    print("Convex hull:", convex_hull(points))


if __name__ == "__main__":
    main()
