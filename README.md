"""
nano_wait.py

Official Nano-Wait Library: Precise and Adaptive Waiting in Python ⚡

Description: This library allows you to perform adaptive waiting based on the current performance of your computer

### 📦 Installation


⚠️ To download it is necessary to have two libraries to work, run in the terminal 'pip install psutil pywifi⚠️ 

### Compatibility

⚠️ Compatibility: For now it only works on Windows, we are working on it now :) ⚠️ 

### Version

Version: 1.2
License: MIT

### formulas

Formulas used in the NanoWait library:

1) PC Score Calculation:
Evaluates how "free" your computer is based on CPU and memory usage:: 

cpu_score = max(0, min(10, 10 - cpu_usage / 10)) 

memory_score = max(0, min(10, 10 - memory_usage / 10)) 

pc_score = (cpu_score + memory_score) / 2

2) Wi-Fi Score calculation:
Converts Wi-Fi signal strength (in dBm) to a scale of 0 to 10: 

wifi_score = max(0, min(10, (signal_strength + 100) / 10)) 

Example: If the signal is -60 dBm, 
wifi_score = (-60 + 100) / 10 = 4

3) Combined Risk Score Calculation (PC + Wi-Fi): 

risk_score = (pc_score + wifi_score) / 2

4) Wi-Fi standby time (wait_wifi): 

wait_time = max(1, (10 - risk_score) / speed)

5) Waiting time without Wi-Fi (wait_n_wifi): 

wait_time = max(1, (10 - pc_score) / speed)

Variable legend:

| Variable | Description |
|------------------|---------------------------------------|
| cpu_usage | Current CPU usage (%) |
| memory_usage | Current RAM usage (%) |
| signal_strength | Wi-Fi signal strength (in dBm) |
| speed | Speed factor (example: 1 to 10) |
"""

import pywifi
import psutil
import time


class NanoWait: 
""" 
Core class of the Nano-Wait library.
Allows you to calculate wait times based on the machine's current performance and Wi-Fi quality. 
""" 

def __init__(self): 
""" 
Initializes Wi-Fi modules, if available.
""" 
self.wifi = pywifi.PyWiFi() 
self.interface = self.wifi.interfaces()[0] 

def get_wifi_signal(self, ssid: str) -> float:7 

"""Returns a score from 0 to 10 based on the Wi-Fi signal strength for the given SSID. 

Args: 
ssid (str): Name of the Wi-Fi network to be analyzed. 

Returns: 
float: Wi-Fi quality rating between 0 (poor) and 10 (excellent). 
""" 
try: 
self.interface.scan() 
time.sleep(2) # Wait for the scan to complete 
scan_results = self.interface.scan_results() 

signal_strength = -100 # Default weak signal value 

for network in scan_results: 
if network.ssid == ssid: 
signal_strength = network.signal 
break 
else: 
raise ValueError(f"Wi-Fi network '{ssid}' not found.") 

wifi_score = max(0, min(10, (signal_strength + 100) / 10)) 
return wifi_score 

except Exception as e: 
print(f"[WiFi Error] {e}") 
return 0 

def get_pc_score(self) -> float: 
""" 
Returns a score from 0 to 10 based on current CPU and RAM usage. 

Returns: 
float: Rating between 0 (overload) and 10 (light performance). 
""" 
try: 
cpu_usage = psutil.cpu_percent(interval=1) 
memory_usage = psutil.virtual_memory().percent 

cpu_score = max(0, min(10, 10 - cpu_usage / 10)) 
memory_score = max(0, min(10, 10 - memory_usage / 10)) 

pc_score = (cpu_score + memory_score) / 2 
return pc_score 

except Exception as e:
print(f"[PC Score Error] {e}")
return 0

def wait_wifi(self, speed: float, ssid: str) -> float:
"""
Calculates the wait time based on PC performance and Wi-Fi quality.

Args:
speed (float): Speed factor. Higher values result in shorter wait times.
ssid (str): Name of the Wi-Fi network to be analyzed.

Returns:
float: Recommended wait time.
"""
try:
pc_score = self.get_pc_score()
wifi_score = self.get_wifi_signal(ssid)

risk_score = (pc_score + wifi_score) / 2
wait_time = max(1, (10 - risk_score) / speed)
return wait_time

except Exception as e:
print(f"[Wait_wifi Error] {e}")
return 1

def wait_n_wifi(self, speed: float) -> float:
"""
Calculates the wait time based only on the PC's performance (no Wi-Fi).

Args:
speed (float): Speed factor.

Returns:
float: Recommended wait time.
"""
try:
pc_score = self.get_pc_score()
wait_time = max(1, (10 - pc_score) / speed)
return wait_time

except Exception as e:
print(f"[Error wait_n_wifi] {e}")
return 1

def nano_wait(self, t: float, use_wifi: bool = False, ssid: str = "", speed: float = 1.5) -> None:
"""
Main library function. Adaptively waits for precisely t seconds.

The wait is divided between passive time (with time.sleep) and active time (status check).

Args:
t (float): Desired total wait time, in seconds.
use_wifi (bool): If True, considers the Wi-Fi network status in the analysis.
ssid (str): Wi-Fi network name (required if use_wifi=True).
speed (float): Adaptive speed. Higher values result in shorter waits.
"""
try:
if use_wifi:
if not ssid:
raise ValueError("SSID required when use_wifi=True")
wait_time = self.wait_wifi(speed, ssid)
else:
wait_time = self.wait_n_wifi(speed)

t_passive = max(0, t - wait_time)
t_active = min(t, wait_time)

time.sleep(t_passive)

