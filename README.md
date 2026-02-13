# NanoWait: The Adaptive Wait Engine for Python

[![PyPI version](https://img.shields.io/pypi/v/nano_wait.svg)](https://pypi.org/project/nano-wait/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/nano_wait.svg)](https://pypi.org/project/nano-wait/)

**NanoWait** is a deterministic and adaptive execution wait engine designed to replace Python's standard `time.sleep()`. Instead of waiting for a fixed duration, NanoWait dynamically adjusts the wait time based on **system load (CPU/RAM)** and optionally **Wi-Fi signal strength**, ensuring automation scripts remain reliable even in slow or overloaded environments.

With **Execution Profiles**, NanoWait offers a semantic layer to manage wait behavior, allowing you to define the operational context clearly and consistently.

> **In summary:** You request a base time (e.g., `wait(5)`), and NanoWait ensures a *safe, context-aware wait* that never exceeds the requested time and never falls below a minimum execution floor.

### Cross-Platform Stability & Headless Environments

NanoWait has been optimized for **cross-platform stability**, especially macOS, and **safe usage in headless environments** (CI, RPA, servers). In headless environments, no graphical UI is instantiated, preventing crashes such as `NSWindow should only be instantiated on the main thread` on macOS. This ensures total stability in CI/CD pipelines, Docker, and remote execution.

---

## 🚀 Key Features

- **Adaptive Waiting:** Dynamically scales wait times based on real-time system metrics.  
- **Execution Profiles:** Semantic presets for CI, RPA, Testing, and more.  
- **Async Support:** Native `wait_async` for non-blocking execution in `asyncio` environments.  
- **Parallel Execution:** `wait_pool` and `wait_pool_async` for multiple waits concurrently.  
- **Ultra-Adaptive Auto Wait (`wait_auto`):** Automatically computes the safest and fastest interval without manual configuration.  
- **Cross-Platform Stability:** Optimized for macOS and headless environments.  
- **Explain Mode:** Auditable decision reports for full transparency.  
- **CLI Support:** Powerful command-line interface for quick tasks.  
- **Local Telemetry:** Opt-in system for analyzing wait behavior without remote data collection.

---

## 🆕 Ultra-Adaptive Auto Wait (`wait_auto`) — Full Reference

**`wait_auto` is the core default for all waits when no profile is specified (`profile="auto"`).** It is designed for **automation workflows** (e.g., PyAutoGUI scripts) and removes the need to manually tune wait times.

It automatically:

- Estimates the optimal wait time for your system.  
- Considers CPU, RAM, and optional Wi-Fi signal strength.  
- Chooses the minimal safe interval between actions.  
- Applies the selected Execution Profile automatically.  
- Logs and prints the wait decision (optional).  
- Works out-of-the-box with loops, sequences, and PyAutoGUI automation.  

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `verbose` | `bool` | `False` | Prints interval calculation details to console. |
| `log` | `bool` | `False` | Logs wait decision to file or system log. |
| `telemetry` | `bool` | `False` | Records metrics like CPU, Wi-Fi, and interval for analysis. |
| `profile` | `str` | `"auto"` | Execution profile: `"default"`, `"ci"`, `"rpa"`, `"fast"`, `"auto"` etc. |
| `wifi` | `str | None` | `None` | Optional SSID to include Wi-Fi signal in calculation. |
| `min_interval` | `float` | `0.05` | Lower floor for waits (seconds). |
| `max_interval` | `float | None` | `None` | Optional maximum cap for wait times. |
| `callback` | `Callable | None` | `None` | Function to run after wait completes (sync or async). |

> Tip: When called via `wait()`, `wait_auto` is used automatically if no profile is provided.

---

### Basic Usage

```python
from nano_wait import wait

# Simple wait_auto usage (default auto profile)
interval = wait(verbose=True)
print(f"Interval calculated: {interval:.3f}s")
````

---

### Integration with PyAutoGUI

```python
import pyautogui
from nano_wait import wait

# Example automation sequence using auto wait
pyautogui.click(100, 200)
wait()  # Computes next safe interval automatically
pyautogui.write("Hello, world!")
wait(verbose=True)  # Logs the decision
pyautogui.press("enter")
```

**Tip:** `wait_auto` ensures your automation adapts to CPU load and network conditions automatically.

---

### Using `wait_auto` in Loops

```python
from nano_wait import wait
import pyautogui

# Repeated actions with adaptive interval
for i in range(5):
    pyautogui.moveTo(100 + i*10, 200 + i*10)
    wait()  # Interval adapts per iteration
```

---

### Async Integration with `wait_async`

```python
import asyncio
from nano_wait import wait_async

async def perform_tasks():
    print("Task 1 started")
    await wait_async(smart=True, verbose=True)
    print("Task 1 finished, adaptive wait applied")

asyncio.run(perform_tasks())
```

**Note:** `wait_auto` logic is embedded in `wait_async` when used with `profile="auto"`.

---

### Advanced Features

#### Telemetry Example

```python
from nano_wait import wait

interval = wait(verbose=True, telemetry=True)
print(f"Adaptive interval recorded: {interval:.3f}s")
```

* Records CPU, Wi-Fi, and wait interval for later analysis.
* Compatible with the `TelemetryDashboard` for live visualization.

#### Explain Mode Example

```python
from nano_wait import wait

report = wait(2, explain=True)
print(report)
```

* Returns an **ExplainReport** object.
* Contains factor, bias, requested and actual interval, CPU/Wi-Fi scores, and timestamp.

---

### Best Practices

1. Use `wait_auto()` for all automation scripts to avoid hard-coded delays.
2. Combine with PyAutoGUI for UI automation.
3. Enable `telemetry` and `verbose` during testing for optimal tuning.
4. Use `explain=True` for debugging or auditing wait decisions.

---

## 💡 Quick Start

### Standard Adaptive Wait

```python
from nano_wait import wait
import time

# Adaptive wait (up to 5 seconds, adjusted by system load)
start = time.time()
wait(5)
print(f"nano_wait.wait(): {time.time() - start:.2f}s")
```

*NanoWait never waits longer than the requested base time and applies a minimum internal delay of 50ms to prevent excessive CPU usage.*

---

## 🌐 Parallel Execution (`wait_pool`)

Run multiple adaptive waits in parallel, ideal for batch automation or concurrent UI interactions.

```python
import psutil
from nano_wait import wait_pool

def heavy_load():
    return psutil.cpu_percent() > 80

results = wait_pool([1, 2, 3], cancel_if=heavy_load)
```

---

## ⚡️ Asynchronous Support (`wait_async`)

NanoWait supports asynchronous environments like **FastAPI**, **asyncio bots**, or **web scrapers**.

```python
import asyncio
from nano_wait import wait_async

async def main():
    result = await wait_async(2, smart=True)
    print(f"Wait finished in: {result:.3f}s")

asyncio.run(main())
```

---

## ⚙️ Core API Reference

| Function          | Sync | Async | Parallel | Cancelable |
| :---------------- | :--: | :---: | :------: | :--------- |
| `wait`            |   ✅  |   ❌   |     ❌    | ❌          |
| `wait_async`      |   ❌  |   ✅   |     ❌    | ❌          |
| `wait_pool`       |   ✅  |   ❌   |     ✅    | ✅          |
| `wait_pool_async` |   ❌  |   ✅   |     ✅    | ✅          |
| `wait_auto`       |   ✅  |   ❌   |     ❌    | ❌          |

> **Note:** `wait_auto` is now **integrated into `wait()`** as the default when no profile is provided.

---

## 🛠️ Installation

```bash
pip install nano_wait
```

### Required Dependencies

```bash
pip install psutil pywifi
```

### Optional — Vision Mode

Visual waiting is available in a dedicated package:

```bash
pip install nano-wait-vision
```

*Note: Without Vision Mode, NanoWait will raise a runtime error if visual functions are requested.*

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.