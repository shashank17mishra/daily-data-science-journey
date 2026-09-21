# Day 025: Metaclasses & Dunder Methods

## Overview
Implementation of a declarative data model framework using custom metaclasses, descriptors (__get__, __set__, __set_name__), and automated dunder method injection (__repr__, __eq__, __len__, __getitem__, __setitem__).

## Objectives
- Master core concepts of Metaclasses & Dunder Methods.
- Write clean, tested Python code.

## Key Concepts
Metaclasses are the 'classes of classes' in Python. When defining a metaclass by inheriting from `type`, you can intercept class creation (`__new__`), class definition namespace allocation (`__prepare__`), and class instantiation (`__call__`). In this implementation, `ModelMeta` inspects the class attributes during creation, collects descriptor objects (`Field` subclasses), registers the class in a global registry, and automatically generates container dunder methods (`__repr__`, `__eq__`, `__len__`, `__getitem__`, `__setitem__`). Descriptors utilize `__set_name__` to automatically know their attribute names and handle access control (`__get__`) and type/range validation (`__set__`).
