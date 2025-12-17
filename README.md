# Nano-Wait

## Intelligent Automation with Adaptive Waiting and Computer Vision

---

## Overview

Nano-Wait is a Python library for automating graphical user interfaces (GUIs) that replaces the use of `time.sleep()` with an Intelligent Adaptive Waiting system, dynamically adjusting the wait time based on:

- Computer performance (CPU and memory)

- Wi-Fi signal quality (when available)

- User-defined aggressiveness level

From version **3.0**, Nano-Wait also includes a Computer Vision (OCR) module capable of reading numbers directly from the screen and making automated decisions.

## 🚀 Why not use `time.sleep()`?

`time.sleep()` is static and "blind":

it ignores whether the system is overloaded or if the network is slow.

Nano-Wait solves this by applying a Dynamic Adjustment Factor, ensuring that the script:

- Is not too slow when the system is fast

- Nor too fast to the point of breaking the automation

---

## 📦 Installation
```bash
pip install nano-wait
```
### Optional Dependencies

For full functionality of the Vision module:


- Tesseract OCR (required for OCR)

- pytesseract

- Pillow

- pyautogui

- pynput

- psutil

- pywifi (Windows only)

## ⚠️ Nano-Wait does not collect network data.

It only reads local signal and operating system performance metrics.

## 🧠 Module 1 — Adaptive Waiting (Smart Wait)

Main function: **wait()**

The wait() function is the direct replacement for time.sleep().

```python
from nano_wait import wait

wait(5)
```
Function Signature
```python
wait(
    t: float,
    wifi: str | None = None,
    speed: str | float = "normal",
    verbose: bool = False,
    log: bool = False
)

```

### Parameters

| Parameter | Default Value | Behavior when omitted |
|---------|--------------|-------------------------------|
| t | **required** | Defines the maximum wait time. Cannot be omitted. |
| wifi | `None` | Nano-Wait ignores network metrics and calculates the factor based only on local performance (CPU and memory). |
| speed | `"normal"` | Uses balanced aggressiveness, prioritizing stability without sacrificing performance. |
| verbose | `False` | No calculation information is displayed in the terminal. |
| log| `False` | No log file is generated (`nano_wait.log` is neither created nor updated). |

## Example with Wi-Fi
```python
wait(
    5,
    wifi="My5G_Network",
    speed="fast",
    verbose=True
)
```
## Example without Wi-Fi (local hardware only)
```python
wait(2, speed="ultra")
```

## 🔬 How wait time is calculated

Nano-Wait calculates an adaptive factor based on:

- CPU usage

- Memory usage

- Wi-Fi signal strength (when available)

## Formula applied
```python
wait_time = max(0.05, min(t / factor, t))
```
## Safety rules

- Floor: never wait less than 50 ms

- Ceiling: never exceed the original t time

- Avoids excessive CPU usage

## 🧠 Module 2 — Vision (OCR and Visual Decision)

The Vision module allows you to read Display numbers on the screen and make automatic decisions.

Main Class

```python
from nano_wait.vision import VisionMode
```
### Available Modes

| Mode | Description |
|------|----------|
| observe | Only reads and displays data |
| decision | Reads data and executes actions |
| learn | Collects visual patterns (experimental) |

## 📸 Screen Region Capture

The user can manually mark regions:

```python
region = VisionMode.mark_region()
```

The return is a tuple:

```
(x, y, width, height)
```
## 🔍 Complete Example — Reading and Decision
```python
from nano_wait.vision import VisionMode

vision = VisionMode(mode="decision")
region = VisionMode.mark_region()
vision.run(regions=[region])

```
## Internal Logic (decision mode)

- If detected number is greater than 1000 → double-click  

Otherwise → skip item

These actions can be easily customized in the code.

## ⚙️ Vision Internal Pipeline

- Screen region capture (ImageGrab)

- Grayscale conversion

- OCR via Tesseract

- Numerical extraction with Regex

- Execution of automated actions

## 🧪 Learn Mode (Current State)

The learn mode currently:

- Captures visual data repeatedly  
- Serves as a basis for future versions with persistence

📌 Note: The learn mode does not yet save models to disk.

It is experimental and focused on data collection.

| System | Wi-Fi | Note |
| ------- | ----- | --------------------- |
| Windows | ✅ | Uses pywifi |
| macOS | ✅ | Uses airport command |
| Linux | ✅ | Uses nmcli |
| Others | ❌ | Only wireless mode |

## 🛠 Real-World Use Cases

- Visual Automation Bots

- Legacy Dashboard Reading

- Intelligent Click Adjustment

- OCR-Based Automation

- Lightweight RPA without Selenium

## 🤝 Contribution

- Fork the project

- Create a branch (feature/my-improvement)

- Submit a Pull Request

## 📄 License

MIT License

## 👤 Author

Luiz Seabra De Marco

## 👤 Documentation Author

Vitor Seabra De Marco