import keyboard
import time
import pyautogui

recorded_actions = []
start_time = time.time()
wait_start_time = None
swipe_start_time = None
swipe_start_pos = None
swipe_direction = None

def execute_recorded_actions(actions):
    for action in actions:
        tokens = action.split()
        if tokens[0] == 'click':
            x, y = map(int, tokens[1].split(','))
            pyautogui.click(x, y)
            time.sleep(0.1)
        elif tokens[0] == 'swipe':
            coordinates = [int(coord) for coord in tokens[1].split(',')]
            if len(coordinates) == 2:
                x1, y1 = coordinates
                pyautogui.moveTo(x1, y1)
                time.sleep(0.1)
            elif len(coordinates) == 4:
                x1, y1, x2, y2 = coordinates
                pyautogui.dragTo(x2, y2, duration=0.5)
            elif len(coordinates) == 5:
                x1, y1, x2, y2, direction = coordinates
                speed = float(tokens[5])
                if direction == 'up':
                    pyautogui.scroll(-speed)
                elif direction == 'down':
                    pyautogui.scroll(speed)
            time.sleep(0.1)
        elif tokens[0] == 'wait':
            time.sleep(float(tokens[1]))
        elif tokens[0] == 'type':
            text = ' '.join(tokens[1:])
            pyautogui.typewrite(text)
            time.sleep(0.1)
        elif tokens[0] == 'double_click':
            x, y = map(int, tokens[1].split(','))
            pyautogui.doubleClick(x, y)
            time.sleep(0.1)

print("Press 1 key to record clicks, 2 key to record swipes, 3 key to record waits, 4 key to record text, 5 key to record double clicks")

while time.time() - start_time < 30:  # maximum recording time of 30 seconds
    if keyboard.is_pressed('1'):
        x, y = pyautogui.position()
        recorded_actions.append(f"click {x},{y}")
        print(f"Recorded click at ({x},{y})")
        time.sleep(0.1)
    elif keyboard.is_pressed('2'):
        if not swipe_start_time:
            x1, y1 = pyautogui.position()
            recorded_actions.append(f"swipe {x1},{y1}")
            print(f"Recorded swipe start position at ({x1},{y1})")
            time.sleep(0.1)
            swipe_start_pos = (x1, y1)
            swipe_start_time = time.time()
            swipe_direction = None
        else:
            x2, y2 = pyautogui.position()
            recorded_actions[-1] += f" {x2},{y2}"
            print(f"Recorded swipe end position at ({x2},{y2})")
            time.sleep(0.1)
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
    elif keyboard.is_pressed('3'):
        if not wait_start_time:
            wait_start_time = time.time()
            print("Recording wait")
        else:
            wait_duration = time.time() - wait_start_time
            recorded_actions.append(f"wait {wait_duration}")
            print(f"Recorded wait for {wait_duration} seconds")
            wait_start_time = None
    elif keyboard.is_pressed('4'):
        if len(recorded_actions) > 0 and recorded_actions[-1].startswith('type'):
            recorded_actions[-1] += pyautogui.prompt("Enter text:")
            print(f"Recorded text: {recorded_actions[-1]}")
        else:
            text = pyautogui.prompt("Enter text:")
            recorded_actions.append(f"type {text}")
            print(f"Recorded text: {text}")
    elif keyboard.is_pressed('5'):
        x, y = pyautogui.position()
        recorded_actions.append(f"double_click {x},{y}")
        print(f"Recorded double click at ({x},{y})")
        time.sleep(0.1)
    elif keyboard.is_pressed('esc'):

        break

print("Recording finished.")
print("Recorded actions:")
for action in recorded_actions:
    print(action)

# Execute the recorded actions
execute_recorded_actions(recorded_actions)
