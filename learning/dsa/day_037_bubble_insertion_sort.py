from typing import List, Dict, Any, TypeVar, Union

T = TypeVar('T', int, float, str)


def bubble_sort(arr: List[T]) -> Dict[str, Any]:
    """
    Sorts a list in-place using the Bubble Sort algorithm with an early-exit optimization.
    Tracks and returns the number of comparisons and swaps performed.

    Args:
        arr: A list of comparable elements.

    Returns:
        A dictionary containing:
            - 'sorted_list': The sorted list (modified in-place).
            - 'comparisons': Total number of element comparisons.
            - 'swaps': Total number of element swaps.
    """
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        # If no two elements were swapped by inner loop, then break
        if not swapped:
            break

    return {
        "sorted_list": arr,
        "comparisons": comparisons,
        "swaps": swaps
    }


def insertion_sort(arr: List[T]) -> Dict[str, Any]:
    """
    Sorts a list in-place using the Insertion Sort algorithm.
    Tracks and returns the number of comparisons and shifts performed.

    Args:
        arr: A list of comparable elements.

    Returns:
        A dictionary containing:
            - 'sorted_list': The sorted list (modified in-place).
            - 'comparisons': Total number of element comparisons.
            - 'shifts': Total number of element shifts (movements).
    """
    n = len(arr)
    comparisons = 0
    shifts = 0

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            else:
                break
        arr[j + 1] = key

    return {
        "sorted_list": arr,
        "comparisons": comparisons,
        "shifts": shifts
    }
