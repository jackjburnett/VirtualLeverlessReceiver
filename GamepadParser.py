import time

import vgamepad as vg


# Function to parse the message and simulate the corresponding gamepad input
def parse_gamepad(message, gamepad):
    """
    Parses the incoming message and performs the appropriate action on the gamepad.

    Args:
    message (str): The incoming message indicating the action (e.g., 'A_PRESS', 'A_RELEASE').
    gamepad (vgamepad.VX360Gamepad): The virtual gamepad object to control.
    """
    try:
        # Parse the message and perform the corresponding gamepad action
        if message == "A_PRESS":
            # Press the A button on the virtual gamepad
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        elif message == "A_RELEASE":
            # Release the A button
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        elif message == "LEFT_JOYSTICK_50_50":
            # Move the left joystick to (50%, 50%)
            gamepad.left_joystick_float(x_value_float=0.5, y_value_float=0.5)
        # Add more cases for other buttons, triggers, or joystick movements as needed

        # Send the updates to the virtual gamepad
        gamepad.update()

    except Exception as e:
        # Handle any potential errors that occur during parsing or gamepad interaction
        print(f"Error parsing message: {e}")


if __name__ == "__main__":
    # Create a test instance of the VX360Gamepad
    TestGamepad = vg.VX360Gamepad()

    # Simulate pressing the A button
    parse_gamepad("A_PRESS", TestGamepad)
    time.sleep(1)  # Wait for 1 second

    # Simulate releasing the A button
    parse_gamepad("A_RELEASE", TestGamepad)
