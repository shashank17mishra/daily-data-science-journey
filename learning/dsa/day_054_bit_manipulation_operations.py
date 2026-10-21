import math

def count_set_bits(n: int) -> int:
    """
    Counts the number of set (1) bits in the binary representation of a non-negative integer.

    Args:
        n: A non-negative integer.

    Returns:
        The number of set bits.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")

    count = 0
    while n > 0:
        n &= (n - 1)  # Brian Kernighan's algorithm: clears the least significant set bit
        count += 1
    return count

def is_power_of_two(n: int) -> bool:
    """
    Checks if a given positive integer is a power of two.
    A number is a power of two if and only if it has exactly one set bit in its
    binary representation. This can be checked efficiently using the property
    that for a power of two 'n', 'n & (n - 1)' will be 0.

    Args:
        n: A positive integer.

    Returns:
        True if n is a power of two, False otherwise.
    """
    return n > 0 and (n & (n - 1)) == 0

def find_single_number_twice(nums: list[int]) -> int:
    """
    Finds the single number that appears only once in an array where every other
    number appears exactly twice.

    This solution uses the XOR bitwise operation. The XOR of a number with itself
    is 0 (a ^ a = 0), and XOR of a number with 0 is the number itself (a ^ 0 = a).
    If we XOR all numbers in the array, all numbers appearing twice will cancel
    each other out, leaving only the single number.

    Args:
        nums: A list of integers where one number appears once and others twice.

    Returns:
        The single number that appears only once.
    """
    single_num = 0
    for num in nums:
        single_num ^= num
    return single_num

def find_single_number_thrice(nums: list[int]) -> int:
    """
    Finds the single number that appears only once in an array where every other
    number appears exactly three times. Handles both positive and negative integers.

    This solution uses bit manipulation. For each bit position (0 to 31 for 32-bit integers),
    it counts how many numbers have that bit set. Since every number except one appears
    three times, the sum of bits at any position modulo 3 will reveal the bit of the
    single number.

    Args:
        nums: A list of integers where one number appears once and others thrice.

    Returns:
        The single number that appears only once.
    """
    result = 0
    # Assuming 32-bit integers for the problem context, common in competitive programming
    # and for handling negative numbers with two's complement.
    # Python integers have arbitrary precision, but the problem implies a fixed bit width
    # for the "thrice" property to work with negative numbers.
    num_bits = 32

    for i in range(num_bits):
        bit_sum = 0
        for num in nums:
            # Check the i-th bit of each number.
            # (num >> i) & 1 correctly extracts the i-th bit for both positive and negative
            # numbers in a two's complement context in Python.
            if (num >> i) & 1:
                bit_sum += 1

        # If the sum of bits at position 'i' is not a multiple of 3,
        # it means the single number has its i-th bit set.
        if bit_sum % 3 != 0:
            result |= (1 << i)

    # After constructing the result from the bits, we need to handle
    # the case where the single number is negative.
    # If the 31st bit (MSB for 32-bit signed int) is set, the number is negative.
    # The 'result' currently holds the unsigned 32-bit representation.
    # Convert it to signed 32-bit if necessary.
    if result >= (1 << (num_bits - 1)):  # Check if MSB is set
        result -= (1 << num_bits)

    return result
