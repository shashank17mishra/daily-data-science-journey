import pytest
from pathlib import Path
from src.automation.git import GitAutomation

def test_git_commit_generic_message_rejection():
    git_auto = GitAutomation()
    with pytest.raises(ValueError, match="Invalid or generic commit message"):
        git_auto.commit("update")

    with pytest.raises(ValueError, match="Invalid or generic commit message"):
        git_auto.commit("test")

def test_git_stage_and_commit_generic_rejection():
    git_auto = GitAutomation()
    with pytest.raises(ValueError, match="Invalid or generic commit message"):
        git_auto.stage_and_commit([Path("dummy.py")], "update")

def test_git_ensure_identity(monkeypatch):
    git_auto = GitAutomation()
    executed_cmds = []
    git_auto._run = lambda cmd: executed_cmds.append(cmd)

    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GIT_AUTHOR_NAME", "Test User")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "test@example.com")

    git_auto.ensure_git_identity()
    assert ["git", "config", "user.name", "Test User"] in executed_cmds
    assert ["git", "config", "user.email", "test@example.com"] in executed_cmds

def test_git_create_daily_commits_orchestration(tmp_path):
    from unittest.mock import MagicMock
    git_auto = GitAutomation(repo_root=tmp_path)
    git_auto.ensure_git_identity = MagicMock()

    staged_calls = []
    def fake_stage_and_commit(paths, msg):
        staged_calls.append((paths, msg))
        return True

    git_auto.stage_and_commit = fake_stage_and_commit
    git_auto.is_working_tree_clean = MagicMock(return_value=True)

    impl = tmp_path / "learning" / "python" / "day_015_typing.py"
    test = tmp_path / "tests" / "test_day_015_typing.py"
    notes = tmp_path / "learning" / "python" / "day_015_notes.md"
    progress = tmp_path / "progress.json"
    progress.write_text("{}", encoding="utf-8")

    count = git_auto.create_daily_commits(
        day=15,
        topic="Type Hinting",
        category="python",
        written_paths=[impl, test, notes]
    )

    assert count == 4
    assert len(staged_calls) == 4
    assert "feat(day-015)" in staged_calls[0][1]
    assert "test(day-015)" in staged_calls[1][1]
    assert "docs(day-015)" in staged_calls[2][1]
    assert "chore(day-015)" in staged_calls[3][1]
