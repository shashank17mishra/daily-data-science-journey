from server import get_container_config

def test_container_config():
    config = get_container_config()
    assert config["port"] == "8080"
    assert config["status"] == "ready"
