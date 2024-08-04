import pyautogui
import time
from biblioteca import PCAutomation

# Initialize the automation
automation = PCAutomation()

# Define desired speed (1 to 10)
speed = 1

# Continue with the automation
# Press the Windows key
wait_time = automation.wait_n_wifi(speed=speed)
print(f"Wait Time (without WiFi) for pressing Windows: {wait_time} seconds")
pyautogui.press('win')
time.sleep(wait_time)

# Type 'chrome'
wait_time = automation.wait_n_wifi(speed=speed)
print(f"Wait Time (without WiFi) for typing 'chrome': {wait_time} seconds")
pyautogui.write('chrome', interval=0.1)
time.sleep(wait_time)

# Press 'Enter' to open Chrome
wait_time = automation.wait_wifi(speed=speed)
print(f"Wait Time (without WiFi) for pressing 'Enter': {wait_time} seconds")
pyautogui.press('enter')
time.sleep(wait_time)  # Wait for Chrome to open

# Type the URL of YouTube
wait_time = automation.wait_wifi(speed=speed)
print(f"Wait Time (with WiFi) for typing 'youtube.com': {wait_time} seconds")
pyautogui.write('youtube.com', interval=0.1)
time.sleep(wait_time)

# Press 'Enter' to go to YouTube
wait_time = automation.wait_n_wifi(speed=speed)
print(f"Wait Time (with WiFi) for pressing 'Enter': {wait_time} seconds")
pyautogui.press('enter')