start = time.time()
while (time.time() - start) < t_active:
continue # Active wait — ensures accuracy at the end of the wait

except Exception as e:
print(f"[Error nano_wait] {e}")
time.sleep(t) # fallback: simple wait

# Usage examples (to put in a separate file or test interactively):

# Usage example without Wi-Fi
# import time
# from nano_wait.nano_wait import NanoWait

# automation = NanoWait()
# speeds = 10
# wait_time = automation.wait_n_wifi(speed=speeds)
# time.sleep(wait_time)

# Usage example with Wi-Fi
# ssid = "WiFiNetworkName"
# wait_time = automation.wait_wifi(speed=speeds, ssid=ssid)
# time.sleep(wait_time)

# How much more efficient would it be?
# Efficiency Comparison: NanoWait vs. Fixed Wait (Guess)

This snippet mathematically explains how much the NanoWait library can improve wait time efficiency compared to a fixed wait performed by "guessing."

---

## Formula for calculating adaptive wait time (NanoWait)

For Wi-Fi, the wait time is calculated by:

\[
wait\_time = \max\left(min\_wait, \frac{10 - risk\_score}{speed}\right)
\]

Where:

- \( risk\_score = \frac{pc\_score + wifi\_score}{2} \) — combined score of the computer's performance and Wi-Fi network quality (varies between 0 and 10).
- \( speed \) — configurable factor that indicates the desired speed (higher values generate shorter wait times).
- \( min\_wait \) — minimum wait time allowed (example: 0.05 seconds).

---

## Percentage Gain Calculation

The percentage gain in efficiency, comparing the fixed wait \( t_{fixed} \) with the adaptive wait time \( wait\_time \), is:

\[
G = \frac{t_{fixed} - wait\_time}{t_{fixed}} \times 100\%
\]

---

## Example Scenarios

### Scenario A — Very Good PC and Wi-Fi

- \( pc\_score = 9 \)
- \( wifi\_score = 9 \)
- \( risk\_score = 9 \)
- \( speed = 10 \)
- \( min\_wait = 0.05 \) seconds

Calculating the wait time:

\[
wait\_time = \max(0.05, \frac{10 - 9}{10}) = \max(0.05, 0.1) = 0.1 \text{ seconds}
\]

If the fixed time is 0.2 seconds, the gain is:

\[
G = \frac{0.2 - 0.1}{0.2} \times 100\% = 50\%
\]

**Conclusion:** NanoWait halves the wait time.

---

### Scenario B — Reasonable PC and Poor Wi-Fi

- \( pc\_score = 5 \)
- \( wifi\_score = 3 \)
- \( risk\_score = 4 \)
- \( speed = 5 \)
- \( min\_wait = 0.05 \) seconds

Calculating the wait time:

\[
wait\_time = \max(0.05, \frac{10 - 4}{5}) = \max(0.05, 1.2) = 1.2 \text{ seconds}
\]

If the fixed time is 1 second, the gain is:

\[
G = \frac{1 - 1.2}{1} \times 100\% = -20\%
\]

**Conclusion:** Longer wait to ensure stability, which is important to avoid errors.

---

### Scenario C — Good PC, Average Wi-Fi

- \( pc\_score = 8 \)
- \( wifi\_score = 5 \)
- \( risk\_score = 6.5 \)
- \( speed = 10 \)
- \( min\_wait = 0.05 \) seconds

Calculating the wait time:

\[
wait\_time = \max(0.05, \frac{10 - 6.5}{10}) = \max(0.05, 0.35) = 0.35 \text{ seconds}
\]

If the fixed time is 0.5 seconds, the gain is:

\[
G = \frac{0.5 - 0.35}{0.5} \times 100\% = 30%
\]

**Conclusion:** 30% savings in total wait time.

---
## Summary

| Condition | Estimated Gain (%) |
|-------------------|-----------------------------------|
| Very good PC and Wi-Fi | Up to 50% reduction in wait time |
| Reasonable PC, poor Wi-Fi | Can increase the time for robustness |
| Good PC, average Wi-Fi | Approximately 20% to 35% savings |

---

## Practical Benefits of NanoWait

- **Adaptive time savings**: wait time decreases when the system is under stress.
- **Robustness**: time increases when the system is under stress, avoiding errors.
- **Customization**: the `speed` parameter allows you to adjust the behavior to your needs.

---

In other words, on average, it's a 20% to 50% increase in efficiency.

---

### ⚠️ Error Handling

The **Nano-Wait** library is designed with robust fallback mechanisms to ensure stability, even under unexpected conditions.

#### ✅ How the library behaves in case of failures:

| Scenario                        | Behavior                                                                 |
|---------------------------------|--------------------------------------------------------------------------|
| **Wi-Fi network not found**     | Returns a Wi-Fi score of `0` and logs: `[WiFi Error]`                   |
| **CPU or RAM usage unavailable**| Returns a PC score of `0` and logs: `[PC Score Error]`                  |
| **Unexpected internal error**   | Falls back to `time.sleep(t)` and logs: `[Error nano_wait]`            |

#### 🔐 Why this matters:

- Ensures **safe execution** even when the system is under high load or lacks necessary permissions.
- Avoids crashes by using default behaviors in case of unexpected conditions.
- Ideal for **automation scripts** and **real-time systems** that require reliability and resilience.

### Authors

Author: Luiz Filipe Seabra de Marco and Vitor Seabra
(and optionally the Wi-Fi network), ideal for applications that disable more intelligent waiting time control.Official Nano-Wait Library: Accurate and Adaptive Waiting in Python ⚡