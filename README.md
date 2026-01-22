# NanoWait: The Adaptive Wait Engine for Python

[![PyPI version](https://img.shields.io/pypi/v/nano_wait.svg)](https://pypi.org/project/nano-wait/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/nano_wait.svg)](https://pypi.org/project/nano-wait/)

**NanoWait** is a deterministic and adaptive execution wait engine designed to replace Python's standard `time.sleep()`. Instead of waiting for a fixed duration, NanoWait dynamically adjusts the wait time based on **system load (CPU/RAM)** and, optionally, **Wi-Fi signal strength**, ensuring automation scripts remain reliable even in slow or overloaded environments.

With the introduction of **Execution Profiles**, NanoWait now offers a semantic layer to manage wait behavior, allowing you to define the operational context clearly and consistently.

> **In summary:** You request a base time (e.g., `wait(5)`), and NanoWait ensures a *safe and context-aware wait* that never exceeds the requested time and never falls below a minimum execution floor.

### Cross-Platform Stability & Headless Environments

NanoWait has undergone significant structural modifications focused on **cross-platform stability**, especially for macOS, and **safe usage in headless environments** (CI, RPA, servers). It explicitly differentiates between graphical and headless modes. In headless environments, no graphical UI is instantiated, preventing crashes like `NSWindow should only be instantiated on the main thread` on macOS with Tkinter issues. This ensures total stability in macOS, CI/CD pipelines, and remote execution.

---

## 🚀 Key Features

- **Adaptive Waiting:** Dynamically scales wait times based on real-time system metrics.
- **Execution Profiles:** Semantic presets for CI, RPA, Testing, and more.
- **Async Support:** Native `wait_async` for non-blocking execution in `asyncio` environments.
- **Parallel Execution:** `wait_pool` and `wait_pool_async` for handling multiple waits concurrently.
- **Cross-Platform Stability:** Optimized for macOS and headless environments (CI/CD, Docker).
- **Explain Mode:** Auditable decision reports for full transparency.
- **CLI Support:** Powerful command-line interface for quick tasks.
- **Local Telemetry:** Opt-in system for analyzing wait behavior without remote data collection.

---

## 🛠️ Installation

Install the core package via pip:

```bash
pip install nano_wait
```

### Required Dependencies
For adaptive features (CPU/RAM/Wi-Fi awareness) to function, install the following:

```bash
pip install psutil pywifi
```

### Optional Module — Vision Mode
Visual waiting (icon/state detection) is available in a dedicated package to keep the core engine lightweight:

```bash
pip install nano-wait-vision
```
*Note: If Vision Mode is not installed, NanoWait will raise a clear runtime error when visual functionalities are requested.*

---

## 💡 Quick Start

### Standard vs. Adaptive Wait
```python
from nano_wait import wait
import time

# Adaptive wait (Up to 5 seconds, adjusted by system load)
start = time.time()
wait(5)
print(f"nano_wait.wait(): {time.time() - start:.2f}s")
```
*NanoWait **never waits longer than the requested base time** and applies a minimum internal delay of **50 ms** to prevent excessive CPU usage.*

---

## ⚡️ Asynchronous Support (`wait_async`)

NanoWait is fully compatible with asynchronous environments like **FastAPI**, **asyncio-based bots**, and **web scrapers**. The `wait_async` function is non-blocking, ensuring the event loop remains free.

### Usage in Async Code (Concise Example)
```python
import asyncio
from nano_wait import wait_async

async def main():
    # Non-blocking wait for up to 2 seconds
    result = await wait_async(2, smart=True)
    print(f"Wait finished in: {result:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())
```
> **Note:** `wait_async` internally uses `asyncio.to_thread` to run the synchronous adaptive logic in a separate thread, ensuring true non-blocking behavior for the event loop.

---

## 🌐 Parallel Execution (`wait_pool`)

Run multiple adaptive waits in parallel—ideal for batch automation or concurrent UI interactions.

### Execution Comparison (Simulated Times)

| Function | Execution Type | Parallel? | Total Time (Simulated) | Use Case |
| :--- | :--- | :---: | :--- | :--- |
| `wait(1) + wait(2)` | Synchronous | ❌ | ~3.0s | Simple, sequential tasks |
| `wait_async(1) + wait_async(2)` | Asynchronous | ❌ | ~3.0s | Sequential, non-blocking tasks |
| `wait_pool([1, 2])` | Synchronous Pool | ✅ | ~2.0s | Batch automation, concurrent tests |
| `wait_pool_async([1, 2])` | Asynchronous Pool | ✅ | ~2.0s | High-performance async scraping/bots |

### Conditional Cancellation (`cancel_if`)
You can skip waits based on custom conditions (e.g., high system load). If the callable passed to `cancel_if` returns `True`, the wait is skipped. This is available for both `wait_pool` and `wait_pool_async`.

| Condition | Function | Behavior | Result for Skipped Task |
| :--- | :--- | :--- | :--- |
| `cancel_if=callable` | `wait_pool` | Synchronous skip | `None` |
| `cancel_if=callable` | `wait_pool_async` | Asynchronous skip | `None` |

```python
import psutil
from nano_wait import wait_pool

# Function to cancel tasks if CPU load is over 80%
def heavy_load():
    return psutil.cpu_percent() > 80

# If heavy_load() returns True, the waits are skipped
results = wait_pool([1, 2, 3], cancel_if=heavy_load)
# Example output if cancelled: [None, None, None]
```

---

## ⚙️ Core API Reference

| Function | Sync | Async | Parallel | Cancelable |
| :--- | :---: | :---: | :---: | :---: |
| `wait` | ✅ | ❌ | ❌ | ❌ |
| `wait_async` | ❌ | ✅ | ❌ | ❌ |
| `wait_pool` | ✅ | ❌ | ✅ | ✅ |
| `wait_pool_async` | ❌ | ✅ | ✅ | ✅ |

### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `t` / `times` | `float` / `list` | **Required.** Base time(s) in seconds. |
| `smart` | `bool` | Activates Smart Context Mode (dynamic speed calculation). |
| `profile` | `str` | Selects a predefined profile (e.g., `"ci"`, `"rpa"`, `"testing"`). |
| `speed` | `str/int` | Execution speed preset or numeric value. |
| `wifi` | `str` | Wi-Fi SSID to assess signal quality (optional). |
| `explain` | `bool` | Returns a detailed `ExplainReport` object. |
| `verbose` | `bool` | Prints debug information to stdout. |
| `log` | `bool` | Writes execution data to `nano_wait.log`. |
| `headless` | `bool` | Forces headless mode, disabling graphical UI elements. |
| `callback` | `callable`| Function to execute after wait (sync or async). |
| `cancel_if` | `callable`| Condition to cancel wait (pool only). |

---

## 🧩 Execution Profiles

Execution Profiles introduce a semantic layer over NanoWait's adaptive wait engine. Instead of manually adjusting isolated parameters (speed, aggressiveness, verbosity), you can select an execution profile that represents the operational context.

### 🎯 Why use Execution Profiles?
Without profiles, scripts tend to accumulate fragile adjustments:
```python
wait(2, speed="fast", smart=True, verbose=True)
```
With Execution Profiles, the focus shifts to the environment, not mechanical details:
```python
wait(2, profile="ci")
```

### 🧪 Available Profiles

| Profile | Recommended Use | General Behavior |
| :--- | :--- | :--- |
| `ci` | CI/CD Pipelines | Aggressive waits, verbose enabled |
| `testing` | Local Automated Tests | Balance between speed and stability |
| `rpa` | UI / Human Workflow | More conservative waits |
| `default` | Generic Execution | Balanced behavior |

### 🧠 What does an Execution Profile control?
Internally, each profile defines:
- Aggressiveness of time adaptation
- Tolerance to transient instabilities
- Polling interval
- Default verbosity (automatic debug)

---

## 🔬 Explain Mode (`explain=True`)

Explain Mode makes NanoWait's waiting mechanism deterministic, auditable, and explainable. It does not alter the wait behavior but **reveals how the decision was made**.

When activated, `wait()` returns an `ExplainReport` object containing:
- Requested vs. Final applied time
- Configured and resolved speed
- Smart Mode usage & CPU/Wi-Fi scores
- Adaptive factor & Execution profile

### Realistic Example Output
```python
from nano_wait import wait

# Simulating a wait with Smart Mode, a Profile, and Wi-Fi awareness
report = wait(
    t=1.5, 
    smart=True, 
    profile="rpa", 
    wifi="MyNetwork_5G", 
    explain=True
)
print(report.explain())
```

**Example `ExplainReport` output (simulated):**
```
--------------------------------------------------
NanoWait Explain Report
--------------------------------------------------
Requested Time: 1.5s
Final Wait Time: 0.98s (Adaptive)
Execution Profile: rpa
Smart Mode: True
Wi-Fi SSID: MyNetwork_5G
--------------------------------------------------
System Metrics:
  CPU Score: 0.75 (75% CPU load)
  Wi-Fi Score: 0.90 (Excellent signal)
  Adaptive Factor: 1.12
--------------------------------------------------
Decision: Wait time was reduced due to high CPU load,
but slightly increased by the conservative 'rpa' profile.
--------------------------------------------------
```

---

## 🧠 Smart Context Mode (`smart=True`)

When activated, NanoWait automatically calculates the execution speed based on the **average system context score**.

```python
wait(10, smart=True, verbose=True)
```

### How Smart Speed Works
- **PC Score:** Derived from CPU and memory usage.
- **Wi-Fi Score:** Derived from RSSI (if activated).

The final **Smart Speed** is calculated as:
`speed = clamp( (pc_score + wifi_score) / 2 , 0.5 , 5.0 )`

---

## 🌐 Wi-Fi Awareness

If your automation depends on network stability, NanoWait can adapt its waiting behavior based on Wi-Fi signal strength.

```python
wait(5, wifi="MyNetwork_5G")
```
*Supported platforms: Windows (`pywifi`), macOS (`airport`), Linux (`nmcli`).*

---

## 🖥️ Command Line Interface (CLI)

The CLI reflects 100% of the API's capabilities.

### CLI ↔ API Mapping

| API Parameter | CLI Flag | Description |
| :--- | :--- | :--- |
| `t` / `times` | Positional Args | Base time(s) |
| `smart=True` | `--smart` | Activates Smart Mode |
| `profile="ci"` | `--profile ci` | Selects Execution Profile |
| `explain=True` | `--explain` | Returns Explain Report |
| `verbose=True` | `--verbose` | Prints debug logs |
| `wait_async` | `--async` | Enables non-blocking execution |
| `wait_pool` | `--pool` | Enables parallel execution |

### Advanced CLI Examples

```bash
# 1. Asynchronous parallel execution (non-blocking pool)
nano-wait --async --pool 1 2 3 --verbose

# 2. Parallel execution with a cancellation condition (simulated)
# Note: cancel_if logic must be implemented in a wrapper script for CLI use.
# This example shows the pool execution with a profile.
nano-wait --pool 1 2 3 --profile rpa

# 3. Explain Mode with Smart Context and a Profile
nano-wait 5 --smart --profile ci --explain
```

---

## 📊 Local Telemetry (Opt-in)

NanoWait includes an experimental, **fully opt-in local telemetry system**. 
- **No remote data collection:** All data stays on your machine.
- **Records:** CPU score, Wi-Fi score, adaptive factor, and active profile.
- **Stability:** Internal improvements (renamed telemetry queue) ensure no conflicts on macOS or headless environments.

---

## 🛡️ Best Practices

1. **Prefer Profiles:** Use `profile="ci"` or `profile="rpa"` instead of manual speed settings for semantic clarity.
2. **Go Smart:** Use `smart=True` in unpredictable or shared environments.
3. **Headless First:** Explicitly use `headless=True` in Docker or CI to prevent unexpected UI instantiation.
4. **Async for Performance:** Use `wait_async` or `wait_pool_async` in `asyncio` applications to maintain non-blocking performance.
5. **Audit with Explain:** Use `explain=True` during development to understand how environmental factors influence delays.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
