# Day 043: Queue & Monotonic Deque

## Overview
Implementation of a Monotonic Queue (Max Queue) using a standard queue and a monotonic decreasing deque to support push, pop, and max operations in O(1) amortized time. Includes an application to solve the classic Sliding Window Maximum problem.

## Objectives
- Understand the mechanics of a Monotonic Deque and how it maintains order.
- Implement a Monotonic Queue supporting O(1) amortized push, pop, and max operations.
- Apply the Monotonic Queue to solve the Sliding Window Maximum problem efficiently.
- Write robust unit tests covering edge cases like empty inputs, single element windows, and large window sizes.

## Key Concepts
A Monotonic Deque is a double-ended queue that maintains its elements in a strictly increasing or decreasing order. In this exercise, we implement a Monotonic Queue (Max Queue) using a standard FIFO queue alongside a decreasing monotonic deque. When pushing an element, we pop all elements from the back of the deque that are smaller than the new element, ensuring the deque remains sorted in descending order. This guarantees that the front of the deque always contains the maximum element of the queue. This structure allows us to solve the Sliding Window Maximum problem in O(N) time complexity, as each element is pushed and popped from the deque at most once.
