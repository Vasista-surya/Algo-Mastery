class Sorting:
    @staticmethod
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break
        return arr


# Safe input (handles environments where input() is not allowed)
def safe_input(prompt, default):
    try:
        return input(prompt)
    except:
        print(f"\n⚠ Input not supported. Using default value: {default}")
        return str(default)


def user_input_sort():
    n = int(safe_input("Enter number of elements: ", 5))
    arr = []

    for i in range(n):
        val = int(safe_input(f"Enter element {i+1}: ", i + 1))
        arr.append(val)

    print("\nOriginal Array:", arr)
    sorted_arr = Sorting.bubble_sort(arr.copy())
    print("Sorted Array:", sorted_arr)


def test_case_sort():
    test_cases = {
        1: ("Best Case 1 (Already Sorted)", [1, 2, 3, 4, 5]),
        2: ("Best Case 2 (Already Sorted)", [10, 20, 30, 40]),
        3: ("Average Case 1", [3, 1, 4, 2, 5]),
        4: ("Average Case 2", [8, 3, 7, 2, 6]),
        5: ("Worst Case 1 (Reverse Sorted)", [5, 4, 3, 2, 1]),
        6: ("Worst Case 2 (Reverse Sorted)", [9, 7, 5, 3, 1])
    }

    print("\nSelect Test Case:")
    for key, value in test_cases.items():
        print(f"{key}. {value[0]}")

    choice = int(safe_input("Enter your choice (1-6): ", 3))

    if choice in test_cases:
        name, arr = test_cases[choice]
        print(f"\n{name}")
        print("Original Array:", arr)
        sorted_arr = Sorting.bubble_sort(arr.copy())
        print("Sorted Array:", sorted_arr)
    else:
        print("Invalid choice!")


def main():
    while True:
        print("\n===== MENU =====")
        print("1. User Input")
        print("2. Test Case Input")
        print("3. Exit")

        choice = int(safe_input("Enter your choice: ", 2))

        if choice == 1:
            user_input_sort()
        elif choice == 2:
            test_case_sort()
        elif choice == 3:
            print("Exiting program...")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()