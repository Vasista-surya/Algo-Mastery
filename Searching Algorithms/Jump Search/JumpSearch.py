import math

def jump_search(arr, key):
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0

    # finding block
    while prev < n and arr[min(step, n) - 1] < key:
        prev = step
        step += int(math.sqrt(n))

        if prev >= n:
            return -1

    # linear search in block
    for i in range(prev, min(step, n)):
        if arr[i] == key:
            return i

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
            arr = sorted([int(input(f"Enter element {i+1}: ")) for i in range(n)])

            print("Sorted:", arr)

            key = int(input("Enter key: "))
            res = jump_search(arr, key)

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
                res = jump_search(arr, key)

                print("Found at index:" if res != -1 else "Not found", res)

        elif choice == 3:
            break


main()