import pytest
from nano_wait.vision import VisionMode


def test_vision_mode_default_state():
    vm = VisionMode()
    assert vm.mode in ("observe", "decision", "learn")


def test_vision_set_mode_valid():
    vm = VisionMode()
    vm.set_mode("decision")
    assert vm.mode == "decision"


def test_vision_set_mode_invalid():
    vm = VisionMode()
    with pytest.raises(ValueError):
        vm.set_mode("invalid_mode")


def test_vision_mark_region():
    vm = VisionMode()
    region = (10, 20, 200, 300)
    vm.mark_region(region)
    assert vm.region == region


def test_vision_run_without_region_returns_none():
    vm = VisionMode()
    result = vm.run()
    assert result is None


def test_vision_run_with_region(monkeypatch):
    vm = VisionMode()
    vm.mark_region((0, 0, 100, 100))

    monkeypatch.setattr(vm, "_capture_screen", lambda: "fake_image")
    monkeypatch.setattr(vm, "_extract_text", lambda img: "READY")

    result = vm.run()
    assert result == "READY"


def test_vision_mode_does_not_crash_in_learn_mode(monkeypatch):
    vm = VisionMode(mode="learn")
    vm.mark_region((0, 0, 50, 50))

    monkeypatch.setattr(vm, "_capture_screen", lambda: "img")
    monkeypatch.setattr(vm, "_extract_text", lambda img: "Loading")

    result = vm.run()
    assert isinstance(result, str)
