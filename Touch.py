#!/usr/bin/env python3
import re
import sys
import time
import pyautogui

loops = {}

def substitute_variables(text):
    args = sys.argv
    print(args)
    print(text)
    for ar in args:
        if text in ar:
            text = ar[2:]
            print(text)
    return text



def execute_touch_script(lines, args):
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#'):
            i += 1
            continue

        tokens = line.split()

        if line.startswith('<loop'):
            if len(tokens) > 1:
                loop = tokens[1]
                loop_count = int(loop[:-1])
                loop_start = i
                loop_end = None

                # Find the end of the loop
                for j in range(i + 1, len(lines)):
                    inner_line = lines[j].strip()
                    if inner_line == '</loop>':
                        loop_end = j
                        break

                if loop_end is not None:
                    loop_lines = lines[loop_start + 1: loop_end]
                    for _ in range(loop_count):
                        execute_touch_script(loop_lines, args)  # Recursively execute loop_lines
                    i = loop_end + 1  # Skip to the line after </loop>
                else:
                    print("Error: Missing '</loop>' for '<loop>'")
                    break
            else:
                print("Error: Missing argument for '<loop>' command")
                break
        elif line == '</loop>':
            # Ignore '</loop>' here; it was handled when processing the corresponding '<loop>'
            pass
        else:
            try:
                if tokens[0] == 'wait':
                    if len(tokens) > 1:
                        seconds = float(tokens[1])
                        time.sleep(seconds)
                    else:
                        print("Error: Missing argument for 'wait' command")
                elif tokens[0] == 'hold':
                    if len(tokens) > 1:
                        duration = float(tokens[1])
                        time.sleep(duration)
                    else:
                        print("Error: Missing argument for 'hold' command")
                elif tokens[0] == 'click':
                    if len(tokens) > 1:
                        x, y = map(int, tokens[1].split(','))
                        pyautogui.click(x, y)
                        print(f"Clicked at ({x}, {y})")
                    else:
                        print("Error: Missing arguments for 'click' command")
                elif tokens[0] == 'doubleclick':
                    if len(tokens) > 1:
                        x, y = map(int, tokens[1].split(','))
                        pyautogui.doubleClick(x, y)
                        print(f"Double-clicked at ({x}, {y})")
                    else:
                        print("Error: Missing arguments for 'doubleclick' command")
                elif tokens[0] == 'rightclick':
                    if len(tokens) > 1:
                        x, y = map(int, tokens[1].split(','))
                        pyautogui.rightClick(x, y)
                        print(f"Right-clicked at ({x}, {y})")
                    else:
                        print("Error: Missing arguments for 'rightclick' command")
                elif tokens[0] == 'scroll':
                    if len(tokens) > 1:
                        units = int(tokens[1])
                        pyautogui.scroll(units)
                        print(f"Scrolled {units} units")
                    else:
                        print("Error: Missing argument for 'scroll' command")
                elif tokens[0] == 'type':
                        if len(tokens) > 1:
                            text = ' '.join(tokens[1:])

                            # Check for the format $"pos""var" and replace with "var"
                            if '$' in text:

                                text = substitute_variables(text)
                            pyautogui.typewrite(text)
                            print(f"Typed: {text}")
                        else:
                            print("Error: Missing argument for 'type' command")
                elif tokens[0] == 'hotkey':
                    if len(tokens) > 1:
                        hotkey = '+'.join(tokens[1:])
                        pyautogui.hotkey(hotkey)
                        print(f"Pressed hotkey: {hotkey}")
                    else:
                        print("Error: Missing argument for 'hotkey' command")
                elif tokens[0] == 'shiftclick':
                    if len(tokens) > 1:
                        x, y = map(int, tokens[1].split(','))
                        pyautogui.keyDown('shift')
                        pyautogui.click(x, y)
                        pyautogui.keyUp('shift')
                        print(f"Shift-clicked at ({x}, {y})")
                    else:
                        print("Error: Missing arguments for 'shiftclick' command")
                elif tokens[0] == 'swipe':
                    if len(tokens) > 4:
                        start_x, start_y = map(int, tokens[1].split(','))
                        end_x, end_y = map(int, tokens[2].split(','))
                        duration = float(tokens[3])
                        button = tokens[4]
                        pyautogui.moveTo(start_x, start_y)
                        pyautogui.dragTo(end_x, end_y, duration=duration, button=button)
                        print(f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})")
                    else:
                        print("Error: Missing arguments for 'swipe' command")
                else:
                    print(f"Unknown command: {tokens[0]}")
            except:
                print(f'line failed {i}')
        i += 1


def read_file_contents():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        args = sys.argv[2:]
        try:
            with open(file_path, 'r') as f:
                commands = f.readlines()
                execute_touch_script(commands, args)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            sys.exit()
    else:
        print("Usage: ./touch.py <file_path> <arguments>")
        sys.exit()


read_file_contents()
