import keyboard
import time
import pyautogui

print("Press 1 key to record clicks, 2 key to record swipes, 3 key to record waits, 4 key to record text, "
      "5 key to record double clicks")

recorded_actions = []
start_time = time.time()
wait_start_time = None
swipe_start_time = None
swipe_start_pos = None
swipe_direction = None

while time.time() - start_time < 80:  # maximum recording time of 30 seconds
    if keyboard.is_pressed('1'):
        x, y = pyautogui.position()
        recorded_actions.append(f"click {x},{y}")
        print(f"Recorded click at ({x},{y})")
        time.sleep(0.1)  # wait for 100ms to avoid recording multiple clicks
        while keyboard.is_pressed('1'):  # wait for key release
            pass
    elif keyboard.is_pressed('2'):
        if len(recorded_actions) == 0 or not recorded_actions[-1].startswith('swipe'):
            x1, y1 = pyautogui.position()
            recorded_actions.append(f"swipe {x1},{y1}")
            print(f"Recorded swipe start position at ({x1},{y1})")
            time.sleep(0.1)  # wait for 100ms to avoid recording multiple swipes
            swipe_start_pos = (x1, y1)
            swipe_start_time = time.time()
            swipe_direction = None
        else:
            x2, y2 = pyautogui.position()
            recorded_actions[-1] += f" {x2},{y2}"
            print(f"Recorded swipe end position at ({x2},{y2})")
            time.sleep(0.1)  # wait for 100ms to avoid recording multiple swipes
            swipe_end_pos = (x2, y2)
            swipe_duration = time.time() - swipe_start_time
            swipe_distance = ((swipe_end_pos[0] - swipe_start_pos[0])**2 + (swipe_end_pos[1] - swipe_start_pos[1])**2)**0.5
            swipe_speed = swipe_distance / swipe_duration
            if swipe_distance > 0:
                dx = (swipe_end_pos[0] - swipe_start_pos[0]) / swipe_distance
                dy = (swipe_end_pos[1] - swipe_start_pos[1]) / swipe_distance
                if dx > 0.5:
                    swipe_direction = "right"
                elif dx < -0.5:
                    swipe_direction = "left"
                elif dy > 0.5:
                    swipe_direction = "down"
                elif dy < -0.5:
                    swipe_direction = "up"
                recorded_actions[-1] += f" {swipe_direction} {swipe_speed}"
            swipe_start_time = None
            swipe_start_pos = None
            swipe_direction = None
        while keyboard.is_pressed('2'):  # wait for key release
            pass
    elif keyboard.is_pressed('3'):
        if wait_start_time is None:
            wait_start_time = time.time()
            print("Recording wait")
        else:
            wait_duration = time.time() - wait_start_time
            recorded_actions.append(f"wait {wait_duration}")
            print(f"Recorded wait for {wait_duration} seconds")
            wait_start_time = None
        while keyboard.is_pressed('3'):  # wait for key release
            pass
    elif keyboard.is_pressed('4'):
        if len(recorded_actions)is not 0 and recorded_actions[-1].startswith('text'):
            recorded_actions[-1] += pyautogui.prompt("Enter text:")
            print(f"Recorded text: {recorded_actions[-1]}")
        else:
            text = pyautogui.prompt("Enter text:")
            recorded_actions.append(f"type {text}")
            print(f"Recorded text: {text}")
            while keyboard.is_pressed('4'): # wait for key release
                pass
    elif keyboard.is_pressed('5'):
        x, y = pyautogui.position()
        recorded_actions.append(f"double_click {x},{y}")
        print(f"Recorded double click at ({x},{y})")
        time.sleep(0.1) # wait for 100ms to avoid recording multiple clicks
        while keyboard.is_pressed('5'): # wait for key release
            pass
    elif keyboard.is_pressed('esc'):
        break

print("Recording finished.")
print("Recorded actions:")
for action in recorded_actions:
    print(action)






