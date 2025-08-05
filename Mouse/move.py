import pyautogui
import time
from datetime import datetime

def move_mouse_pattern():
    print("Press Ctrl+C in the terminal to stop the mouse movement.")
    try:
        while True:
            # Get the current mouse position
            x, y = pyautogui.position()
            # Move right (smaller movement)
            pyautogui.moveRel(20, 0, duration=0.2)
            time.sleep(0.2)
            # Move down
            pyautogui.moveRel(0, 20, duration=0.2)
            time.sleep(0.2)
            # Move left
            pyautogui.moveRel(-20, 0, duration=0.2)
            time.sleep(0.2)
            # Move up
            pyautogui.moveRel(0, -20, duration=0.2)
            time.sleep(0.2)
            # Perform a click
            pyautogui.click()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mouse moved in a small square and clicked. Waiting 2 minutes...")
            time.sleep(120)  # Wait for 2 minutes
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    move_mouse_pattern()