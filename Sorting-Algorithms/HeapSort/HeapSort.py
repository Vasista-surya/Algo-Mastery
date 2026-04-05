def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    # build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


def main():
    while True:
        print("\n===== MENU =====")
        print("1. User Input")
        print("2. Test Cases")
        print("3. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            # User Input
            n = int(input("Enter number of elements: "))
            arr = []

            for i in range(n):
                val = int(input(f"Enter element {i+1}: "))
                arr.append(val)

            print("Original Array:", arr)

            heap_sort(arr)

            print("Sorted Array:", arr)

        elif choice == 2:
            # Test Cases
            test_cases = [
                [1, 2, 3, 4, 5],      # Best
                [10, 20, 30, 40],    # Best
                [3, 1, 4, 2, 5],     # Average
                [8, 3, 7, 2, 6],     # Average
                [5, 4, 3, 2, 1],     # Worst
                [9, 7, 5, 3, 1]      # Worst
            ]

            print("\nSelect Test Case (1-6):")
            for i in range(6):
                print(f"{i+1}. Test Case {i+1}")

            t = int(input("Enter choice: "))

            if 1 <= t <= 6:
                arr = test_cases[t - 1].copy()

                print("Original Array:", arr)

                heap_sort(arr)

                print("Sorted Array:", arr)
            else:
                print("Invalid choice!")

        elif choice == 3:
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()