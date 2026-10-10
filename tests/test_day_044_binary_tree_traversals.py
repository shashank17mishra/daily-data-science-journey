import pytest
from learning.dsa.day_044_binary_tree_traversals import TreeNode, BinaryTreeTraversals

@pytest.fixture
def sample_tree():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    return root

def test_empty_tree():
    assert BinaryTreeTraversals.preorder_recursive(None) == []
    assert BinaryTreeTraversals.preorder_iterative(None) == []
    assert BinaryTreeTraversals.inorder_recursive(None) == []
    assert BinaryTreeTraversals.inorder_iterative(None) == []
    assert BinaryTreeTraversals.postorder_recursive(None) == []
    assert BinaryTreeTraversals.postorder_iterative(None) == []
    assert BinaryTreeTraversals.level_order(None) == []

def test_preorder(sample_tree):
    expected = [1, 2, 4, 5, 3]
    assert BinaryTreeTraversals.preorder_recursive(sample_tree) == expected
    assert BinaryTreeTraversals.preorder_iterative(sample_tree) == expected

def test_inorder(sample_tree):
    expected = [4, 2, 5, 1, 3]
    assert BinaryTreeTraversals.inorder_recursive(sample_tree) == expected
    assert BinaryTreeTraversals.inorder_iterative(sample_tree) == expected

def test_postorder(sample_tree):
    expected = [4, 5, 2, 3, 1]
    assert BinaryTreeTraversals.postorder_recursive(sample_tree) == expected
    assert BinaryTreeTraversals.postorder_iterative(sample_tree) == expected

def test_level_order(sample_tree):
    expected = [[1], [2, 3], [4, 5]]
    assert BinaryTreeTraversals.level_order(sample_tree) == expected
