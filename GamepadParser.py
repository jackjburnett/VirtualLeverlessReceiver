"""
Gamepad Parser Module

This module handles parsing of gamepad input messages and updating virtual gamepad
instances accordingly. It maps string-based action commands to virtual gamepad
inputs using configurable action maps for different controller types.

Dependencies:
    time: Standard Python library for time-related functions (used in testing)
    vgamepad: A Python library for creating virtual gamepads that simulate
              Xbox 360 and PS4 controller input on Windows systems
    data_store.ACTION_MAP_DS4: Action mapping for PS4 (DS4) controller buttons
    data_store.ACTION_MAP_XBOX: Action mapping for Xbox 360 controller buttons  
    data_store.ACTION_MAP_JOYSTICK: Action mapping for joystick movements
    data_store.ACTION_MAP_TRIGGERS: Action mapping for trigger inputs

Functions:
    parse_gamepad(message, gamepad): Parse gamepad message and update virtual gamepad

The module supports both Xbox 360 and PS4 (DS4) virtual controllers with
comprehensive button, joystick, and trigger input handling.
"""

import time

import vgamepad as vg

import data_store.ACTION_MAP_DS4 as AMD
import data_store.ACTION_MAP_JOYSTICK as AMJ
import data_store.ACTION_MAP_TRIGGERS as AMT
import data_store.ACTION_MAP_XBOX as AMX


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
                # Try trigger actions if no joystick action found
                if not AMT.handle_trigger_action(message, gamepad):
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
        "PS_BUTTON_PRESS",
        "PS_BUTTON_RELEASE",
        "TOUCHPAD_PRESS",
        "TOUCHPAD_RELEASE",
    ]
    joystick_actions = [
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
        "LEFT_JOYSTICK_0.0_0.0",
        "RIGHT_JOYSTICK_-1.0_0.0",
        "RIGHT_JOYSTICK_1.0_0.0",
        "RIGHT_JOYSTICK_0.0_-1.0",
        "RIGHT_JOYSTICK_0.0_1.0",
        "RIGHT_JOYSTICK_0.0_0.0",
    ]
    trigger_actions = [
        # Test trigger continuous values
        "LEFT_TRIGGER_0.5",
        "LEFT_TRIGGER_1.0",
        "LEFT_TRIGGER_0.0",
        "RIGHT_TRIGGER_0.5",
        "RIGHT_TRIGGER_1.0",
        "RIGHT_TRIGGER_0.0",
    ]

    def test_gamepad(gamepad, actions):
        """Test a gamepad with a list of actions"""
        for act in actions:
            parse_gamepad(act, gamepad)
            time.sleep(1)

    # Test XBOX controller
    TestGamepad = vg.VX360Gamepad()
    test_gamepad(TestGamepad, x_actions)
    test_gamepad(TestGamepad, joystick_actions)
    test_gamepad(TestGamepad, trigger_actions)

    # Test DS4 controller
    TestGamepad = vg.VDS4Gamepad()
    test_gamepad(TestGamepad, d_actions)
    test_gamepad(TestGamepad, joystick_actions)
    test_gamepad(TestGamepad, trigger_actions)
