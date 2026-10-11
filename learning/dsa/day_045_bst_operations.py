"""Binary Search Tree (BST) implementation and core operations."""

from typing import List, Optional


class TreeNode:
    """Node in a Binary Search Tree."""

    def __init__(self, val: int):
        self.val: int = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BinarySearchTree:
    """Binary Search Tree with standard operations: insert, delete, search, traversals."""

    def __init__(self) -> None:
        self.root: Optional[TreeNode] = None

    def insert(self, val: int) -> None:
        """Insert a value into the BST. Duplicate values are ignored."""
        if self.root is None:
            self.root = TreeNode(val)
            return

        curr = self.root
        while True:
            if val < curr.val:
                if curr.left is None:
                    curr.left = TreeNode(val)
                    break
                curr = curr.left
            elif val > curr.val:
                if curr.right is None:
                    curr.right = TreeNode(val)
                    break
                curr = curr.right
            else:
                # Value already exists; ignore insertion
                break

    def search(self, val: int) -> bool:
        """Search for a value in the BST. Return True if present, False otherwise."""
        curr = self.root
        while curr is not None:
            if val == curr.val:
                return True
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return False

    def delete(self, val: int) -> bool:
        """Delete a value from the BST. Return True if deleted, False if key not found."""
        deleted = False

        def _delete(node: Optional[TreeNode], key: int) -> Optional[TreeNode]:
            nonlocal deleted
            if node is None:
                return None

            if key < node.val:
                node.left = _delete(node.left, key)
            elif key > node.val:
                node.right = _delete(node.right, key)
            else:
                deleted = True
                # Case 1 & 2: 0 or 1 child
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left

                # Case 3: 2 children
                # Find in-order successor (minimum element in right subtree)
                successor = node.right
                while successor.left is not None:
                    successor = successor.left

                node.val = successor.val
                node.right = _delete(node.right, successor.val)

            return node

        self.root = _delete(self.root, val)
        return deleted

    def inorder_traversal(self) -> List[int]:
        """Return in-order traversal of values (left -> root -> right)."""
        result: List[int] = []

        def _inorder(node: Optional[TreeNode]) -> None:
            if node is not None:
                _inorder(node.left)
                result.append(node.val)
                _inorder(node.right)

        _inorder(self.root)
        return result

    def preorder_traversal(self) -> List[int]:
        """Return pre-order traversal of values (root -> left -> right)."""
        result: List[int] = []

        def _preorder(node: Optional[TreeNode]) -> None:
            if node is not None:
                result.append(node.val)
                _preorder(node.left)
                _preorder(node.right)

        _preorder(self.root)
        return result

    def postorder_traversal(self) -> List[int]:
        """Return post-order traversal of values (left -> right -> root)."""
        result: List[int] = []

        def _postorder(node: Optional[TreeNode]) -> None:
            if node is not None:
                _postorder(node.left)
                _postorder(node.right)
                result.append(node.val)

        _postorder(self.root)
        return result

    def get_min(self) -> Optional[int]:
        """Return minimum value in the BST, or None if tree is empty."""
        if self.root is None:
            return None
        curr = self.root
        while curr.left is not None:
            curr = curr.left
        return curr.val

    def get_max(self) -> Optional[int]:
        """Return maximum value in the BST, or None if tree is empty."""
        if self.root is None:
            return None
        curr = self.root
        while curr.right is not None:
            curr = curr.right
        return curr.val

    def is_valid_bst(self) -> bool:
        """Validate if tree strictly obeys binary search tree invariants."""

        def _validate(node: Optional[TreeNode], low: float, high: float) -> bool:
            if node is None:
                return True
            if not (low < node.val < high):
                return False
            return _validate(node.left, low, node.val) and _validate(node.right, node.val, high)

        return _validate(self.root, float("-inf"), float("inf"))
