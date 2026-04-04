def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        # swap
        arr[i], arr[min_index] = arr[min_index], arr[i]


def print_array(arr):
    print(arr)


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

            selection_sort(arr)

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

            print("\nSelect Test Case (1-6): ")
            for i in range(6):
                print(f"{i+1}. Test Case {i+1}")

            t = int(input("Enter choice: "))

            if 1 <= t <= 6:
                arr = test_cases[t - 1].copy()

                print("Original Array:", arr)

                selection_sort(arr)

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