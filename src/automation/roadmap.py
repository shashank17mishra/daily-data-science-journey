import json
from pathlib import Path
from typing import Dict, Any, Optional
from src.automation.utils import get_repo_root, logger, get_ist_now

class RoadmapManager:
    """Manages loading roadmap.json and tracking progress in progress.json."""

    def __init__(self, roadmap_path: Optional[Path] = None, progress_path: Optional[Path] = None):
        repo_root = get_repo_root()
        self.roadmap_path = roadmap_path or (repo_root / "roadmap.json")
        self.progress_path = progress_path or (repo_root / "progress.json")
        self._roadmap_data = None

    def load_roadmap(self) -> list:
        """Loads and returns the roadmap data list from roadmap.json."""
        if not self.roadmap_path.exists():
            raise FileNotFoundError(f"Roadmap file not found at: {self.roadmap_path}")
        with open(self.roadmap_path, "r", encoding="utf-8") as f:
            self._roadmap_data = json.load(f)
        return self._roadmap_data

    def get_task_for_day(self, day: int) -> Optional[Dict[str, Any]]:
        """Finds task definition for given day (1-365)."""
        roadmap = self.load_roadmap()
        for item in roadmap:
            if item.get("day") == day:
                return item
        return None

    def load_progress(self) -> Dict[str, Any]:
        """Loads progress state from progress.json."""
        if not self.progress_path.exists():
            return {
                "completed_days": [],
                "current_day": 1,
                "last_run": None,
                "categories_completed": {}
            }
        try:
            with open(self.progress_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("progress.json corrupted or invalid. Initializing fresh progress state.")
            return {
                "completed_days": [],
                "current_day": 1,
                "last_run": None,
                "categories_completed": {}
            }

    def is_day_completed(self, day: int) -> bool:
        """Checks if given day has already been completed."""
        progress = self.load_progress()
        return day in progress.get("completed_days", [])

    def get_next_uncompleted_day(self) -> Optional[int]:
        """Finds the lowest numbered day in the roadmap that has not been marked completed."""
        progress = self.load_progress()
        completed = set(progress.get("completed_days", []))
        roadmap = self.load_roadmap()
        for item in roadmap:
            day = item.get("day")
            if day and day not in completed:
                return day
        return None

    def mark_day_completed(self, day: int, category: str) -> None:
        """Updates progress.json recording completed day."""
        progress = self.load_progress()
        completed_days = set(progress.get("completed_days", []))
        completed_days.add(day)

        cats = progress.get("categories_completed", {})
        cats[category] = cats.get(category, 0) + 1

        progress["completed_days"] = sorted(list(completed_days))
        progress["current_day"] = day + 1
        progress["last_run"] = get_ist_now().isoformat()
        progress["categories_completed"] = cats

        with open(self.progress_path, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2)
        logger.info(f"Updated progress.json: Day {day} ({category}) marked completed.")
