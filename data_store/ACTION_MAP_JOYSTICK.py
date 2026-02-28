"""
Joystick Action Handler Module

This module provides functionality for handling continuous joystick input actions
for virtual gamepad controllers. It parses joystick action messages and updates
the corresponding joystick positions with precise float values.

Dependencies:
    None (no external imports)

Functions:
    handle_joystick_action(message, gamepad): Parse joystick action messages and
                                              update virtual gamepad joystick positions

The module handles joystick actions in the format "LEFT_JOYSTICK_x_y" or 
"RIGHT_JOYSTICK_x_y" where x and y are float values between -1.0 and 1.0.
This allows for precise analog joystick control beyond simple directional inputs.

Supported joysticks:
    - LEFT_JOYSTICK: Updates left analog stick position
    - RIGHT_JOYSTICK: Updates right analog stick position

Coordinate system:
    - X-axis: -1.0 (left) to 1.0 (right)
    - Y-axis: -1.0 (down) to 1.0 (up)
"""


def handle_joystick_action(message, gamepad):
    parts = message.split("_")

    # Check if it's a joystick action (LEFT/RIGHT_JOYSTICK_x_y)
    if len(parts) >= 4 and parts[1] == "JOYSTICK":
        try:
            joystick = parts[0]
            x_val = float(parts[2])
            y_val = float(parts[3])

            if joystick == "LEFT":
                gamepad.left_joystick_float(x_val, y_val)
            elif joystick == "RIGHT":
                gamepad.right_joystick_float(x_val, y_val)
            return True
        except (ValueError, IndexError):
            print("Joystick Value Error")
    return False
