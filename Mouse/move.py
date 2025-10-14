import pyautogui
import time
from datetime import datetime, timedelta

def move_mouse_pattern(duration_minutes=None):
    print("Press Ctrl+C in the terminal to stop the mouse movement.")
    start_time = datetime.now()
    if duration_minutes is not None:
        end_time = start_time + timedelta(minutes=duration_minutes)
        print(f"Mouse movement will stop after {duration_minutes} minutes.")
    else:
        end_time = None

    try:
        while True:
            if end_time and datetime.now() >= end_time:
                print("Specified duration reached. Stopping mouse movement.")
                break
            # Move in a small square
            pyautogui.moveRel(20, 0, duration=0.2)
            time.sleep(0.2)
            pyautogui.moveRel(0, 20, duration=0.2)
            time.sleep(0.2)
            pyautogui.moveRel(-20, 0, duration=0.2)
            time.sleep(0.2)
            pyautogui.moveRel(0, -20, duration=0.2)
            time.sleep(0.2)
            pyautogui.click()
            elapsed = datetime.now() - start_time
            elapsed_minutes = elapsed.total_seconds() // 60
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mouse moved in a small square and clicked. Elapsed time: {int(elapsed_minutes)} minutes. Waiting 2 minutes...")
            time.sleep(120)  # Wait for 2 minutes
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    # Ask user for duration
    user_input = input("Enter duration in minutes (or press Enter for infinite): ")
    if user_input.strip():
        try:
            duration = int(user_input)
        except ValueError:
            print("Invalid input. Using infinite duration.")
            duration = None
    else:
        duration = None
    move_mouse_pattern(duration_minutes=duration)