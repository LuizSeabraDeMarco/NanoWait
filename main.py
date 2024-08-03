import pywifi
import time
import pyautogui
import psutil
import keyboard
from pywifi import const
from datetime import datetime

def get_wifi_signal_strength():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    scan_results = iface.scan_results()
    if not scan_results:
        return -100
    best_signal = scan_results[0].signal
    return best_signal

def calculate_wait_time(signal_strength):
    if signal_strength > -50:
        return 2
    elif signal_strength > -70:
        return 4
    else:
        return 6

def evaluate_pc_performance():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    if cpu_usage < 50 and memory_info.available > (memory_info.total * 0.5):
        return 0.5
    elif cpu_usage < 75 and memory_info.available > (memory_info.total * 0.25):
        return 1
    else:
        return 1.5

def calculate_combined_wait_time():
    performance_wait_time = evaluate_pc_performance()
    signal_strength = get_wifi_signal_strength()
    network_wait_time = calculate_wait_time(signal_strength)
    return performance_wait_time + network_wait_time

def open_application(app_name, risk_level):
    performance_wait_time = evaluate_pc_performance() * (1 - risk_level / 100)
    pyautogui.press('win')
    time.sleep(performance_wait_time)
    pyautogui.write(app_name)
    time.sleep(performance_wait_time)
    pyautogui.press('enter')
    time.sleep(performance_wait_time)

def open_url(url, risk_level):
    combined_wait_time = calculate_combined_wait_time() * (1 - risk_level / 100)
    if risk_level >= 75:
        pyautogui.write(url)
        pyautogui.press('enter')
    else:
        time.sleep(combined_wait_time)
        pyautogui.write(url)
        pyautogui.press('enter')

def click_position(x, y, clicks=1, interval=0.0):
    pyautogui.click(x, y, clicks=clicks, interval=interval)

def type_text(text):
    pyautogui.write(text)

def click_shortcut(shortcut):
    if isinstance(shortcut, list):
        pyautogui.hotkey(*shortcut)
    else:
        pyautogui.press(shortcut)

def press_tab(times):
    for _ in range(times):
        pyautogui.press('tab')

def show_risk_level(risk_level):
    if risk_level == 100:
        return "Risk 100%: Focus on speed, not on ensuring functionality."
    elif risk_level >= 75:
        return f"Risk {risk_level}%: High priority for speed."
    elif risk_level >= 50:
        return f"Risk {risk_level}%: Balanced between speed and precision."
    elif risk_level >= 25:
        return f"Risk {risk_level}%: High priority for precision."
    else:
        return f"Risk {risk_level}%: Full focus on precision."

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def wait_time(seconds):
    time.sleep(seconds)

def evaluate_wifi_quality(signal_strength):
    if signal_strength > -50:
        return 10
    elif signal_strength > -60:
        return 8
    elif signal_strength > -70:
        return 6
    elif signal_strength > -80:
        return 4
    else:
        return 2

def evaluate_pc_performance_rating(cpu_usage, memory_info):
    if cpu_usage < 20 and memory_info.available > (memory_info.total * 0.8):
        return 10
    elif cpu_usage < 40 and memory_info.available > (memory_info.total * 0.6):
        return 8
    elif cpu_usage < 60 and memory_info.available > (memory_info.total * 0.4):
        return 6
    elif cpu_usage < 80 and memory_info.available > (memory_info.total * 0.2):
        return 4
    else:
        return 2

def open_notepad():
    open_application("notepad", 0)

def paste_to_notepad():
    pyautogui.hotkey('ctrl', 'v')

def check_interruption():
    """
    Checks if the interruption shortcut 'Esc + Ctrl' is pressed.
    """
    return keyboard.is_pressed('esc') and keyboard.is_pressed('ctrl')

if __name__ == "__main__":
    while True:
        if check_interruption():
            print("Interruption detected. Stopping automation.")
            break
        
        start_time = get_current_time()
        risk_level = 80
        print(show_risk_level(risk_level))
        
        # Open Chrome
        open_application("chrome", risk_level)
        time.sleep(calculate_combined_wait_time())  # Wait for Chrome to fully open

        # Check for interruption
        if check_interruption():
            print("Interruption detected. Stopping automation.")
            break
        
        # Open a new tab and navigate to YouTube
        pyautogui.hotkey('ctrl', 't')  # Open a new tab
        time.sleep(calculate_combined_wait_time())  # Wait for the new tab to open
        pyautogui.write("https://www.youtube.com")
        pyautogui.press('enter')
        
        # Check for interruption
        if check_interruption():
            print("Interruption detected. Stopping automation.")
            break
        
        # Wait for the page to load
        wait_time(calculate_combined_wait_time())

        # Check for interruption
        if check_interruption():
            print("Interruption detected. Stopping automation.")
            break
        
        # Press Tab 10 times
        press_tab(10)

        # Press Enter
        pyautogui.press('enter')

        # Press Ctrl + A to select all text
        pyautogui.hotkey('ctrl', 'a')
        
        # Press Ctrl + C to copy the selected text
        pyautogui.hotkey('ctrl', 'c')

        # Open Notepad
        open_notepad()
        
        # Wait for Notepad to open
        wait_time(2)

        # Paste the copied content into Notepad
        paste_to_notepad()
        
        end_time = get_current_time()
        signal_strength = get_wifi_signal_strength()
        performance_wait_time = evaluate_pc_performance()
        
        wifi_quality = evaluate_wifi_quality(signal_strength)
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        pc_performance_rating = evaluate_pc_performance_rating(cpu_usage, memory_info)

        print(f"All time: {end_time}")
        print(f"WiFi signal strength: {signal_strength} dBm (Quality rating: {wifi_quality})")
        print(f"PC performance rating: {pc_performance_rating}")
        print(f"Performance wait time: {performance_wait_time} seconds")
        print(f"Combined wait time: {calculate_combined_wait_time()} seconds")
