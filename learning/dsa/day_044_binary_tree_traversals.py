from typing import List, Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class BinaryTreeTraversals:
    @staticmethod
    def preorder_recursive(root: Optional[TreeNode]) -> List[int]:
        result = []
        def traverse(node: Optional[TreeNode]):
            if not node:
                return
            result.append(node.val)
            traverse(node.left)
            traverse(node.right)
        traverse(root)
        return result

    @staticmethod
    def preorder_iterative(root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        result = []
        stack = [root]
        while stack:
            node = stack.pop()
            result.append(node.val)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result

    @staticmethod
    def inorder_recursive(root: Optional[TreeNode]) -> List[int]:
        result = []
        def traverse(node: Optional[TreeNode]):
            if not node:
                return
            traverse(node.left)
            result.append(node.val)
            traverse(node.right)
        traverse(root)
        return result

    @staticmethod
    def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
        result = []
        stack = []
        curr = root
        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            result.append(curr.val)
            curr = curr.right
        return result

    @staticmethod
    def postorder_recursive(root: Optional[TreeNode]) -> List[int]:
        result = []
        def traverse(node: Optional[TreeNode]):
            if not node:
                return
            traverse(node.left)
            traverse(node.right)
            result.append(node.val)
        traverse(root)
        return result

    @staticmethod
    def postorder_iterative(root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        result = []
        stack = [root]
        while stack:
            node = stack.pop()
            result.append(node.val)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return result[::-1]

    @staticmethod
    def level_order(root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        from collections import deque
        result = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            current_level = []
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(current_level)
        return result
