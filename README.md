# NanoWait: The Adaptive Wait Engine for Python

[![PyPI version](https://img.shields.io/pypi/v/nano_wait.svg)](https://pypi.org/project/nano_wait/)
[![License](https://img.shields.io/pypi/l/nano_wait.svg)](https://github.com/luizfilipe/NanoWait/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/nano_wait.svg)](https://pypi.org/project/nano_wait/)

## 🚀 What is NanoWait?

**NanoWait** is a deterministic and adaptive execution wait engine designed to replace Python's standard `time.sleep()`. Instead of waiting for a fixed duration, NanoWait dynamically adjusts the wait time based on **system load (CPU/RAM)** and, optionally, **Wi-Fi signal strength**, ensuring automation scripts remain reliable even in slow or overloaded environments.

With the introduction of **Execution Profiles**, NanoWait now offers a semantic layer to manage wait behavior, allowing you to define the operational context clearly and consistently.

> **In summary:** you request a base time (e.g., `wait(5)`), and NanoWait ensures a *safe and context-aware wait* that never exceeds the requested time and never falls below a minimum execution floor.

### Cross-Platform Stability & Headless Environments

NanoWait has undergone significant structural modifications focused on **cross-platform stability**, especially for macOS, and **safe usage in headless environments** (CI, RPA, servers). It explicitly differentiates between graphical and headless modes. In headless environments, no graphical UI is instantiated, preventing crashes like `NSWindow should only be instantiated on the main thread` on macOS with Tkinter issues. This ensures total stability in macOS, CI/CD pipelines, and remote execution.

---

## 🛠️ Installation

```bash
pip install nano_wait
```

### Required Dependencies

For the adaptive features (CPU/RAM/Wi-Fi awareness) to function, the following dependencies are necessary:

```bash
pip install psutil pywifi
```

### Optional Module — Vision Mode

Visual waiting (icon/state detection) has been intentionally moved to a dedicated package to keep NanoWait lightweight and deterministic.

```bash
pip install nano-wait-vision
```

If Vision Mode is not installed, NanoWait will raise a clear runtime error when visual functionalities are requested.

---

## 💡 Quick Guide

```python
from nano_wait import wait
import time

# Standard sleep
start = time.time()
time.sleep(5)
print(f"time.sleep(): {time.time() - start:.2f}s")

# Adaptive wait
start = time.time()
wait(5)
print(f"nano_wait.wait(): {time.time() - start:.2f}s")
```

NanoWait **never waits longer than the requested base time** and applies a minimum internal delay of **50 ms** to prevent excessive CPU usage.

---

## ⚡️ Asynchronous Support (`wait_async`)

NanoWait now offers full compatibility with asynchronous environments like **FastAPI**, **asyncio-based bots**, and **async scraping** tools. The new function, `wait_async`, is a non-blocking version of `wait()`, ensuring that the main thread or event loop remains free to process other tasks while the adaptive wait is executed.

This change is crucial for high-performance applications where blocking the event loop is unacceptable.

### Usage in Async Code with Callbacks

The `wait_async` function allows you to pass an optional `callback`, either synchronous or asynchronous, to be executed after the wait completes or after a visual condition is detected.

```python
import asyncio
from nano_wait import wait_async

# Async callback example
async def async_callback():
    print("Async callback executed!")

# Normal (sync) callback example
def normal_callback():
    print("Normal callback executed!")

async def main():
    print("Starting non-blocking wait with callback...")
    result = await wait_async(
        2,                          # base wait time
        verbose=True,
        callback=async_callback     # can be async or normal function
    )
    print(f"Wait finished. Result: {result:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())
```

> **Note:** `wait_async` internally uses `asyncio.to_thread` (or `loop.run_in_executor` in older Python versions) to run the synchronous adaptive logic in a separate thread, ensuring true non-blocking behavior for the event loop.

---

## ⚙️ Core API

NanoWait now exposes two primary functions: `wait` (synchronous) and `wait_async` (asynchronous). Both share the same signature and adaptive logic.

### `wait` (Synchronous)

```python
wait(
    t: float | None = None,
    *,
    wifi: str | None = None,
    speed: str | float = "normal",
    smart: bool = False,
    explain: bool = False,
    verbose: bool = False,
    log: bool = False,
    profile: str | None = None,
    headless: bool = False
) -> float | ExplainReport
```

### `wait_async` (Asynchronous)

```python
async def wait_async(
    t: float | None = None,
    *,
    wifi: str | None = None,
    speed: str | float = "normal",
    smart: bool = False,
    explain: bool = False,
    verbose: bool = False,
    log: bool = False,
    profile: str | None = None,
    headless: bool = False,
    callback: None | callable = None # <-- Added callback parameter
) -> float | ExplainReport
```

### Parameters

| Parameter | Description |
|---|---|
| `t` | Base time in seconds (required for time-based waiting). |
| `wifi` | Wi-Fi network SSID to assess signal quality (optional). |
| `speed` | Execution speed preset or numeric value. |
| `smart` | Activates Smart Context Mode (dynamic speed calculation). |
| `explain` | Activates Explain Mode, which returns a detailed decision report. |
| `verbose` | Prints debug information to `stdout`. |
| `log` | Writes execution data to `nano_wait.log`. |
| `profile` | Selects a predefined execution profile (e.g., "ci", "rpa"). |
| `headless`| Explicitly forces headless mode, disabling graphical UI elements. |
| `callback`| Optional function to be executed after the wait completes; can be sync or async. |

---

## 🧩 Execution Profiles

Execution Profiles introduce a semantic layer over NanoWait's adaptive wait engine. Instead of manually adjusting isolated parameters (speed, aggressiveness, verbosity), you can select an execution profile that represents the operational context in which your code is running — such as continuous integration (CI), automated tests, or robotic process automation (RPA).

Each profile encapsulates a coherent set of decisions, ensuring consistency, readability, and reduced cognitive complexity for the user.

### 🎯 Why use Execution Profiles?

Without profiles, scripts tend to accumulate fragile adjustments:

```python
wait(2, speed="fast", smart=True, verbose=True)
```

With Execution Profiles, the focus shifts to the environment, not mechanical details:

```python
wait(2, profile="ci")
```

### ⚙️ How to use

Basic usage:

```python
from nano_wait import wait

# Executes the wait using the Continuous Integration profile
wait(2, profile="ci")
```

If no profile is specified, NanoWait uses the default profile.

### 🧪 Available Profiles

| Profile | Recommended Use | General Behavior |
|---|---|---|
| `ci` | CI/CD Pipelines | Aggressive waits, verbose enabled |
| `testing` | Local Automated Tests | Balance between speed and stability |
| `rpa` | Interface and Human Workflow Automation | More conservative waits |
| `default` | Generic Execution | Balanced behavior |

### 🧠 What does an Execution Profile control?

Internally, each profile defines:

*   Aggressiveness of time adaptation
*   Tolerance to transient instabilities
*   Polling interval
*   Default verbosity (automatic debug)

These parameters are applied deterministically to each execution.

### 🔄 Integration with Smart Context Mode

Execution Profiles do not replace Smart Context Mode — they complement each other.

```python
wait(
    t=3,
    smart=True,
    profile="testing"
)
```

In this example:

*   Smart Mode calculates the optimal speed based on the system
*   The Execution Profile adjusts the overall wait behavior

### 🧪 Comparative Example

Without Execution Profiles:

```python
wait(
    t=2,
    speed="fast",
    smart=True,
    verbose=True
)
```

With Execution Profiles:

```python
wait(
    t=2,
    profile="ci"
)
```

The second example is more readable, more consistent, and less fragile to future changes.

---

## 🔬 Explain Mode (`explain=True`)

Explain Mode makes NanoWait's waiting mechanism deterministic, auditable, and explainable. It does not alter the wait behavior but **reveals how the decision was made**.

When activated, `wait()` (or `wait_async`) returns an `ExplainReport` object. This report contains all factors used in the calculation, ideal for debugging, auditing, and benchmarking. The `ExplainReport` includes:

*   Requested time
*   Final applied time
*   Configured and resolved speed
*   Smart Mode usage
*   CPU score
*   Wi-Fi score
*   Adaptive factor
*   Application of minimum floor or maximum cap
*   Execution timestamp

This makes the wait behavior fully auditable and reproducible, providing total transparency for critical environments.

### Code Example

```python
from nano_wait import wait

report = wait(
    t=1.5,
    speed="fast",
    smart=True,
    explain=True
)

print(report.explain()) # Use .explain() method for a formatted string output
```

**Example `ExplainReport` output (simplified):**

```
Requested time: 1.5s
Final wait time: 0.7s
Speed input: fast -> 0.5
Smart mode: True
CPU score: 0.62
Adaptive factor: 1.39
Execution profile: default
```

---

## 🧠 Smart Context Mode (`smart=True`)

When activated, NanoWait automatically calculates the execution speed based on the **average system context score**.

```python
wait(10, smart=True, verbose=True)
```

Example output:

```
[NanoWait] speed=3.42 factor=2.05 wait=4.878s
```

### How Smart Speed Works

*   **PC Score** → derived from CPU and memory usage.
*   **Wi-Fi Score** → derived from RSSI (if activated).

The final **Smart Speed** is:

```
speed = clamp( (pc_score + wifi_score) / 2 , 0.5 , 5.0 )
```

This value is used directly as the execution speed factor.

---

## 🌐 Wi-Fi Awareness

If your automation depends on network stability, NanoWait can adapt its waiting behavior based on Wi-Fi signal strength.

```python
wait(5, wifi="MyNetwork_5G")
```

Supported platforms:

*   Windows (`pywifi`)
*   macOS (`airport`)
*   Linux (`nmcli`)

---

## 🖥️ Command Line Interface (CLI)

The CLI has been updated to reflect 100% of the API's capabilities, making the tool easy to test, debug, and use in real scripts.

**New Feature: Asynchronous Execution**

The CLI now supports a non-blocking execution mode using the new `--async` flag:

```bash
# Asynchronous wait with verbose output
python3 -m nano_wait.cli 2 --async --verbose
```

**CLI can be executed locally via:**

```bash
python -m nano_wait.cli 3
```

**Or as an installed command:**

```bash
nano-wait 3 --smart --explain
```

**Supported flags:**

*   `--smart`
*   `--speed`
*   `--wifi`
*   `--verbose`
*   `--log`
*   `--explain`
*   `--telemetry` (for local telemetry activation)
*   `--profile`
*   `--headless`
*   **`--async`** (New)

---

## 📊 Local Telemetry (Opt-in, No Remote Collection)

NanoWait now includes an experimental, **fully opt-in local telemetry system**. There is **no remote data collection or transmission**.

**Stability Improvement:** The internal import for the telemetry queue has been renamed (`import queue as std_queue`) to prevent potential conflicts and `AttributeError` issues, particularly on macOS.

Telemetry records:

*   `cpu_score`
*   `wifi_score`
*   `adaptive factor`
*   `intervals`
*   Active `profile`

In graphical mode (when applicable), a local dashboard might be available. In headless mode, the UI is automatically deactivated. The objective is to allow analysis of wait behavior without compromising security or portability.

---

## 🛡️ Best Practices & Recommendations

1.  **Use Profiles:** Prefer `wait(2, profile="testing")` over `wait(2, speed="fast")` for semantic clarity and robustness.
2.  **Smart Mode in Production:** Activate `smart=True` in environments where CPU load is unpredictable to ensure adaptive waiting.
3.  **Audit with Explain:** Use `explain=True` during debugging or intermittent test failures to understand how environmental factors influenced the wait duration.
4.  **Explicit Headless:** When running in Docker, CI, or on servers without a display, explicitly use the `--headless` flag in the CLI or the `headless=True` parameter in the API to prevent unexpected UI attempts.
5.  **Async for Web/Bots:** Use `await wait_async(...)` in any application that relies on an `asyncio` event loop (FastAPI, aiohttp, etc.) to maintain non-blocking performance.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
