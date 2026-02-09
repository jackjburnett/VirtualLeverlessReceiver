"""
GamepadParser.py

This script handles gamepad input and updates a virtual gamepad accordingly.
It uses the vgamepad library to interact with the virtual gamepad.

Dependencies:
    - vgamepad
    - data_store.ACTION_MAP_DS4
"""

import time

import vgamepad as vg

import data_store.ACTION_MAP_DS4 as AMD
import data_store.ACTION_MAP_XBOX as AMX
import data_store.ACTION_MAP_JOYSTICK as AMJ


def parse_gamepad(message, gamepad):
    """
    Parse a gamepad message and update the virtual gamepad accordingly.

    Parameters:
        message (str): The gamepad message to parse.
        gamepad (vg.VX360Gamepad or vg.VDS4Gamepad): The virtual gamepad to update.
    """
    # Set the appropriate action map based on gamepad type
    if isinstance(gamepad, vg.VX360Gamepad):
        action_map = AMX.ACTION_MAP
    elif isinstance(gamepad, vg.VDS4Gamepad):
        action_map = AMD.ACTION_MAP
    else:
        print(f"Invalid gamepad type. Expected vg.VX360Gamepad or vg.VDS4Gamepad.")
        return
    
    try:
        # Retrieve the lambda function based on the message
        action = action_map.get(message)
        
        if action:
            # Execute the button action function
            action(gamepad)
        else:
            # Try joystick actions if no button action found
            if not AMJ.handle_joystick_action(message, gamepad):
                print(f"Unknown action: {message}")

        # Send the updates to the virtual gamepad
        gamepad.update()

    except Exception as e:
        # Handle any potential errors that occur during parsing or gamepad interaction
        print(f"Error parsing message: {e}")


# Tests the script if executed standalone
# For testing, go to https://hardwaretester.com/gamepad
if __name__ == "__main__":
    # Prepare all actions as a list
    x_actions = [
        "A_PRESS",
        "A_RELEASE",
        "B_PRESS",
        "B_RELEASE",
        "X_PRESS",
        "X_RELEASE",
        "Y_PRESS",
        "Y_RELEASE",
        "LEFT_SHOULDER_PRESS",
        "LEFT_SHOULDER_RELEASE",
        "RIGHT_SHOULDER_PRESS",
        "RIGHT_SHOULDER_RELEASE",
        "BACK_PRESS",
        "BACK_RELEASE",
        "START_PRESS",
        "START_RELEASE",
        "LEFT_THUMB_PRESS",
        "LEFT_THUMB_RELEASE",
        "RIGHT_THUMB_PRESS",
        "RIGHT_THUMB_RELEASE",
        "DPAD_UP_PRESS",
        "DPAD_UP_RELEASE",
        "DPAD_DOWN_PRESS",
        "DPAD_DOWN_RELEASE",
        "DPAD_LEFT_PRESS",
        "DPAD_LEFT_RELEASE",
        "DPAD_RIGHT_PRESS",
        "DPAD_RIGHT_RELEASE",
        "LEFT_TRIGGER_PRESS",
        "LEFT_TRIGGER_RELEASE",
        "RIGHT_TRIGGER_PRESS",
        "RIGHT_TRIGGER_RELEASE",
        "LEFT_JOYSTICK_LEFT",
        "LEFT_JOYSTICK_RIGHT",
        "LEFT_JOYSTICK_UP",
        "LEFT_JOYSTICK_DOWN",
        "LEFT_JOYSTICK_RESET",
        "RIGHT_JOYSTICK_LEFT",
        "RIGHT_JOYSTICK_RIGHT",
        "RIGHT_JOYSTICK_UP",
        "RIGHT_JOYSTICK_DOWN",
        "RIGHT_JOYSTICK_RESET",
        # Test joystick continuous values
        "LEFT_JOYSTICK_-1.0_0.0",
        "LEFT_JOYSTICK_1.0_0.0",
        "LEFT_JOYSTICK_0.0_-1.0",
        "LEFT_JOYSTICK_0.0_1.0",
        "RIGHT_JOYSTICK_-1.0_0.0",
        "RIGHT_JOYSTICK_1.0_0.0",
        "RIGHT_JOYSTICK_0.0_-1.0",
        "RIGHT_JOYSTICK_0.0_1.0",
    ]
    d_actions = [
        "CROSS_PRESS",
        "CROSS_RELEASE",
        "CIRCLE_PRESS",
        "CIRCLE_RELEASE",
        "TRIANGLE_PRESS",
        "TRIANGLE_RELEASE",
        "SQUARE_PRESS",
        "SQUARE_RELEASE",
        "L1_PRESS",
        "L1_RELEASE",
        "R1_PRESS",
        "R1_RELEASE",
        "SHARE_PRESS",
        "SHARE_RELEASE",
        "OPTIONS_PRESS",
        "OPTIONS_RELEASE",
        "DPAD_UP_PRESS",
        "DPAD_UP_RELEASE",
        "DPAD_DOWN_PRESS",
        "DPAD_DOWN_RELEASE",
        "DPAD_LEFT_PRESS",
        "DPAD_LEFT_RELEASE",
        "DPAD_RIGHT_PRESS",
        "DPAD_RIGHT_RELEASE",
        "LEFT_TRIGGER_PRESS",
        "LEFT_TRIGGER_RELEASE",
        "RIGHT_TRIGGER_PRESS",
        "RIGHT_TRIGGER_RELEASE",
        "LEFT_JOYSTICK_LEFT",
        "LEFT_JOYSTICK_RIGHT",
        "LEFT_JOYSTICK_UP",
        "LEFT_JOYSTICK_DOWN",
        "LEFT_JOYSTICK_RESET",
        "RIGHT_JOYSTICK_LEFT",
        "RIGHT_JOYSTICK_RIGHT",
        "RIGHT_JOYSTICK_UP",
        "RIGHT_JOYSTICK_DOWN",
        "RIGHT_JOYSTICK_RESET",
        # Test joystick continuous values
        "LEFT_JOYSTICK_-1.0_0.0",
        "LEFT_JOYSTICK_1.0_0.0",
        "LEFT_JOYSTICK_0.0_-1.0",
        "LEFT_JOYSTICK_0.0_1.0",
        "RIGHT_JOYSTICK_-1.0_0.0",
        "RIGHT_JOYSTICK_1.0_0.0",
        "RIGHT_JOYSTICK_0.0_-1.0",
        "RIGHT_JOYSTICK_0.0_1.0",
        "PS_BUTTON_PRESS",
        "PS_BUTTON_RELEASE",
        "TOUCHPAD_PRESS",
        "TOUCHPAD_RELEASE",
    ]
    TestGamepad = vg.VX360Gamepad()
    # Simulate pressing and releasing all buttons, triggers, and joysticks
    for act in x_actions:
        parse_gamepad(act, TestGamepad)
        time.sleep(1)
    TestGamepad = vg.VDS4Gamepad()
    # Simulate pressing and releasing all buttons, triggers, and joysticks
    for act in d_actions:
        parse_gamepad(act, TestGamepad)
        time.sleep(1)
