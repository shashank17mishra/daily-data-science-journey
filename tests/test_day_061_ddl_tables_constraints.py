import sqlite3
import pytest
from learning.sql.day_061_ddl_tables_constraints import DatabaseSchemaManager


@pytest.fixture
def db_manager():
    """Fixture providing initialized database schema manager."""
    manager = DatabaseSchemaManager(":memory:")
    manager.create_tables()
    yield manager
    manager.close()


def test_schema_creation_and_column_metadata(db_manager):
    """Test table creation and schema metadata retrieval."""
    dept_cols = db_manager.get_table_columns("departments")
    col_names = [col["name"] for col in dept_cols]
    assert "dept_id" in col_names
    assert "dept_name" in col_names
    assert "budget" in col_names

    dept_id_col = next(c for c in dept_cols if c["name"] == "dept_id")
    assert dept_id_col["pk"] is True

    dept_name_col = next(c for c in dept_cols if c["name"] == "dept_name")
    assert dept_name_col["notnull"] is True

    emp_fk = db_manager.get_foreign_keys("employees")
    assert len(emp_fk) == 1
    assert emp_fk[0]["table"] == "departments"
    assert emp_fk[0]["from"] == "dept_id"
    assert emp_fk[0]["to"] == "dept_id"
    assert emp_fk[0]["on_delete"] == "RESTRICT"


def test_successful_insertion(db_manager):
    """Test valid insertions into departments and employees tables."""
    dept_id = db_manager.add_department("Engineering", 100000.0)
    assert dept_id == 1

    emp_id = db_manager.add_employee("Alice", "alice@example.com", 85000.0, dept_id)
    assert emp_id == 1


def test_unique_constraint_violation(db_manager):
    """Test that duplicate department names or emails violate UNIQUE constraint."""
    db_manager.add_department("HR", 50000.0)
    with pytest.raises(sqlite3.IntegrityError):
        db_manager.add_department("HR", 60000.0)

    dept_id = 1
    db_manager.add_employee("Bob", "bob@example.com", 60000.0, dept_id)
    with pytest.raises(sqlite3.IntegrityError):
        db_manager.add_employee("Robert", "bob@example.com", 70000.0, dept_id)


def test_check_constraint_violation(db_manager):
    """Test that invalid values violate CHECK constraints."""
    with pytest.raises(sqlite3.IntegrityError):
        db_manager.add_department("Finance", -100.0)

    dept_id = db_manager.add_department("Finance", 50000.0)
    with pytest.raises(sqlite3.IntegrityError):
        db_manager.add_employee("Charlie", "charlie@example.com", -50.0, dept_id)


def test_foreign_key_constraint_violation(db_manager):
    """Test that referencing non-existent foreign key raises IntegrityError."""
    with pytest.raises(sqlite3.IntegrityError):
        db_manager.add_employee("Eve", "eve@example.com", 75000.0, dept_id=999)


def test_foreign_key_restrict_on_delete(db_manager):
    """Test that ON DELETE RESTRICT prevents deleting department with employees."""
    dept_id = db_manager.add_department("Sales", 80000.0)
    db_manager.add_employee("David", "david@example.com", 65000.0, dept_id)

    with pytest.raises(sqlite3.IntegrityError):
        db_manager.delete_department(dept_id)
