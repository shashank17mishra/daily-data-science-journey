from typing import List

def lomuto_partition(arr: List[int], low: int, high: int) -> int:
    """
    Partitions the array using Lomuto's partitioning scheme.
    Uses the last element as the pivot.
    
    Args:
        arr: The list of integers to partition.
        low: Starting index of the partition.
        high: Ending index of the partition.
        
    Returns:
        The index of the pivot element after partitioning.
    """
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def hoare_partition(arr: List[int], low: int, high: int) -> int:
    """
    Partitions the array using Hoare's partitioning scheme.
    Uses the first element as the pivot.
    
    Args:
        arr: The list of integers to partition.
        low: Starting index of the partition.
        high: Ending index of the partition.
        
    Returns:
        The boundary index dividing the two partitioned halves.
    """
    pivot = arr[low]
    i = low - 1
    j = high + 1
    
    while True:
        while True:
            i += 1
            if arr[i] >= pivot:
                break
        while True:
            j -= 1
            if arr[j] <= pivot:
                break
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]

def quick_sort(arr: List[int], low: int = 0, high: int = None, scheme: str = "lomuto") -> List[int]:
    """
    Sorts an array in-place using the Quick Sort algorithm.
    
    Args:
        arr: The list of integers to sort.
        low: Starting index for sorting.
        high: Ending index for sorting.
        scheme: Partitioning scheme to use ('lomuto' or 'hoare').
        
    Returns:
        The sorted list (modified in-place).
    """
    if high is None:
        high = len(arr) - 1
        
    if low < high:
        if scheme.lower() == "lomuto":
            p = lomuto_partition(arr, low, high)
            quick_sort(arr, low, p - 1, scheme)
            quick_sort(arr, p + 1, high, scheme)
        elif scheme.lower() == "hoare":
            p = hoare_partition(arr, low, high)
            quick_sort(arr, low, p, scheme)
            quick_sort(arr, p + 1, high, scheme)
        else:
            raise ValueError(f"Unknown partitioning scheme: {scheme}")
            
    return arr
