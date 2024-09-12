import time

import vgamepad as vg

import data_store.ACTION_MAP as AM


# Function to parse the message and simulate the corresponding gamepad input
def parse_gamepad(message, gamepad):
    """
    Parses the incoming message and performs the appropriate action on the gamepad.

    Args:
    message (str): The incoming message indicating the action (e.g., 'A_PRESS', 'A_RELEASE').
    gamepad (vgamepad.VX360Gamepad): The virtual gamepad object to control.
    """
    try:
        # Retrieve the lambda function based on the message or use a default function
        action = AM.ACTION_MAP.get(
            message, lambda g: print(f"Unknown action: {message}")
        )

        # Execute the action function
        action(gamepad)

        # Send the updates to the virtual gamepad
        gamepad.update()

    except Exception as e:
        # Handle any potential errors that occur during parsing or gamepad interaction
        print(f"Error parsing message: {e}")


# Tests the script if executed standalone
if __name__ == "__main__":
    # Create a test instance of the VX360Gamepad
    TestGamepad = vg.VX360Gamepad()

    # Prepare all actions as a list
    actions = [
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

    # Simulate pressing and releasing all buttons and triggers
    for act in actions:
        parse_gamepad(act, TestGamepad)
        time.sleep(1)  # Wait for 1 second between actions
