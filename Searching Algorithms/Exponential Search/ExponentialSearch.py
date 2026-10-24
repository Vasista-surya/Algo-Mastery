def binary_search(arr, left, right, key):
    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def exponential_search(arr, key):
    n = len(arr)
    if n == 0:
        return -1

    if arr[0] == key:
        return 0

    i = 1
    while i < n and arr[i] <= key:
        i *= 2

    return binary_search(arr, i // 2, min(i, n - 1), key)


def main():
    while True:
        print("\n===== MENU =====")
        print("1. User Input")
        print("2. Test Cases")
        print("3. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            n = int(input("Enter number of elements: "))
            arr = sorted([int(input(f"Enter element {i+1}: ")) for i in range(n)])

            print("Sorted:", arr)

            key = int(input("Enter key: "))
            res = exponential_search(arr, key)

            print("Found at index:" if res != -1 else "Not found", res)

        elif choice == 2:
            test = [
                [1,2,3,4,5],
                [10,20,30,40],
                [3,1,4,2,5],
                [8,3,7,2,6],
                [5,4,3,2,1],
                [9,7,5,3,1]
            ]

            for i in range(6):
                print(f"{i+1}. Test Case {i+1}")

            t = int(input("Enter choice: "))

            if 1 <= t <= 6:
                arr = sorted(test[t-1])
                print("Sorted:", arr)

                key = int(input("Enter key: "))
                res = exponential_search(arr, key)

                print("Found at index:" if res != -1 else "Not found", res)

        elif choice == 3:
            break


if __name__ == "__main__":
    main()
