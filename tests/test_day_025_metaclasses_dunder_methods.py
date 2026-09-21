import pytest
from learning.python.day_025_metaclasses_dunder_methods import (
    BaseModel,
    ModelMeta,
    Field,
    StringField,
    IntegerField,
)


class User(BaseModel):
    name = StringField(min_length=2, max_length=50)
    age = IntegerField(min_value=0, max_value=120)
    email = StringField(required=False, default="unknown@example.com")


def test_model_instantiation_and_validation():
    user = User(name="Alice", age=30)
    assert user.name == "Alice"
    assert user.age == 30
    assert user.email == "unknown@example.com"


def test_field_validation_type_error():
    with pytest.raises(TypeError, match="must be a str"):
        User(name=123, age=25)

    with pytest.raises(TypeError, match="must be an int"):
        User(name="Bob", age="twenty")


def test_field_validation_value_error():
    with pytest.raises(ValueError, match="at least 2 chars"):
        User(name="A", age=25)

    with pytest.raises(ValueError, match=">= 0"):
        User(name="Bob", age=-1)


def test_missing_required_field():
    with pytest.raises(ValueError, match="Missing required field 'name'"):
        User(age=25)


def test_model_dunder_methods():
    user1 = User(name="Charlie", age=40)
    user2 = User(name="Charlie", age=40)
    user3 = User(name="Dave", age=40)

    assert repr(user1) == "User(name='Charlie', age=40, email='unknown@example.com')"
    assert user1 == user2
    assert user1 != user3
    assert user1 != "not_a_user"
    assert len(user1) == 3

    assert user1["name"] == "Charlie"
    user1["age"] = 41
    assert user1.age == 41

    with pytest.raises(KeyError):
        _ = user1["non_existent"]

    with pytest.raises(KeyError):
        user1["non_existent"] = "value"


def test_metaclass_registry():
    registered = ModelMeta.get_registered_models()
    assert "User" in registered
    assert registered["User"] is User
