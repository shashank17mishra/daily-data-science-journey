import pytest
from learning.dsa.day_045_bst_operations import BinarySearchTree, TreeNode


@pytest.fixture
def empty_bst():
    return BinarySearchTree()


@pytest.fixture
def sample_bst():
    # Structure:
    #        50
    #      /    \
    #    30      70
    #   /  \    /  \
    #  20  40  60  80
    bst = BinarySearchTree()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(val)
    return bst


def test_empty_bst_operations(empty_bst):
    assert empty_bst.root is None
    assert empty_bst.get_min() is None
    assert empty_bst.get_max() is None
    assert empty_bst.search(10) is False
    assert empty_bst.delete(10) is False
    assert empty_bst.inorder_traversal() == []
    assert empty_bst.preorder_traversal() == []
    assert empty_bst.postorder_traversal() == []
    assert empty_bst.is_valid_bst() is True


def test_insert_and_traversals(sample_bst):
    assert sample_bst.inorder_traversal() == [20, 30, 40, 50, 60, 70, 80]
    assert sample_bst.preorder_traversal() == [50, 30, 20, 40, 70, 60, 80]
    assert sample_bst.postorder_traversal() == [20, 40, 30, 60, 80, 70, 50]


def test_duplicate_insert(sample_bst):
    sample_bst.insert(50)
    sample_bst.insert(30)
    assert sample_bst.inorder_traversal() == [20, 30, 40, 50, 60, 70, 80]


def test_search(sample_bst):
    assert sample_bst.search(50) is True
    assert sample_bst.search(20) is True
    assert sample_bst.search(80) is True
    assert sample_bst.search(100) is False
    assert sample_bst.search(10) is False


def test_get_min_max(sample_bst):
    assert sample_bst.get_min() == 20
    assert sample_bst.get_max() == 80


def test_delete_leaf_node(sample_bst):
    assert sample_bst.delete(20) is True
    assert sample_bst.search(20) is False
    assert sample_bst.inorder_traversal() == [30, 40, 50, 60, 70, 80]
    assert sample_bst.is_valid_bst() is True


def test_delete_node_with_one_child():
    bst = BinarySearchTree()
    for val in [50, 30, 20]:
        bst.insert(val)
    assert bst.delete(30) is True
    assert bst.inorder_traversal() == [20, 50]
    assert bst.search(30) is False
    assert bst.is_valid_bst() is True


def test_delete_node_with_two_children(sample_bst):
    assert sample_bst.delete(30) is True
    assert sample_bst.search(30) is False
    assert sample_bst.inorder_traversal() == [20, 40, 50, 60, 70, 80]
    assert sample_bst.is_valid_bst() is True


def test_delete_root_node(sample_bst):
    assert sample_bst.delete(50) is True
    assert sample_bst.search(50) is False
    assert sample_bst.inorder_traversal() == [20, 30, 40, 60, 70, 80]
    assert sample_bst.is_valid_bst() is True


def test_delete_non_existent_key(sample_bst):
    assert sample_bst.delete(999) is False
    assert sample_bst.inorder_traversal() == [20, 30, 40, 50, 60, 70, 80]


def test_is_valid_bst_tampered():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    assert bst.is_valid_bst() is True

    # Manually break BST invariant
    assert bst.root is not None and bst.root.left is not None
    bst.root.left.right = TreeNode(100)
    assert bst.is_valid_bst() is False
