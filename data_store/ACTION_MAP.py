import vgamepad as vg

# Dictionary mapping messages to lambda functions
ACTION_MAP = {
    # Buttons
    "A_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A
    ),
    "A_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A
    ),
    "B_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B
    ),
    "B_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B
    ),
    "X_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X
    ),
    "X_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X
    ),
    "Y_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
    ),
    "Y_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
    ),
    "LEFT_SHOULDER_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
    ),
    "LEFT_SHOULDER_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
    ),
    "RIGHT_SHOULDER_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
    ),
    "RIGHT_SHOULDER_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
    ),
    "BACK_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
    ),
    "BACK_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
    ),
    "START_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START
    ),
    "START_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START
    ),
    "LEFT_THUMB_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
    ),
    "LEFT_THUMB_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
    ),
    "RIGHT_THUMB_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
    ),
    "RIGHT_THUMB_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
    ),
    # D-Pad
    "DPAD_UP_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
    ),
    "DPAD_UP_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
    ),
    "DPAD_DOWN_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
    ),
    "DPAD_DOWN_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
    ),
    "DPAD_LEFT_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
    ),
    "DPAD_LEFT_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
    ),
    "DPAD_RIGHT_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
    ),
    "DPAD_RIGHT_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
    ),
    # Triggers
    "LEFT_TRIGGER_PRESS": lambda gamepad: gamepad.left_trigger(255),  # Full press
    "LEFT_TRIGGER_RELEASE": lambda gamepad: gamepad.left_trigger(0),  # Release
    "RIGHT_TRIGGER_PRESS": lambda gamepad: gamepad.right_trigger(255),  # Full press
    "RIGHT_TRIGGER_RELEASE": lambda gamepad: gamepad.right_trigger(0),  # Release
}
