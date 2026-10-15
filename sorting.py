"""Обе сортировки возвращают новый список, не изменяя исходные данные."""


def bubble_sort(values):
    result = list(values)
    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
        if not swapped:
            break
    return result


def quick_sort(values):
    """Итеративная быстрая сортировка с разбиением на три части."""
    result = list(values)
    stack = [(0, len(result) - 1)]
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        pivot = result[(low + high) // 2]
        left, current, right = low, low, high
        while current <= right:
            if result[current] < pivot:
                result[left], result[current] = result[current], result[left]
                left += 1
                current += 1
            elif result[current] > pivot:
                result[current], result[right] = result[right], result[current]
                right -= 1
            else:
                current += 1
        stack.extend(((low, left - 1), (right + 1, high)))
    return result
