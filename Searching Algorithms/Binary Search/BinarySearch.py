def binary_search(arr, key):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return -1


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

            arr.sort()  # IMPORTANT
            print("Sorted Array:", arr)

            key = int(input("Enter element to search: "))

            result = binary_search(arr, key)

            if result != -1:
                print("Element found at index:", result)
            else:
                print("Element not found")

        elif choice == 2:
            test_cases = [
                [1, 2, 3, 4, 5],
                [10, 20, 30, 40],
                [3, 1, 4, 2, 5],
                [8, 3, 7, 2, 6],
                [5, 4, 3, 2, 1],
                [9, 7, 5, 3, 1]
            ]

            print("\nSelect Test Case (1-6):")
            for i in range(6):
                print(f"{i+1}. Test Case {i+1}")

            t = int(input("Enter choice: "))

            if 1 <= t <= 6:
                arr = sorted(test_cases[t - 1])
                print("Sorted Array:", arr)

                key = int(input("Enter element to search: "))

                result = binary_search(arr, key)

                if result != -1:
                    print("Element found at index:", result)
                else:
                    print("Element not found")
            else:
                print("Invalid choice!")

        elif choice == 3:
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()