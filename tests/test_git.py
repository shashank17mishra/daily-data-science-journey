import pytest
from src.automation.git import GitAutomation

def test_git_commit_generic_message_rejection():
    git_auto = GitAutomation()
    with pytest.raises(ValueError, match="Invalid or generic commit message"):
        git_auto.commit("update")

    with pytest.raises(ValueError, match="Invalid or generic commit message"):
        git_auto.commit("test")
