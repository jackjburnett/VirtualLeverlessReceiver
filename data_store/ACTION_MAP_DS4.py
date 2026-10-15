## PS4 (DS4) Action Map Module
# Maps plain text commands to vgamepad controller commands, using lambda functions.
# For each of the following inputs, press and release are supported:
# - Buttons: CROSS, CIRCLE, TRIANGLE, SQUARE, L1, R1, SHARE, OPTIONS
# - D-Pad: DPAD_UP, DPAD_DOWN, DPAD_LEFT, DPAD_RIGHT
# - Triggers (Simplified to full/no hold): L2, R2
# - Joysticks (Simplified to full/no hold): LEFT_JOYSTICK, RIGHT_JOYSTICK
# - Special: PS_BUTTON, TOUCHPAD, L3, R3

# vgamepad (library for VigEmBus interfacing) import for gamepad object
import vgamepad as vg

# Dictionary mapping messages to gamepad lambda functions
ACTION_MAP = {
    # Face Buttons and Bumpers
    "CROSS_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS
    ),
    "CROSS_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS
    ),
    "CIRCLE_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE
    ),
    "CIRCLE_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE
    ),
    "TRIANGLE_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE
    ),
    "TRIANGLE_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE
    ),
    "SQUARE_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE
    ),
    "SQUARE_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE
    ),
    "L1_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT
    ),
    "L1_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT
    ),
    "R1_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT
    ),
    "R1_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT
    ),
    "SHARE_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_SHARE
    ),
    "SHARE_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_SHARE
    ),
    "OPTIONS_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS
    ),
    "OPTIONS_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS
    ),
    # D-Pad
    "DPAD_UP_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH
    ),
    "DPAD_UP_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH
    ),
    "DPAD_DOWN_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH
    ),
    "DPAD_DOWN_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH
    ),
    "DPAD_LEFT_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST
    ),
    "DPAD_LEFT_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST
    ),
    "DPAD_RIGHT_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST
    ),
    "DPAD_RIGHT_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST
    ),
    # Simplified Triggers
    "L2_PRESS": lambda gamepad: gamepad.left_trigger_float(
        value_float=1.0
    ),  # Full press
    "L2_RELEASE": lambda gamepad: gamepad.left_trigger_float(
        value_float=0.0
    ),  # Release
    "R2_PRESS": lambda gamepad: gamepad.right_trigger_float(
        value_float=1.0
    ),  # Full press
    "R2_RELEASE": lambda gamepad: gamepad.right_trigger_float(
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
    # PS4 Special Buttons
    "PS_BUTTON_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS
    ),
    "PS_BUTTON_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS
    ),
    "TOUCHPAD_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD
    ),
    "TOUCHPAD_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD
    ),
    # Thumbsticks
    "L3_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT
    ),
    "L3_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT
    ),
    "R3_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT
    ),
    "R3_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT
    ),
}
