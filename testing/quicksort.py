n = [3, 1, 4, 2]


def quicksort(n):
    if len(n) <= 1:
        return n
    pivot = n[len(n) // 2]
    left = [x for x in n if x < pivot]
    middle = [x for x in n if x == pivot]
    right = [x for x in n if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def recsum(i):
    if i < 1:
        return i
    return recsum(i + 1)


print(recsum(2))
print(quicksort(n))
