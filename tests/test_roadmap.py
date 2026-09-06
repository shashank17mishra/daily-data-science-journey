import json
import pytest
from pathlib import Path
from src.automation.utils import get_current_day
from src.automation.roadmap import RoadmapManager

def test_get_current_day_calculation():
    # If start_date = 2026-09-07 and target_date = 2026-09-07 -> day 1
    day1 = get_current_day(start_date_str="2026-09-07", target_date_str="2026-09-07")
    assert day1 == 1

    # Day 10
    day10 = get_current_day(start_date_str="2026-09-07", target_date_str="2026-09-16")
    assert day10 == 10

def test_roadmap_manager_load(tmp_path):
    roadmap_file = tmp_path / "roadmap.json"
    roadmap_data = [
        {"day": 1, "category": "python", "topic": "Variables", "difficulty": "Beginner"}
    ]
    with open(roadmap_file, "w", encoding="utf-8") as f:
        json.dump(roadmap_data, f)

    mgr = RoadmapManager(roadmap_path=roadmap_file)
    data = mgr.load_roadmap()
    assert len(data) == 1
    assert mgr.get_task_for_day(1)["topic"] == "Variables"

def test_roadmap_progress_tracking(tmp_path):
    roadmap_file = tmp_path / "roadmap.json"
    progress_file = tmp_path / "progress.json"

    with open(roadmap_file, "w") as f:
        json.dump([{"day": 1, "category": "python"}], f)

    mgr = RoadmapManager(roadmap_path=roadmap_file, progress_path=progress_file)
    assert not mgr.is_day_completed(1)

    mgr.mark_day_completed(1, "python")
    assert mgr.is_day_completed(1)
