import sys
import argparse
from pathlib import Path
from src.automation.utils import logger, get_current_day, get_repo_root
from src.automation.roadmap import RoadmapManager
from src.automation.gemini import generate_daily_task
from src.automation.generator import TaskGenerator
from src.automation.validator import TaskValidator
from src.automation.git import GitAutomation

def run_daily_automation(
    dry_run: bool = False,
    custom_date: str = None,
    force_day: int = None,
    force_run: bool = False
) -> int:
    """
    Main orchestration routine for daily data science learning task.
    Returns 0 on success, non-zero on failure/exit.
    """
    logger.info("=== Daily Data Science Journey Automation ===")
    if dry_run:
        logger.info("[MODE] DRY RUN ENABLED (No git commit/push will be performed)")

    roadmap_mgr = RoadmapManager()

    # Determine day number
    if force_day:
        current_day = force_day
    elif custom_date:
        current_day = get_current_day(target_date_str=custom_date)
    else:
        sched_day = get_current_day()
        if roadmap_mgr.is_day_completed(sched_day):
            next_day = roadmap_mgr.get_next_uncompleted_day()
            if next_day:
                logger.info(f"Scheduled day (Day {sched_day}) is already completed. Automatically advancing to next uncompleted day: Day {next_day}")
                current_day = next_day
            else:
                current_day = sched_day
        else:
            current_day = sched_day

    logger.info(f"Target Learning Day: Day {current_day}")

    if current_day < 1 or current_day > 365:
        logger.info(f"365-day roadmap completed or target day {current_day} is out of bounds (1-365).")
        return 0

    # Idempotency check
    if roadmap_mgr.is_day_completed(current_day) and not force_run and not dry_run:
        logger.info(f"Today's task (Day {current_day}) is already completed in progress.json.")
        return 0

    # Fetch task specification from roadmap.json
    task_spec = roadmap_mgr.get_task_for_day(current_day)
    if not task_spec:
        logger.error(f"Task definition for Day {current_day} not found in roadmap.json.")
        return 1

    category = task_spec["category"]
    topic = task_spec["topic"]
    difficulty = task_spec["difficulty"]
    objectives = task_spec.get("learning_objectives", [])
    expected_output = task_spec.get("expected_output", "")

    logger.info(f"Roadmap Spec: [{category}] {topic} (Difficulty: {difficulty})")

    # Generate, write, and validate task content with self-healing retry loop
    MAX_ATTEMPTS = 3
    generator = TaskGenerator()
    validator = TaskValidator()
    task_data = None
    written_paths = []
    validation_error = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if written_paths:
            logger.info(f"Rolling back and cleaning up files from previous failed attempt {attempt - 1}...")
            generator.cleanup_files(written_paths)
            written_paths = []

        logger.info(f"Task generation & validation attempt {attempt}/{MAX_ATTEMPTS} for Day {current_day}...")
        try:
            task_data = generate_daily_task(
                day=current_day,
                category=category,
                topic=topic,
                difficulty=difficulty,
                learning_objectives=objectives,
                expected_output=expected_output,
                feedback=validation_error if attempt > 1 else None
            )
            written_paths = generator.write_task_files(task_data)
            validator.validate_all(task_data, written_paths)
            validation_error = None
            logger.info(f"Attempt {attempt} passed all validations successfully!")
            break
        except Exception as e:
            validation_error = str(e)
            logger.warning(f"Attempt {attempt} failed: {validation_error}")
            if attempt == MAX_ATTEMPTS:
                logger.error(f"All {MAX_ATTEMPTS} generation/validation attempts failed for Day {current_day}.")
                if written_paths:
                    generator.cleanup_files(written_paths)
                logger.error("Aborting git commit due to validation failure.")
                return 1

    # Update progress state
    if not dry_run:
        roadmap_mgr.mark_day_completed(current_day, category)

    # Git operations
    if dry_run:
        logger.info("[DRY-RUN COMPLETE] Files created and validated successfully without git commit.")
        return 0

    git_auto = GitAutomation()
    if not git_auto.check_git_installed():
        logger.error("Git is not available on system path.")
        return 1

    try:
        commits_count = git_auto.create_daily_commits(
            day=current_day,
            topic=topic,
            category=category,
            written_paths=written_paths
        )
        logger.info(f"Successfully created {commits_count} commits for Day {current_day}.")
        git_auto.push()
    except Exception as e:
        logger.error(f"Git automation failed: {e}")
        return 1

    logger.info(f"=== Successfully finished Day {current_day} automation! ===")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Automated Daily Data Science Journey CLI")
    parser.add_argument("--dry-run", action="store_true", help="Run generation and validation without committing or pushing.")
    parser.add_argument("--date", type=str, default=None, help="Target date in YYYY-MM-DD format.")
    parser.add_argument("--day", type=int, default=None, help="Force specific day number (1-365).")
    parser.add_argument("--force", action="store_true", help="Force task execution even if day is marked completed.")

    args = parser.parse_args()

    exit_code = run_daily_automation(
        dry_run=args.dry_run,
        custom_date=args.date,
        force_day=args.day,
        force_run=args.force
    )
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
