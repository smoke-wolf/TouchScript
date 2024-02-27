# TouchScript
.touch is a lightweight and user-friendly scripting language designed to automate common tasks on your computer.


> [!TIP]
> Compile the .cpp file using `g++ -o touch touch.cpp -framework CoreFoundation -framework CoreGraphics` for macOS only

📦 Three Scripts: Qrec, TouchEditor, Touch

📝 Description:
Qrec: Records touch inputs and generates .touch code.
TouchEditor: Edits .touch language scripts, with syntax highlighting.
Touch: Executes .touch scripts.

🚀 Features:
Qrec:
- Records touch inputs and generates .touch code.
- Can record a all touch capabilities.
- Generates code with comments and wait times for easy editing.

TouchEditor:
- Syntax highlighting for .touch code.
- Auto-completion for commands and parameters.
- Line numbering for easy reference.
- Export edited scripts as .touch files.

Touch:
- g++ -o  touch Touch.cpp  -framework ApplicationServices
- Executes .touch scripts.
- Supports wait times, taps, double taps, long presses, swipes, scrolling, typing, hotkeys, and more.
- Outputs feedback on executed commands.

💻 Syntax and Formatting:
- Commands are written one per line.
- Parameters are separated by spaces.
- Comments start with the '#' symbol.
- Indentation is not necessary but helps with readability.
- See documentation for command-specific parameters.

| Script Name  | Functionality                       |
| ------------ | ----------------------------------- |
| Qrec         | Records touch inputs                 |
| TouchEditor  | Edits .touch language scripts        |
| Touch        | Executes .touch scripts              |

| Command     | Syntax                                             | Description                                                                                              |
|-------------|----------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| wait        | wait <seconds>                                     | Wait for specified number of seconds                                                                     |
| hold        | hold <duration>                                    | Hold for specified duration                                                                              |
| click       | click <x>,<y>                                      | Click at the specified coordinates                                                                       |
| doubleclick | doubleclick <x>,<y>                                | Double-click at the specified coordinates                                                               |
| rightclick  | rightclick <x>,<y>                                 | Right-click at the specified coordinates                                                                |
| scroll      | scroll <units>                                     | Scroll the mouse wheel by the specified number of units                                                |
| type        | type <text>                                        | Type the specified text                                                                                  |
| hotkey      | hotkey <key1>+<key2>+...                           | Press the specified hotkey                                                                               |
| swipe       | swipe <start_x>,<start_y> <end_x>,<end_y> [duration] [button] | Swipe from the start coordinates to the end coordinates with the specified duration and button (default is left) |
 
 ## Usage

Qrec
Run `sudo python3 qrec.py` to start recording your touch interactions.
Press Esc to stop recording and save the output as a .touch file.

TouchEditor
Run `python3 toucheditor.py <file_path>` to open the TouchEditor and load a .touch file.

Touch
Run `python3 touch.py <file_path>` to execute a .touch file.


