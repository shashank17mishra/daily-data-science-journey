import os
import pytest
from learning.python.day_026_custom_context_managers import TransactionalStore, temp_env_vars


def test_transaction_success() -> None:
    """Test that successful transactions commit changes correctly."""
    store = TransactionalStore({"a": 1, "b": 2})
    
    with store.transaction() as tx:
        store.data["a"] = 10
        store.data["c"] = 3
        assert tx.committed is False

    assert tx.committed is True
    assert tx.rolled_back is False
    assert store.data == {"a": 10, "b": 2, "c": 3}


def test_transaction_rollback() -> None:
    """Test that transactions roll back state on exceptions."""
    store = TransactionalStore({"a": 1, "b": 2})
    
    with pytest.raises(ValueError):
        with store.transaction() as tx:
            store.data["a"] = 99
            store.data["b"] = 100
            raise ValueError("Something went wrong")
            
    assert tx.committed is False
    assert tx.rolled_back is True
    assert store.data == {"a": 1, "b": 2}  # Restored to original state


def test_transaction_exception_suppression() -> None:
    """Test that specified exceptions are suppressed and state is rolled back."""
    store = TransactionalStore({"a": 1})
    
    # Suppress KeyError, but let other exceptions propagate
    with store.transaction(suppress_exceptions=(KeyError,)) as tx:
        store.data["a"] = 5
        raise KeyError("Suppressed key error")
        
    assert tx.committed is False
    assert tx.rolled_back is True
    assert store.data == {"a": 1}  # Rolled back


def test_nested_transactions() -> None:
    """Test nested transactions where inner failure rolls back only inner changes."""
    store = TransactionalStore({"a": 1})
    
    with store.transaction() as outer_tx:
        store.data["a"] = 2
        
        # Inner transaction fails and suppresses its own exception
        with store.transaction(suppress_exceptions=(ValueError,)) as inner_tx:
            store.data["a"] = 3
            raise ValueError("Inner failure")
            
        assert inner_tx.rolled_back is True
        assert store.data["a"] == 2  # Rolled back to outer transaction state
        
    assert outer_tx.committed is True
    assert store.data["a"] == 2


def test_temp_env_vars_success() -> None:
    """Test that environment variables are temporarily overridden and restored."""
    os.environ["TEST_KEY_1"] = "original_val"
    if "TEST_KEY_2" in os.environ:
        del os.environ["TEST_KEY_2"]
        
    overrides = {
        "TEST_KEY_1": "new_val",
        "TEST_KEY_2": "temp_val"
    }
    
    with temp_env_vars(overrides):
        assert os.environ["TEST_KEY_1"] == "new_val"
        assert os.environ["TEST_KEY_2"] == "temp_val"
        
    assert os.environ["TEST_KEY_1"] == "original_val"
    assert "TEST_KEY_2" not in os.environ


def test_temp_env_vars_exception() -> None:
    """Test that environment variables are restored even if an exception occurs."""
    os.environ["TEST_KEY_1"] = "original_val"
    
    with pytest.raises(RuntimeError):
        with temp_env_vars({"TEST_KEY_1": "new_val"}):
            assert os.environ["TEST_KEY_1"] == "new_val"
            raise RuntimeError("Error inside block")
            
    assert os.environ["TEST_KEY_1"] == "original_val"
