from typing import List, Tuple

def two_sum_sorted(numbers: List[int], target: int) -> Tuple[int, int]:
    """
    Finds two numbers in a sorted array that add up to a specific target.
    Returns the 1-based indices of the two numbers as a tuple (index1, index2).
    If no solution is found, returns (-1, -1).

    Complexity:
        Time: O(N) - Single pass through the array.
        Space: O(1) - In-place pointer manipulation.
    """
    if len(numbers) < 2:
        return -1, -1

    left, right = 0, len(numbers) - 1
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return left + 1, right + 1
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return -1, -1

def max_area(height: List[int]) -> int:
    """
    Finds two lines that together with the x-axis form a container,
    such that the container contains the most water.
    Returns the maximum area of water.

    Complexity:
        Time: O(N) - Single pass through the array.
        Space: O(1) - In-place pointer manipulation.
    """
    if len(height) < 2:
        return 0

    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        width = right - left
        current_height = min(height[left], height[right])
        current_area = width * current_height
        max_water = max(max_water, current_area)

        # Move the pointer pointing to the shorter line to maximize potential height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water
