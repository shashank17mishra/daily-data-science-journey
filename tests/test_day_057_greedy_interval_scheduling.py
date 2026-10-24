import pytest
from learning.dsa.day_057_greedy_interval_scheduling import (
    Interval,
    select_max_non_overlapping,
    min_removals_to_avoid_overlap,
    min_resources_required,
)


def test_interval_dataclass_validation():
    inv = Interval(1.0, 5.0, id="task1")
    assert inv.start == 1.0
    assert inv.end == 5.0
    assert inv.duration == 4.0
    assert inv.id == "task1"

    with pytest.raises(ValueError, match="must be strictly less than"):
        Interval(5.0, 5.0)

    with pytest.raises(ValueError, match="must be strictly less than"):
        Interval(10.0, 2.0)


def test_interval_overlaps():
    a = Interval(1.0, 3.0)
    b = Interval(2.0, 4.0)
    c = Interval(3.0, 5.0)

    assert a.overlaps(b) is True
    assert b.overlaps(a) is True
    assert a.overlaps(c) is False


def test_select_max_non_overlapping_empty():
    assert select_max_non_overlapping([]) == []


def test_select_max_non_overlapping_classic():
    intervals = [
        Interval(1, 4, id="A"),
        Interval(3, 5, id="B"),
        Interval(0, 6, id="C"),
        Interval(5, 7, id="D"),
        Interval(3, 9, id="E"),
        Interval(5, 9, id="F"),
        Interval(6, 10, id="G"),
        Interval(8, 11, id="H"),
        Interval(8, 12, id="I"),
        Interval(2, 14, id="J"),
        Interval(12, 16, id="K"),
    ]
    selected = select_max_non_overlapping(intervals)
    selected_ids = [inv.id for inv in selected]

    assert len(selected) == 4
    assert selected_ids == ["A", "D", "H", "K"]


def test_select_max_non_overlapping_boundary_touch():
    intervals = [
        Interval(1, 2, id="1"),
        Interval(2, 3, id="2"),
        Interval(3, 4, id="3"),
    ]
    selected = select_max_non_overlapping(intervals)
    assert len(selected) == 3


def test_min_removals_to_avoid_overlap():
    intervals = [
        Interval(1, 2),
        Interval(2, 3),
        Interval(1, 3),
        Interval(3, 4),
    ]
    assert min_removals_to_avoid_overlap(intervals) == 1
    assert min_removals_to_avoid_overlap([]) == 0


def test_min_resources_required_empty():
    count, rooms = min_resources_required([])
    assert count == 0
    assert rooms == []


def test_min_resources_required():
    intervals = [
        Interval(0, 30, id="m1"),
        Interval(5, 10, id="m2"),
        Interval(15, 20, id="m3"),
    ]
    count, rooms = min_resources_required(intervals)
    assert count == 2
    assert len(rooms) == 2

    for room in rooms:
        sorted_room = sorted(room, key=lambda x: x.start)
        for i in range(len(sorted_room) - 1):
            assert not sorted_room[i].overlaps(sorted_room[i + 1])


def test_min_resources_required_all_overlapping():
    intervals = [
        Interval(1, 10, id="1"),
        Interval(2, 9, id="2"),
        Interval(3, 8, id="3"),
    ]
    count, rooms = min_resources_required(intervals)
    assert count == 3
