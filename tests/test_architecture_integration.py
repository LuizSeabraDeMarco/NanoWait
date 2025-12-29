from nano_wait.core import wait
from nano_wait.vision import VisionMode


def test_wait_with_vision_condition(monkeypatch):
    vm = VisionMode()
    vm.mark_region((0, 0, 100, 100))

    monkeypatch.setattr(vm, "run", lambda: "DONE")

    result = wait(lambda: vm.run() == "DONE", timeout=0.5)
    assert result is True


def test_multiple_vision_instances_are_independent():
    v1 = VisionMode()
    v2 = VisionMode()

    v1.set_mode("learn")
    v2.set_mode("decision")

    assert v1.mode != v2.mode


def test_wait_does_not_modify_vision_state():
    vm = VisionMode()
    initial_mode = vm.mode

    wait(lambda: True, timeout=0.1)

    assert vm.mode == initial_mode


def test_imports_are_clean():
    import nano_wait.core
    import nano_wait.vision

    assert True
