## Xbox 360 Action Map Module
# Maps plain text commands to vgamepad controller commands, using lambda functions.
# For each of the following inputs, press and release are supported:
# - Buttons: A, B, X, Y, LEFT_BUMBER/LB, RIGHT_BUMPER/RB, BACK, START
# - D-Pad: DPAD_UP, DPAD_DOWN, DPAD_LEFT, DPAD_RIGHT
# - Triggers (Simplified to full/no hold): LEFT_TRIGGER/LT, RIGHT_TRIGGER/RT
# - Joysticks (Simplified to full/no hold): LEFT_JOYSTICK, RIGHT_JOYSTICK
# - Special: HOME/GUIDE/XBOX_BUTTON, LEFT_THUMB/LS, RIGHT_THUMB/RS

# vgamepad (library for VigEmBus interfacing) import for gamepad object
import vgamepad as vg

# Dictionary mapping messages to gamepad lambda functions
ACTION_MAP = {
    # Face Buttons and Bumpers
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
    "LEFT_BUMPER_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
    ),
    "LEFT_BUMPER_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
    ),
    "LB_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
    ),
    "LB_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
    ),
    "RIGHT_BUMPER_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
    ),
    "RIGHT_BUMPER_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
    ),
    "RB_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
    ),
    "RB_RELEASE": lambda gamepad: gamepad.release_button(
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
    # Simplified Triggers
    "LEFT_TRIGGER_PRESS": lambda gamepad: gamepad.left_trigger_float(
        value_float=1.0
    ),  # Full press
    "LEFT_TRIGGER_RELEASE": lambda gamepad: gamepad.left_trigger_float(
        value_float=0.0
    ),  # Release
    "LT_PRESS": lambda gamepad: gamepad.left_trigger_float(
        value_float=1.0
    ),  # Full press
    "LT_RELEASE": lambda gamepad: gamepad.left_trigger_float(
        value_float=0.0
    ),  # Release
    "RIGHT_TRIGGER_PRESS": lambda gamepad: gamepad.right_trigger_float(
        value_float=1.0
    ),  # Full press
    "RIGHT_TRIGGER_RELEASE": lambda gamepad: gamepad.right_trigger_float(
        value_float=0.0
    ),  # Release
    "RT_PRESS": lambda gamepad: gamepad.right_trigger_float(
        value_float=1.0
    ),  # Full press
    "RT_RELEASE": lambda gamepad: gamepad.right_trigger_float(
        value_float=0.0
    ),  # Release
    # Simplified Joysticks
    "LEFT_JOYSTICK_LEFT": lambda gamepad: gamepad.left_joystick_float(
        x_value_float=-1.0, y_value_float=0.0
    ),
    "LEFT_JOYSTICK_RIGHT": lambda gamepad: gamepad.left_joystick_float(
        x_value_float=1.0, y_value_float=0.0
    ),
    "LEFT_JOYSTICK_UP": lambda gamepad: gamepad.left_joystick_float(
        x_value_float=0.0, y_value_float=1.0
    ),
    "LEFT_JOYSTICK_DOWN": lambda gamepad: gamepad.left_joystick_float(
        x_value_float=0.0, y_value_float=-1.0
    ),
    "LEFT_JOYSTICK_RESET": lambda gamepad: gamepad.left_joystick_float(
        x_value_float=0.0, y_value_float=0.0
    ),
    "RIGHT_JOYSTICK_LEFT": lambda gamepad: gamepad.right_joystick_float(
        x_value_float=-1.0, y_value_float=0.0
    ),
    "RIGHT_JOYSTICK_RIGHT": lambda gamepad: gamepad.right_joystick_float(
        x_value_float=1.0, y_value_float=0.0
    ),
    "RIGHT_JOYSTICK_UP": lambda gamepad: gamepad.right_joystick_float(
        x_value_float=0.0, y_value_float=1.0
    ),
    "RIGHT_JOYSTICK_DOWN": lambda gamepad: gamepad.right_joystick_float(
        x_value_float=0.0, y_value_float=-1.0
    ),
    "RIGHT_JOYSTICK_RESET": lambda gamepad: gamepad.right_joystick_float(
        x_value_float=0.0, y_value_float=0.0
    ),
    # Xbox Special Button
    "HOME_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE
    ),
    "HOME_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE
    ),
    "GUIDE_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE
    ),
    "GUIDE_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE
    ),
    "XBOX_BUTTON_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE
    ),
    "XBOX_BUTTON_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE
    ),
    # Thumbsticks
    "LEFT_THUMB_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
    ),
    "LEFT_THUMB_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
    ),
    "LS_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
    ),
    "LS_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
    ),
    "RIGHT_THUMB_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
    ),
    "RIGHT_THUMB_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
    ),
    "RS_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
    ),
    "RS_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
    ),
    # Reset
    "RESET": lambda gamepad: gamepad.reset(),
}
