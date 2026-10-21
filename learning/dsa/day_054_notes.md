# Day 054: Bit Manipulation Operations

## Overview
This exercise focuses on fundamental bit manipulation techniques, which are crucial for optimizing algorithms, especially in competitive programming and low-level systems. You will implement functions to count set bits, determine if a number is a power of two, and find unique numbers in arrays where other numbers appear a fixed number of times (twice or thrice). The challenge includes handling edge cases and negative numbers correctly, particularly for the 'find single number thrice' problem, which requires careful consideration of two's complement representation.

## Objectives
- Understand algorithmic mechanics of Bit Manipulation Operations.
- Implement unit tests for edge cases.

## Key Concepts
Bit manipulation involves operating on individual bits of a number. It's a powerful technique for optimizing code, especially in scenarios requiring high performance or memory efficiency.

1.  **`count_set_bits(n)`**: This function uses Brian Kernighan's algorithm. The expression `n & (n - 1)` clears the least significant set bit in `n`. By repeatedly applying this operation and counting how many times it's performed until `n` becomes 0, we effectively count all set bits. This method is efficient as it runs in `O(k)` time, where `k` is the number of set bits, rather than `O(log n)` (number of bits).

2.  **`is_power_of_two(n)`**: A positive integer `n` is a power of two if and only if its binary representation has exactly one set bit. For example, `4` is `0b100`, `8` is `0b1000`. When you subtract 1 from a power of two, all trailing zeros become ones, and the single set bit becomes zero (e.g., `8 (0b1000) - 1 = 7 (0b0111)`). Performing a bitwise AND operation `n & (n - 1)` will result in 0 if `n` is a power of two. The `n > 0` check handles the edge case of 0, which is not considered a power of two.

3.  **`find_single_number_twice(nums)`**: This problem leverages the properties of the XOR (`^`) operator: `x ^ x = 0` and `x ^ 0 = x`. If you XOR all numbers in an array where every number appears twice except one, all pairs will cancel each other out (resulting in 0), leaving only the unique number. This is a very efficient `O(N)` time and `O(1)` space solution.

4.  **`find_single_number_thrice(nums)`**: This is a more complex variant. The core idea is to count the occurrences of each bit position across all numbers. Since every number except one appears three times, the sum of bits at any given position `i` (across all numbers) will be `3k + 1` if the single number has its `i`-th bit set, or `3k` if it doesn't. Therefore, `(bit_sum % 3)` will reveal the `i`-th bit of the single number. We iterate through all 32 bits (assuming 32-bit integers, a common constraint in such problems) and reconstruct the result. A critical aspect for handling negative numbers is the final conversion: if the most significant bit (31st bit for 32-bit) of the reconstructed `result` is set, it means the number is negative in two's complement. We convert it from its unsigned 32-bit representation to its signed equivalent by subtracting `2^32` (i.e., `1 << num_bits`). This ensures correct interpretation of negative numbers like -1 or -2.
