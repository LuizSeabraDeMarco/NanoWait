# 🚀 NanoWait — Adaptive Execution Engine for Python

**NanoWait is not a sleep function.
It’s an adaptive execution engine.**

> Execute. Retry. Adapt. Learn.

---

# 📦 Installation

```bash
pip install nano-wait
```

---

# ⚡ Quick Start

## 1. Smart Wait (better than sleep)

```python
from nano_wait import wait

wait(2)  # adapts to your CPU, memory and Wi-Fi
```

---

## 2. Wait until something happens

```python
wait(lambda: button_is_visible(), timeout=10)
```

---

## 3. Execution Engine (🔥 core feature)

```python
from nano_wait import execute

result = execute(lambda: fetch_data())

print(result.success)
```

---

## 4. Retry (clean and powerful)

```python
from nano_wait import retry

@retry(timeout=5)
def click_button():
    return driver.click("#submit")
```

---

## 5. 🤖 Agent (NEW — experimental)

```python
from nano_wait import Agent

agent = Agent(verbose=True)
agent.run("click login")
```

> High-level automation layer (future AI-ready interface)

---

# 🧠 Core Concepts

## 1. Adaptive Wait

NanoWait dynamically adjusts timing based on:

* CPU usage
* Memory pressure
* Wi-Fi signal
* Execution profile
* Historical learning

---

## 2. Execution Engine

NanoWait doesn’t just wait — it **executes with intelligence**:

```python
execute(
    fn,
    timeout=10,
    interval=0.2
)
```

---

## 3. Scheduler

Internally:

```python
schedule(interval)
```

→ replaces `time.sleep()` with adaptive timing.

---

## 4. Agent Layer (NEW)

```python
agent.run("click login button")
```

NanoWait is evolving into:

> 🧠 a system that **observes → decides → acts**

---

# 🔁 API Reference

---

## `wait()`

```python
wait(
    t: float | Callable | None,
    timeout: float = 15.0,
    wifi: str | None = None,
    speed: str | float = "normal",
    smart: bool = False,
    verbose: bool = False,
    log: bool = False,
    explain: bool = False,
    telemetry: bool = False,
    profile: str | None = None
)
```

---

### Modes

#### ⏱ Time Mode

```python
wait(2)
```

#### 🔄 Condition Mode

```python
wait(lambda: is_ready(), timeout=10)
```

---

## `execute()` ⭐

```python
execute(
    fn,
    timeout=10,
    interval=0.2,
    profile=None,
    verbose=False
)
```

---

### Example

```python
def fetch():
    return api.get_data()

result = execute(fetch, timeout=5)
```

---

### Return

```python
ExecutionResult(
    success=True,
    result=...,
    attempts=3,
    duration=1.23
)
```

---

## `retry`

```python
@retry(timeout=5, interval=0.2)
def connect():
    return connect_to_server()
```

---

## `Agent` (experimental)

```python
agent = Agent()
agent.run("wait")
agent.run("click submit")
```

---

# ⚙️ Execution Profiles

```python
profile="ci"       # fast & aggressive
profile="testing"  # balanced
profile="rpa"      # stable & safe
```

---

# 🧠 Smart Mode

```python
wait(2, smart=True)
```

Automatically adapts to:

* slow machines → longer waits
* fast machines → shorter waits

---

# 📊 Telemetry

```python
wait(2, telemetry=True)
```

Displays:

* adaptive factor
* intervals
* real-time adjustments

---

# 🧪 Explain Mode

```python
report = wait(2, explain=True)
print(report)
```

Returns:

* final wait time
* adaptive factor
* CPU/Wi-Fi scores
* internal decisions

---

# 🤖 CLI

## Basic

```bash
nano-wait 2
```

---

## Async

```bash
nano-wait 2 --async
```

---

## Pool

```bash
nano-wait --pool 1 2 3
```

---

## Auto

```bash
nano-wait --auto
```

---

## ⚙️ Execution

```bash
nano-wait --exec "lambda: 1+1"
```

---

## 🤖 Agent (NEW)

```bash
nano-wait --agent "click login"
```

---

# 🧩 Real Use Cases

---

## Selenium / Playwright

```python
execute(
    lambda: driver.find_element("#btn").click(),
    timeout=5
)
```

---

## API Retry

```python
execute(
    lambda: requests.get(url),
    timeout=5
)
```

---

## RPA

```python
@retry(timeout=10)
def open_app():
    click_icon()
```

---

# 🧠 Learning Engine

NanoWait learns from execution:

* delays
* failures
* timeouts

Improving future runs automatically.

Stored at:

```bash
~/.nano_wait_learning.json
```

---

# 🔥 Why NanoWait?

Most systems separate:

* `time.sleep()` ❌
* retry ❌
* polling ❌

NanoWait unifies everything:

✅ Adaptive Scheduler
✅ Execution Engine
✅ Learning System
✅ Telemetry
✅ Agent Layer (new)

---

# 🚀 Roadmap

* [ ] AI-powered Agent (LLM integration)
* [ ] Vision integration (`nano-wait-vision`)
* [ ] execute_async
* [ ] circuit breaker
* [ ] error classification

---

# 💡 Philosophy

> “Don’t wait blindly.
> Execute intelligently.”

---

# ⚡ Final insight (isso aqui é o diferencial real)

NanoWait is evolving from:

> a timing utility

to:

> 🧠 an adaptive execution system for real-world automation

---