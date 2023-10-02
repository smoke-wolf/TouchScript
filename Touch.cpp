#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <thread>
#include <ApplicationServices/ApplicationServices.h>

void simulateMouseClick(int x, int y) {
    CGEventRef clickEvent = CGEventCreateMouseEvent(
        nullptr, kCGEventLeftMouseDown, CGPointMake(x, y), kCGEventLeftMouseDown);

    CGEventRef releaseEvent = CGEventCreateMouseEvent(
        nullptr, kCGEventLeftMouseUp, CGPointMake(x, y), kCGEventLeftMouseUp);

    CGEventPost(kCGHIDEventTap, clickEvent);
    CGEventPost(kCGHIDEventTap, releaseEvent);

    CFRelease(clickEvent);
    CFRelease(releaseEvent);
}

void execute_type(const std::vector<std::string>& tokens) {
    if (tokens.size() > 1) {
        std::string textToType;

        for (size_t i = 1; i < tokens.size(); ++i) {
            textToType += tokens[i];
            if (i < tokens.size() - 1) {
                textToType += ' ';
            }
        }

        for (size_t i = 0; i < textToType.length(); ++i) {
            char c = textToType[i];
            CGEventRef keyDownEvent = CGEventCreateKeyboardEvent(nullptr, 0, true);
            UniChar oneChar = c;
            CGEventKeyboardSetUnicodeString(keyDownEvent, 1, &oneChar);
            CGEventPost(kCGHIDEventTap, keyDownEvent);
            CFRelease(keyDownEvent);

            CGEventRef keyUpEvent = CGEventCreateKeyboardEvent(nullptr, 0, false);
            CGEventKeyboardSetUnicodeString(keyUpEvent, 1, &oneChar);
            CGEventPost(kCGHIDEventTap, keyUpEvent);
            CFRelease(keyUpEvent);

            std::this_thread::sleep_for(std::chrono::milliseconds(50));
        }
    } else {
        std::cerr << "Missing argument for the 'type' command" << std::endl;
    }
}

void execute_wait(const std::vector<std::string>& tokens) {
    if (tokens.size() > 1) {
        double seconds = std::stod(tokens[1]);
        std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(seconds * 1000)));
    } else {
        std::cerr << "Missing argument for the 'wait' command" << std::endl;
    }
}

void execute_hold(const std::vector<std::string>& tokens) {
    if (tokens.size() > 1) {
        double duration = std::stod(tokens[1]);
        std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(duration * 1000)));
    } else {
        std::cerr << "Missing argument for the 'hold' command" << std::endl;
    }
}

void execute_click(const std::vector<std::string>& tokens) {
    if (tokens.size() > 1) {
        size_t commaPos = tokens[1].find(',');
        if (commaPos != std::string::npos) {
            std::string xStr = tokens[1].substr(0, commaPos);
            std::string yStr = tokens[1].substr(commaPos + 1);

            int x = std::stoi(xStr);
            int y = std::stoi(yStr);

            simulateMouseClick(x, y);

        } else {
            std::cerr << "Invalid argument format for the 'click' command" << std::endl;
        }
    } else {
        std::cerr << "Missing argument for the 'click' command" << std::endl;
    }
}

void execute_command(const std::vector<std::string>& tokens) {
    if (tokens[0] == "click") {
        execute_click(tokens);
    } else if (tokens[0] == "wait") {
        execute_wait(tokens);
    } else if (tokens[0] == "hold") {
        execute_hold(tokens);
    } else if (tokens[0] == "type") {
        execute_type(tokens);
    } else {
        std::cerr << "Unknown command: " << tokens[0] << std::endl;
    }
}

void execute_touch_script(std::vector<std::string>& lines, std::vector<std::string>& args, int& i) {
    while (i < lines.size()) {
        std::string line = lines[i];

        if (line[0] == '#') {
            i++;
            continue;
        }

        std::vector<std::string> tokens;
        size_t pos = 0;
        std::string delimiter = " ";
        while ((pos = line.find(delimiter)) != std::string::npos) {
            std::string token = line.substr(0, pos);
            tokens.push_back(token);
            line.erase(0, pos + delimiter.length());
        }
        tokens.push_back(line);

        if (tokens[0] == "<loop") {
            if (tokens.size() > 1) {
                int loop_count = std::stoi(tokens[1]);
                int loop_start = i;
                int loop_end = -1;

                for (int j = i + 1; j < lines.size(); j++) {
                    if (lines[j] == "</loop>") {
                        loop_end = j;
                        break;
                    }
                }

                if (loop_end != -1) {
                    for (int k = 0; k < loop_count; k++) {
                        execute_touch_script(lines, args, i);
                    }
                    i = loop_end + 1;
                } else {
                    std::cerr << "Missing '</loop>' for the current '<loop>'" << std::endl;
                }
            } else {
                std::cerr << "Missing argument for the '<loop>' command" << std::endl;
            }
        } else if (line == "</loop>") {
            i++;
        } else {
            execute_command(tokens);
            i++;
        }
    }
}

int main(int argc, char* argv[]) {
    std::vector<std::string> args;
    for (int i = 1; i < argc; ++i) {
        args.push_back(argv[i]);
    }

    if (args.size() == 0) {
        std::cout << "Please enter the path to the script file: ";
        std::string file_path;
        std::cin >> file_path;
        args.push_back(file_path);
    }

    std::string file_path = args[0];
    args.erase(args.begin());
    std::ifstream input_file(file_path);

    if (!input_file.is_open()) {
        std::cerr << "File not found" << std::endl;
        return 1;
    }

    std::vector<std::string> commands;
    std::string line;
    while (std::getline(input_file, line)) {
        commands.push_back(line);
    }

    int i = 0;
    execute_touch_script(commands, args, i);

    return 0;
}
