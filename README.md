# NanoWait: The Adaptive Wait Engine for Python

[![PyPI version](https://img.shields.io/pypi/v/nano_wait.svg)](https://pypi.org/project/nano-wait/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/nano_wait.svg)](https://pypi.org/project/nano-wait/)

**NanoWait** is a deterministic and adaptive execution wait engine designed to replace Python's standard `time.sleep()`. Instead of waiting for a fixed duration, NanoWait dynamically adjusts the wait time based on **system load (CPU/RAM)** and optionally **Wi-Fi signal strength**, ensuring automation scripts remain reliable even in slow or overloaded environments.

With **Execution Profiles**, NanoWait offers a semantic layer to manage wait behavior, allowing you to define the operational context clearly and consistently.

Now with **Deterministic Condition Waiting**, NanoWait can also wait for *state changes* — not just time.

> **In summary:** You request a base time (e.g., `wait(5)`), or a condition (e.g., `wait(lambda: ready())`), and NanoWait ensures a *safe, context-aware wait* that never exceeds the requested constraints and never falls below a minimum execution floor.

---

## Cross-Platform Stability & Headless Environments

NanoWait has been optimized for **cross-platform stability**, especially macOS, and **safe usage in headless environments** (CI, RPA, servers). In headless environments, no graphical UI is instantiated, preventing crashes such as `NSWindow should only be instantiated on the main thread` on macOS.

This ensures total stability in CI/CD pipelines, Docker containers, and remote execution.

---

# 🚀 Key Features

* **Adaptive Waiting:** Dynamically scales wait times based on real-time system metrics.
* **Deterministic Condition Waiting (`wait(until=...)`):** Wait for Python conditions instead of fixed delays.
* **Execution Profiles:** Semantic presets for CI, RPA, Testing, and more.
* **Async Support:** Native `wait_async` for non-blocking execution in `asyncio` environments.
* **Parallel Execution:** `wait_pool` and `wait_pool_async` for multiple waits concurrently.
* **Ultra-Adaptive Auto Wait (`wait_auto`):** Automatically computes the safest and fastest interval without manual configuration.
* **Cross-Platform Stability:** Optimized for macOS and headless environments.
* **Explain Mode:** Auditable decision reports for full transparency.
* **CLI Support:** Powerful command-line interface for quick tasks.
* **Local Telemetry:** Opt-in system for analyzing wait behavior without remote data collection.

---

# 🆕 Deterministic Condition Waiting (`wait(until=...)`)

NanoWait 5.1 introduces **condition-based waiting**, eliminating the need for manual polling loops like:

```python
while not something_ready():
    time.sleep(0.3)
```

Instead, you can now write:

```python
from nano_wait import wait

wait(lambda: something_ready(), timeout=10)
```

### What This Solves

* Removes fragile polling loops
* Prevents excessive CPU usage
* Applies adaptive backoff automatically
* Respects a minimum 50ms interval
* Stops safely at timeout
* Integrates with telemetry and profiles

---

## Condition Waiting Parameters

| Parameter   | Type       | Default  | Description                                    |
| ----------- | ---------- | -------- | ---------------------------------------------- |
| `until`     | `Callable` | `None`   | Condition function returning `True` when ready |
| `timeout`   | `float`    | `15.0`   | Maximum time allowed                           |
| `profile`   | `str`      | `"auto"` | Execution profile                              |
| `smart`     | `bool`     | `False`  | Enables smart speed detection                  |
| `verbose`   | `bool`     | `False`  | Prints polling intervals                       |
| `telemetry` | `bool`     | `False`  | Records adaptive adjustments                   |
| `explain`   | `bool`     | `False`  | Returns decision report                        |

---

## Basic Condition Usage

```python
from nano_wait import wait

def api_ready():
    return check_server_status() == 200

result = wait(api_ready, timeout=5)

if result:
    print("API is ready.")
else:
    print("Timeout reached.")
```

---

## Waiting for File Availability

```python
import os
from nano_wait import wait

wait(lambda: os.path.exists("output.txt"), timeout=10)
```

---

## Adaptive Polling in Action

NanoWait dynamically adjusts polling intervals:

* Heavy CPU load → slightly longer interval
* Light system load → faster responsiveness
* Never below 50ms floor
* Never exceeds timeout

This makes it safe for:

* Backend services
* CI pipelines
* API retry loops
* Scraping workflows
* Database readiness checks

---

# 🆕 Ultra-Adaptive Auto Wait (`wait_auto`)

`wait_auto` remains the default engine behind `wait()` when no condition is provided.

It automatically:

* Estimates optimal wait time
* Considers CPU and Wi-Fi
* Applies Execution Profile
* Learns from previous runs
* Applies adaptive bias

---

## Example: Automation Flow

```python
import pyautogui
from nano_wait import wait

pyautogui.click(100, 200)
wait()

pyautogui.write("Hello")
wait()

pyautogui.press("enter")
```

---

# ⚡ Async Condition Waiting

```python
import asyncio
from nano_wait import wait_async

async def main():
    result = await wait_async(lambda: check_ready(), timeout=5)
    print(result)

asyncio.run(main())
```

Works seamlessly in:

* FastAPI
* Async bots
* Scrapers
* Async task queues

---

# 💡 Quick Start

### Standard Adaptive Time Wait

```python
from nano_wait import wait

wait(5)
```

### Deterministic Condition Wait

```python
wait(lambda: database_ready(), timeout=10)
```

---

# 🌐 Parallel Execution (`wait_pool`)

```python
from nano_wait import wait_pool

results = wait_pool([1, 2, 3])
```

---

# ⚙️ Core API Reference

| Function          | Sync | Async | Condition | Parallel | Cancelable |
| ----------------- | :--: | :---: | :-------: | :------: | :--------: |
| `wait`            |   ✅  |   ❌   |     ✅     |     ❌    |      ❌     |
| `wait_async`      |   ❌  |   ✅   |     ✅     |     ❌    |      ❌     |
| `wait_pool`       |   ✅  |   ❌   |     ❌     |     ✅    |      ✅     |
| `wait_pool_async` |   ❌  |   ✅   |     ❌     |     ✅    |      ✅     |
| `wait_auto`       |   ✅  |   ❌   |     ❌     |     ❌    |      ❌     |

---

# 🛠 Installation

```bash
pip install nano_wait
```

### Required Dependencies

```bash
pip install psutil pywifi
```

---

# 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.