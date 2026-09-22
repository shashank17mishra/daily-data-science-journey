import copy
import os
from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional, Type, Union


class TransactionalStore:
    """
    A simple key-value store that supports nested transactions via context managers.
    """
    def __init__(self, initial_data: Optional[Dict[Any, Any]] = None) -> None:
        self._data: Dict[Any, Any] = copy.deepcopy(initial_data) if initial_data else {}
        self._transaction_stack: list[Dict[Any, Any]] = []

    @property
    def data(self) -> Dict[Any, Any]:
        return self._data

    def transaction(self, suppress_exceptions: Optional[tuple[Type[BaseException], ...]] = None) -> "Transaction":
        """
        Returns a Transaction context manager for this store.
        """
        return Transaction(self, suppress_exceptions=suppress_exceptions)


class Transaction:
    """
    Class-based context manager implementing transactional safety for TransactionalStore.
    Supports nested transactions, rollbacks on failure, and selective exception suppression.
    """
    def __init__(
        self, 
        store: TransactionalStore, 
        suppress_exceptions: Optional[tuple[Type[BaseException], ...]] = None
    ) -> None:
        self.store = store
        self.suppress_exceptions = suppress_exceptions or ()
        self._snapshot: Optional[Dict[Any, Any]] = None
        self.committed = False
        self.rolled_back = False

    def __enter__(self) -> "Transaction":
        # Save a deep copy of the current state before entering the block
        self._snapshot = copy.deepcopy(self.store._data)
        self.store._transaction_stack.append(self._snapshot)
        return self

    def __exit__(
        self, 
        exc_type: Optional[Type[BaseException]], 
        exc_val: Optional[BaseException], 
        exc_tb: Optional[Any]
    ) -> bool:
        if not self.store._transaction_stack:
            raise RuntimeError("Transaction stack underflow: No active transaction found.")
        
        # Pop the snapshot corresponding to this transaction
        last_snapshot = self.store._transaction_stack.pop()

        if exc_type is not None:
            # An exception occurred: Rollback to the snapshot state
            self.store._data = last_snapshot
            self.rolled_back = True
            
            # Check if we should suppress this exception
            if issubclass(exc_type, self.suppress_exceptions):
                return True  # Suppress exception
            return False  # Propagate exception
        
        # No exception: Commit changes
        self.committed = True
        return False


@contextmanager
def temp_env_vars(overrides: Dict[str, str]) -> Generator[None, None, None]:
    """
    A generator-based context manager that temporarily overrides environment variables.
    Restores original environment variables upon exit, even if exceptions occur.
    """
    original_vars = {}
    for key, value in overrides.items():
        # Save original state (either the value or None if it didn't exist)
        original_vars[key] = os.environ.get(key, None)
        os.environ[key] = value

    try:
        yield
    finally:
        # Restore original environment state
        for key, original_value in original_vars.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value
