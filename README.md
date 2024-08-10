# Nano-Wait Library Documentation

## Overview

The Nano-Wait library is designed to automate PC tasks by dynamically calculating the wait time between actions based on system performance and WiFi signal strength. This library is particularly useful for scripting and automation tasks where timing is critical, and variations in system resources and network conditions can impact the execution of actions.

## Installation

To use the Nano-Wait library, ensure that the necessary dependencies are installed:
```bash
pip install pywifi psutil
```

## Initialization

Before using the Nano-Wait library, you need to create an instance of the PCAutomation class. This instance will provide methods to calculate wait times based on your PC's performance and WiFi signal strength.

```
from biblioteca import PCAutomation

# Initialize the automation
automation = PCAutomation()
```
## Parameters

speed
Type: int
Range: 1 to 10
Description: This parameter controls the desired speed of automation. A value of 1 represents the slowest speed with the longest wait times, while a value of 10 represents the fastest speed with the shortest wait times. Adjust this parameter based on your specific requirements and system performance.

## Main Functions

wait_wifi(speed)
Description: Calculates the necessary wait time between actions when considering both PC performance and WiFi signal strength.
Parameters:
speed (int): A value between 1 and 10 that controls the speed of automation.
Returns: The calculated wait time in seconds as a float.

Below is an example of how to use the Nano-Wait library in a Python automation script:

```
import pyautogui
import time
from biblioteca import PCAutomation

# Initialize the automation
automation = PCAutomation()

# Set the desired speed of automation
speed = 1

# Press the Windows key and wait for the appropriate time
wait_time = automation.wait_n_wifi(speed=speed)
pyautogui.press('win')
time.sleep(wait_time)

# Type 'chrome' and wait for the appropriate time
wait_time = automation.wait_n_wifi(speed=speed)
pyautogui.write('chrome', interval=0.1)
time.sleep(wait_time)

# Press 'Enter' to open Chrome and wait for the appropriate time
wait_time = automation.wait_wifi(speed=speed)
pyautogui.press('enter')
time.sleep(wait_time)  # Wait for Chrome to open

# Type the URL of YouTube and wait for the appropriate time
wait_time = automation.wait_wifi(speed=speed)
pyautogui.write('youtube.com', interval=0.1)
time.sleep(wait_time)

# Press 'Enter' to go to YouTube and wait for the appropriate time
wait_time = automation.wait_n_wifi(speed=speed)
pyautogui.press('enter')
Detailed Functionality
get_wifi_signal()
Description: Scans the available WiFi networks and returns a score (0-10) based on the signal strength of a specified WiFi network.
Internal Usage: Used within the wait_wifi function to determine the WiFi score.
get_pc_score()
Description: Computes a score (0-10) based on CPU and memory usage, indicating the PC's performance.
Internal Usage: Used within both wait_wifi and wait_n_wifi functions to determine the PC performance score.
Conclusion
The Nano-Wait library provides a simple yet powerful way to manage wait times in PC automation scripts by dynamically adjusting based on system and network conditions. By configuring the speed parameter, users can control the pace of automation to match their specific needs.
```