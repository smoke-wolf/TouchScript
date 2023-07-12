#!/usr/bin/env python3
import sys
import time
import pyautogui

loops = {}

def execute_touch_script(lines):
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#'):  # check if the line starts with a comment symbol
            i += 1
            continue  # skip the line if it's a comment
        tokens = line.split()
        if tokens[0] == 'wait':
            seconds = float(tokens[1])
            time.sleep(seconds)
        elif tokens[0] == 'hold':
            duration = float(tokens[1])
            time.sleep(duration)
        elif tokens[0] == 'click':
            x, y = map(int, tokens[1].split(','))
            pyautogui.click(x, y)
            print(f"Clicked at ({x}, {y})")
        elif tokens[0] == 'doubleclick':
            x, y = map(int, tokens[1].split(','))
            pyautogui.doubleClick(x, y)
            print(f"Double-clicked at ({x}, {y})")
        elif tokens[0] == 'rightclick':
            x, y = map(int, tokens[1].split(','))
            pyautogui.rightClick(x, y)
            print(f"Right-clicked at ({x}, {y})")
        elif tokens[0] == 'scroll':
            units = int(tokens[1])
            pyautogui.scroll(units)
            print(f"Scrolled {units} units")
        elif tokens[0] == 'type':
            text = ' '.join(tokens[1:])
            pyautogui.typewrite(text)
            print(f"Typed: {text}")
        elif tokens[0] == 'hotkey':
            hotkey = '+'.join(tokens[1:])
            pyautogui.hotkey(hotkey)
            print(f"Pressed hotkey: {hotkey}")
        elif tokens[0] == 'swipe':
            start_x, start_y = map(int, tokens[1].split(','))
            end_x, end_y = map(int, tokens[2].split(','))
            duration = float(tokens[3]) if len(tokens) > 3 else 0.5
            button = tokens[4] if len(tokens) > 4 else 'left'
            pyautogui.moveTo(start_x, start_y)
            pyautogui.dragTo(end_x, end_y, duration=duration, button=button)
            print(f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        elif tokens[0] == 'loop':
            loop_name = tokens[1]
            loop_block = []
            i += 1
            while i < len(lines) and lines[i].strip() != 'endloop':
                loop_block.append(lines[i].strip())
                i += 1
            loops[loop_name] = loop_block
        elif tokens[0] == 'call':
            loop_name = tokens[1]
            count = int(tokens[2])
            if loop_name in loops:
                block = loops[loop_name]
                for _ in range(count):
                    execute_touch_script(block)
            else:
                print(f"Unknown loop: {loop_name}")
        else:
            print(f"Unknown command: {tokens[0]}")

        i += 1


def read_file_contents():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                execute_touch_script(f.readlines())
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            sys.exit()
    else:
        print("Usage: ./touch.py <file_path>")
        sys.exit()


read_file_contents()
