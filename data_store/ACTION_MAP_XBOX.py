"""
Xbox 360 Action Map Module

This module defines the action mapping for Xbox 360 virtual gamepad controllers.
It maps string-based action commands to lambda functions that interact with the
virtual Xbox 360 gamepad using the vgamepad library.

Dependencies:
    vgamepad: A Python library for creating virtual gamepads that simulate
              Xbox 360 controller input on Windows systems

Constants:
    ACTION_MAP: Dictionary mapping action strings to lambda functions for Xbox inputs
               - Buttons: A, B, X, Y, LEFT_SHOULDER, RIGHT_SHOULDER, BACK, START
               - D-Pad: DPAD_UP, DPAD_DOWN, DPAD_LEFT, DPAD_RIGHT
               - Triggers: LEFT_TRIGGER, RIGHT_TRIGGER (float values 0.0-1.0)
               - Joysticks: LEFT_JOYSTICK, RIGHT_JOYSTICK (x,y coordinates -1.0 to 1.0)
               - Thumb sticks: LEFT_THUMB, RIGHT_THUMB

The action mapping supports both press and release events for buttons, and
simplified binary updates for triggers and joysticks. Each action string
corresponds to a specific gamepad input that can be executed via the lambda
functions stored in the ACTION_MAP dictionary.
"""

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
}
