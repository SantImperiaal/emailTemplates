
import pyautogui
import time

def move_mouse_pattern():
    print("Press Ctrl+C in the terminal to stop the mouse movement.")
    try:
        while True:
            # Get the current mouse position
            x, y = pyautogui.position()
            # Move right
            pyautogui.moveRel(100, 0, duration=0.5)
            time.sleep(0.5)
            # Move down
            pyautogui.moveRel(0, 100, duration=0.5)
            time.sleep(0.5)
            # Move left
            pyautogui.moveRel(-100, 0, duration=0.5)
            time.sleep(0.5)
            # Move up
            pyautogui.moveRel(0, -100, duration=0.5)
            time.sleep(0.5)
            # Perform a click
            pyautogui.click()
            print("Mouse moved and clicked. Waiting 2 minutes...")
            time.sleep(120)  # Wait for 2 minutes
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    move_mouse_pattern()
