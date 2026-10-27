import concurrent.futures
import pytest
from learning.python.day_060_creational_design_patterns import (
    SingletonMeta,
    DynamicFactory,
    ModelConfig,
    ModelConfigBuilder,
    PrototypeRegistry,
)


class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, connection_string: str = "sqlite:///:memory:"):
        self.connection_string = connection_string


class SamplePrototype:
    def __init__(self, name: str, settings: dict, tags: list):
        self.name = name
        self.settings = settings
        self.tags = tags


def test_singleton_returns_same_instance():
    db1 = DatabaseConnection("db_a")
    db2 = DatabaseConnection("db_b")
    assert db1 is db2


def test_singleton_thread_safety():
    instances = []

    def get_instance():
        return DatabaseConnection()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_instance) for _ in range(20)]
        for future in concurrent.futures.as_completed(futures):
            instances.append(future.result())

    first_instance = instances[0]
    for inst in instances:
        assert inst is first_instance


def test_dynamic_factory_registration_and_creation():
    factory = DynamicFactory()
    factory.register("linear", lambda lr: f"LinearModel(lr={lr})")

    model = factory.create("linear", lr=0.01)
    assert model == "LinearModel(lr=0.01)"


def test_dynamic_factory_duplicate_registration_fails():
    factory = DynamicFactory()
    factory.register("svc", lambda: "SVC")
    with pytest.raises(ValueError, match="already registered"):
        factory.register("svc", lambda: "SVC2")


def test_dynamic_factory_unregistered_key_raises():
    factory = DynamicFactory()
    with pytest.raises(KeyError, match="not registered"):
        factory.create("unknown")


def test_dynamic_factory_unregister():
    factory = DynamicFactory()
    factory.register("tree", lambda: "DecisionTree")
    assert factory.create("tree") == "DecisionTree"
    factory.unregister("tree")
    with pytest.raises(KeyError):
        factory.create("tree")


def test_builder_successful_build():
    builder = ModelConfigBuilder()
    config = (
        builder.set_model_type("transformer")
        .set_learning_rate(0.001)
        .set_epochs(10)
        .set_batch_size(32)
        .set_optimizer("adamw")
        .build()
    )
    assert isinstance(config, ModelConfig)
    assert config.model_type == "transformer"
    assert config.learning_rate == 0.001
    assert config.epochs == 10
    assert config.batch_size == 32
    assert config.optimizer == "adamw"


def test_builder_immutability():
    builder = ModelConfigBuilder()
    config = (
        builder.set_model_type("cnn")
        .set_learning_rate(0.01)
        .set_epochs(5)
        .set_batch_size(64)
        .build()
    )
    with pytest.raises(Exception):
        config.epochs = 20


def test_builder_missing_required_fields():
    builder = ModelConfigBuilder()
    builder.set_model_type("resnet")
    with pytest.raises(ValueError, match="Missing required field"):
        builder.build()


def test_builder_invalid_inputs():
    builder = ModelConfigBuilder()
    with pytest.raises(ValueError):
        builder.set_learning_rate(-0.01)
    with pytest.raises(ValueError):
        builder.set_epochs(0)
    with pytest.raises(ValueError):
        builder.set_batch_size(-5)
    with pytest.raises(ValueError):
        builder.set_model_type("")


def test_prototype_cloning_and_independence():
    registry = PrototypeRegistry()
    base_proto = SamplePrototype("base_model", {"depth": 10}, ["v1", "test"])
    registry.register("base_model", base_proto)

    cloned = registry.clone("base_model", name="custom_model")
    assert cloned is not base_proto
    assert cloned.name == "custom_model"
    assert cloned.settings == {"depth": 10}

    cloned.settings["depth"] = 20
    cloned.tags.append("v2")

    assert base_proto.settings["depth"] == 10
    assert base_proto.tags == ["v1", "test"]


def test_prototype_unregistered_clone_raises():
    registry = PrototypeRegistry()
    with pytest.raises(KeyError, match="not registered"):
        registry.clone("non_existent")


def test_prototype_invalid_attribute_override_raises():
    registry = PrototypeRegistry()
    base_proto = SamplePrototype("base", {}, [])
    registry.register("base", base_proto)

    with pytest.raises(AttributeError, match="does not exist"):
        registry.clone("base", non_existent_attr=123)


def test_prototype_unregister():
    registry = PrototypeRegistry()
    base_proto = SamplePrototype("base", {}, [])
    registry.register("base", base_proto)
    registry.unregister("base")

    with pytest.raises(KeyError):
        registry.clone("base")
