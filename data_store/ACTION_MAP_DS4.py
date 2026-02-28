"""
PS4 (DS4) Action Map Module

This module defines the action mapping for PS4 DualShock 4 (DS4) virtual gamepad
controllers. It maps string-based action commands to lambda functions that
interact with the virtual DS4 gamepad using the vgamepad library.

Dependencies:
    vgamepad: A Python library for creating virtual gamepads that simulate
              PS4 (DS4) controller input on Windows systems

Constants:
    ACTION_MAP: Dictionary mapping action strings to lambda functions for DS4 inputs
               - Buttons: CROSS, CIRCLE, TRIANGLE, SQUARE, L1, R1, SHARE, OPTIONS
               - D-Pad: DPAD_UP, DPAD_DOWN, DPAD_LEFT, DPAD_RIGHT
               - Triggers: LEFT_TRIGGER, RIGHT_TRIGGER (float values 0.0-1.0)
               - Joysticks: LEFT_JOYSTICK, RIGHT_JOYSTICK (x,y coordinates -1.0 to 1.0)
               - Special: PS_BUTTON, TOUCHPAD, LEFT_THUMB, RIGHT_THUMB

The action mapping supports both press and release events for buttons, and
simplified binary updates for triggers and joysticks. Each action string
corresponds to a specific gamepad input that can be executed via the lambda
functions stored in the ACTION_MAP dictionary.
"""

import vgamepad as vg

# Dictionary mapping messages to lambda functions
ACTION_MAP = {
    # Buttons
    # Buttons
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
    "LEFT_THUMB_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT
    ),
    "LEFT_THUMB_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT
    ),
    "RIGHT_THUMB_PRESS": lambda gamepad: gamepad.press_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT
    ),
    "RIGHT_THUMB_RELEASE": lambda gamepad: gamepad.release_button(
        button=vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT
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
    "LEFT_TRIGGER_PRESS": lambda gamepad: gamepad.left_trigger_float(
        value_float=1.0
    ),  # Full press
    "LEFT_TRIGGER_RELEASE": lambda gamepad: gamepad.left_trigger_float(
        value_float=0.0
    ),  # Release
    "RIGHT_TRIGGER_PRESS": lambda gamepad: gamepad.right_trigger_float(
        value_float=1.0
    ),  # Full press
    "RIGHT_TRIGGER_RELEASE": lambda gamepad: gamepad.right_trigger_float(
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
}
