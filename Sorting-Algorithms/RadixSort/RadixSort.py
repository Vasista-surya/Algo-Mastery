def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10


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
            radix_sort(arr)
            print("Sorted:", arr)

        elif choice == 2:
            test_cases = [
                [1, 2, 3, 4, 5],
                [10, 20, 30, 40],
                [170, 45, 75, 90, 802],
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
                radix_sort(arr)
                print("Sorted:", arr)
            else:
                print("Invalid choice!")

        elif choice == 3:
            break

main()