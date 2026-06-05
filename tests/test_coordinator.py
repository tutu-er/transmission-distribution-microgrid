"""协调控制器测试."""

from tdm.core.coordinator import Coordinator


def test_coordinator_run() -> None:
    coord = Coordinator(name="test")
    result = coord.run()
    assert result["status"] == "ok"
    assert result["coordinator"] == "test"
