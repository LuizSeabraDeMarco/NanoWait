from nano_wait.vision import VisionMode


def test_ocr_returns_string(monkeypatch):
    vm = VisionMode()

    monkeypatch.setattr(vm, "_ocr", lambda img: "test text")

    result = vm._ocr(None)
    assert isinstance(result, str)
    assert result == "test text"


def test_ocr_empty_string(monkeypatch):
    vm = VisionMode()

    monkeypatch.setattr(vm, "_ocr", lambda img: "")

    result = vm._ocr(None)
    assert result == ""


def test_extract_text_calls_ocr(monkeypatch):
    vm = VisionMode()

    called = {"value": False}

    def fake_ocr(img):
        called["value"] = True
        return "OK"

    monkeypatch.setattr(vm, "_ocr", fake_ocr)

    text = vm._extract_text("fake_image")
    assert called["value"] is True
    assert text == "OK"


def test_extract_text_handles_none_image(monkeypatch):
    vm = VisionMode()

    monkeypatch.setattr(vm, "_ocr", lambda img: "")

    result = vm._extract_text(None)
    assert result == ""
