def bucket_sort(arr):
    if len(arr) == 0:
        return arr

    max_val = max(arr)
    bucket_count = len(arr)

    buckets = [[] for _ in range(bucket_count)]

    # distribute elements into buckets
    for num in arr:
        index = int(num * bucket_count / (max_val + 1))
        buckets[index].append(num)

    # sort individual buckets
    for bucket in buckets:
        bucket.sort()

    # merge buckets
    k = 0
    for bucket in buckets:
        for num in bucket:
            arr[k] = num
            k += 1


def main():
    while True:
        print("\n===== MENU =====")
        print("1. User Input")
        print("2. Test Cases")
        print("3. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            n = int(input("Enter number of elements: "))
            arr = [int(input(f"Enter element {i+1}: ")) for i in range(n)]

            print("Original:", arr)
            bucket_sort(arr)
            print("Sorted:", arr)

        elif choice == 2:
            test_cases = [
                [1, 2, 3, 4, 5],
                [10, 20, 30, 40],
                [3, 1, 4, 2, 5],
                [8, 3, 7, 2, 6],
                [5, 4, 3, 2, 1],
                [9, 7, 5, 3, 1]
            ]

            for i in range(6):
                print(f"{i+1}. Test Case {i+1}")

            t = int(input("Enter choice: "))

            if 1 <= t <= 6:
                arr = test_cases[t - 1].copy()
                print("Original:", arr)
                bucket_sort(arr)
                print("Sorted:", arr)
            else:
                print("Invalid choice!")

        elif choice == 3:
            break

main()