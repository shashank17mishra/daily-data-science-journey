import pytest
from learning.dsa.day_040_singly_linked_list import SinglyLinkedList, Node


def test_node_creation():
    node = Node(10)
    assert node.value == 10
    assert node.next is None
    assert repr(node) == "Node(10)"


def test_empty_list():
    sll = SinglyLinkedList()
    assert len(sll) == 0
    assert sll.is_empty()
    assert sll.to_list() == []


def test_append_and_prepend():
    sll = SinglyLinkedList()
    sll.append(2)
    sll.append(3)
    sll.prepend(1)
    assert sll.to_list() == [1, 2, 3]
    assert len(sll) == 3
    assert not sll.is_empty()


def test_insert_at():
    sll = SinglyLinkedList()
    sll.insert_at(0, 10)
    sll.insert_at(1, 30)
    sll.insert_at(1, 20)
    assert sll.to_list() == [10, 20, 30]

    with pytest.raises(IndexError):
        sll.insert_at(-1, 5)
    with pytest.raises(IndexError):
        sll.insert_at(5, 5)


def test_delete_value():
    sll = SinglyLinkedList()
    for val in [10, 20, 30, 20]:
        sll.append(val)

    assert sll.delete_value(20) is True
    assert sll.to_list() == [10, 30, 20]

    assert sll.delete_value(10) is True
    assert sll.to_list() == [30, 20]

    assert sll.delete_value(99) is False
    assert sll.to_list() == [30, 20]

    assert sll.delete_value(20) is True
    assert sll.delete_value(30) is True
    assert sll.to_list() == []
    assert sll.delete_value(10) is False


def test_delete_at():
    sll = SinglyLinkedList()
    for val in [10, 20, 30, 40]:
        sll.append(val)

    val = sll.delete_at(1)
    assert val == 20
    assert sll.to_list() == [10, 30, 40]

    val = sll.delete_at(0)
    assert val == 10
    assert sll.to_list() == [30, 40]

    val = sll.delete_at(1)
    assert val == 40
    assert sll.to_list() == [30]

    with pytest.raises(IndexError):
        sll.delete_at(1)
    with pytest.raises(IndexError):
        sll.delete_at(-1)


def test_find():
    sll = SinglyLinkedList()
    for val in ["a", "b", "c"]:
        sll.append(val)

    assert sll.find("a") == 0
    assert sll.find("b") == 1
    assert sll.find("c") == 2
    assert sll.find("z") == -1


def test_reverse():
    sll = SinglyLinkedList()
    sll.reverse()
    assert sll.to_list() == []

    sll.append(1)
    sll.reverse()
    assert sll.to_list() == [1]

    sll.append(2)
    sll.append(3)
    sll.append(4)
    sll.reverse()
    assert sll.to_list() == [4, 3, 2, 1]
