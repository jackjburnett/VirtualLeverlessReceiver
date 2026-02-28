"""
Trigger Action Handler Module

This module provides functionality for handling continuous trigger input actions
for virtual gamepad controllers. It parses trigger action messages and updates
the corresponding trigger positions with precise float values.

Dependencies:
    None (no external imports)

Functions:
    handle_trigger_action(message, gamepad): Parse trigger action messages and
                                             update virtual gamepad trigger positions

The module handles trigger actions in the format "LEFT_TRIGGER_x" or 
"RIGHT_TRIGGER_x" where x is a float value between 0.0 and 1.0.
This allows for precise analog trigger control beyond simple press/release inputs.

Supported triggers:
    - LEFT_TRIGGER: Updates left trigger position
    - RIGHT_TRIGGER: Updates right trigger position

Value range:
    - 0.0: Fully released
    - 1.0: Fully pressed
    - Values between 0.0 and 1.0: Partial trigger depression
"""


def handle_trigger_action(message, gamepad):
    parts = message.split("_")

    # Check if it's a trigger action (LEFT/RIGHT_TRIGGER_x)
    if len(parts) >= 3 and parts[1] == "TRIGGER":
        try:
            trigger = parts[0]
            value = float(parts[2])

            if trigger == "LEFT":
                gamepad.left_trigger_float(value_float=value)
            elif trigger == "RIGHT":
                gamepad.right_trigger_float(value_float=value)
            return True
        except (ValueError, IndexError):
            print("Trigger Value Error")
    return False
