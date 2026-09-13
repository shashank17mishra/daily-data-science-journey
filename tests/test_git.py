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


def test_git_push_local_skips(monkeypatch):
    git_auto = GitAutomation()
    executed_cmds = []
    git_auto._run = lambda cmd: executed_cmds.append(cmd)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)

    git_auto.push()
    assert len(executed_cmds) == 0


def test_git_push_ci_success(monkeypatch):
    git_auto = GitAutomation()
    executed_cmds = []
    git_auto._run = lambda cmd: executed_cmds.append(cmd)

    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_REF_NAME", "main")

    git_auto.push()
    assert ["git", "fetch", "origin", "main"] in executed_cmds
    assert ["git", "rebase", "origin/main"] in executed_cmds
    assert ["git", "push", "origin", "HEAD:main"] in executed_cmds


def test_git_push_ci_retry_on_failure(monkeypatch):
    git_auto = GitAutomation()
    executed_cmds = []
    attempts = 0

    def mock_run(cmd):
        nonlocal attempts
        executed_cmds.append(cmd)
        if cmd == ["git", "push", "origin", "HEAD:main"] and attempts == 0:
            attempts += 1
            raise RuntimeError("push rejected (fetch first)")
        return ""

    git_auto._run = mock_run
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_REF_NAME", "main")
    monkeypatch.setattr("time.sleep", lambda s: None)

    git_auto.push(max_retries=2)
    assert attempts == 1
    assert ["git", "rebase", "--abort"] in executed_cmds
    assert executed_cmds.count(["git", "push", "origin", "HEAD:main"]) == 2


def test_git_push_ci_aborts_and_raises_after_max_retries(monkeypatch):
    git_auto = GitAutomation()
    executed_cmds = []

    def mock_run(cmd):
        executed_cmds.append(cmd)
        if "push" in cmd:
            raise RuntimeError("push failed")
        return ""

    git_auto._run = mock_run
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_REF_NAME", "main")
    monkeypatch.setattr("time.sleep", lambda s: None)

    with pytest.raises(RuntimeError, match="Git push failed after 2 attempts"):
        git_auto.push(max_retries=2)

    assert ["git", "rebase", "--abort"] in executed_cmds

