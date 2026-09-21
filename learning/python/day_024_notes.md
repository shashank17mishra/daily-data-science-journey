# Day 024: Memory Management & Garbage Collection

## Overview
Comprehensive exercise and practical implementation of Python Memory Management, Reference Counting, Generational Garbage Collection, Weak References, and Resource Finalizers.

## Objectives
- Master core concepts of CPython memory management and reference counting.
- Understand generational garbage collection and reference cycles.
- Utilize weak references (`weakref`) for non-owning caches and lookups.
- Implement robust resource finalizers using `weakref.finalize` without cyclic retention traps.
- Write clean, tested Python code.

## Key Concepts

### 1. CPython Reference Counting
CPython manages memory primarily through reference counting:
- Every Python object has an internal `ob_refcnt` field.
- When an object is assigned to a name or added to a collection, its reference count increments.
- When a name goes out of scope or is reassigned, its reference count decrements.
- When the reference count reaches zero, memory is freed immediately.

> [!NOTE]
> `sys.getrefcount(obj)` temporarily increments the reference count because the function call passes `obj` as an argument. Similarly, passing `obj` into a wrapper function adds an extra reference for the function parameter frame.

### 2. Reference Cycles and Cyclic Garbage Collection
Reference counting cannot collect cyclic references (e.g. Node A pointing to Node B, and Node B pointing to Node A).
- CPython includes a cyclic garbage collector (`gc` module) that detects unreachable reference cycles.
- It operates using three generations (Generation 0, 1, and 2) based on the heuristic that most objects die young.
- Unreachable cycles in Generation 0 are collected frequently, promoting survivors to older generations.

### 3. Weak References (`weakref`)
Weak references allow referencing an object without preventing it from being deallocated:
- `weakref.ref(obj)` creates a weak reference.
- `weakref.WeakValueDictionary` automatically evicts entries when the values are no longer referenced anywhere else in the application.
- Ideal for memory-sensitive caching and graph structures where parent-child cycles must be broken.

### 4. Safe Resource Finalization (`weakref.finalize`)
- Unlike deprecated `__del__` methods, `weakref.finalize` provides predictable teardown semantics.
- **Critical Trap**: Never pass a bound method of `self` (such as `self._cleanup`) as the finalizer callback. A bound method keeps a strong reference to `self`, preventing the object from ever being collected!
- Instead, use a `@staticmethod` or top-level function callback and pass only the detached resource identifier or data.
