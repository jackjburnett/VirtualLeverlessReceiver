"""
Gamepad Manager Module

This module provides functionality for managing virtual gamepad instances. It allows
creation, retrieval, and deletion of virtual Xbox 360 and PS4 (DS4) gamepads
that can be used to simulate gamepad input for gaming applications.

Dependencies:
    vgamepad: A Python library for creating virtual gamepads that simulate
              Xbox 360 and PS4 controller input on Windows systems.

Classes:
    VX360Gamepad: Virtual Xbox 360 gamepad controller
    VDS4Gamepad: Virtual PS4 (DS4) gamepad controller

Functions:
    get_or_create_gamepad(name, gamepad_type): Retrieve existing or create new gamepad
    create_gamepad(name, gamepad_type): Create a new virtual gamepad instance
    delete_gamepad(name): Safely remove and cleanup a gamepad instance

Constants:
    XBOX_GAMEPAD: Reference to Xbox 360 gamepad class
    DS4_GAMEPAD: Reference to PS4 (DS4) gamepad class
"""

import vgamepad as vg

# Dictionary to store gamepad objects for each value
gamepads = {}

# Gamepad types
XBOX_GAMEPAD = vg.VX360Gamepad
DS4_GAMEPAD = vg.VDS4Gamepad


def get_or_create_gamepad(name, gamepad_type="XBOX"):
    """
    Get or create a gamepad based on the given name (Client ID).

    Args:
        name (str): The name (Client ID) of the gamepad.
        gamepad_type (str): The type of gamepad [either Xbox or PS].

    Returns:
        vg.VX360Gamepad: The gamepad object.
    """

    if name in gamepads:
        return gamepads[name]
    else:
        return create_gamepad(name, gamepad_type)


def create_gamepad(name, gamepad_type="XBOX"):
    """
    Create a gamepad based on the given name (Client ID) and gamepad type.

    Args:
    name (str): The name (Client ID) of the gamepad.
    gamepad_type (str): The type of gamepad [either Xbox or PS].

    Returns:
        vg.VX360Gamepad: The gamepad object.
    """
    try:
        gamepad_type = gamepad_type.upper()
        if gamepad_type == "XBOX":
            gamepad = XBOX_GAMEPAD()
        elif gamepad_type == "PS":
            gamepad = DS4_GAMEPAD()
        else:
            print(f"Invalid gamepad_type provided")
            return None
        gamepads[name] = gamepad
        print(f"Created new {gamepad_type} gamepad for {name}")
        return gamepad
    except Exception as e:
        print(f"Error creating gamepad: {e}")
        return None


def delete_gamepad(name):
    """
    Safely delete a gamepad based on the given name (Client ID).

    Args:
        name (str): The name (Client ID) of the gamepad.
    """
    if name in gamepads:
        print(f"Deleting gamepad for {name}")
        gamepad = gamepads[name]
        gamepad.reset()
        gamepad.update()
        del gamepads[name]
    else:
        print(f"No gamepad found for {name}")


# Tests the script if executed standalone
if __name__ == "__main__":
    get_or_create_gamepad("Gamepad")
    print(gamepads)
    get_or_create_gamepad("Gamepad2", "PS")
    print(gamepads)
    delete_gamepad("Gamepad")
    print(gamepads)
    delete_gamepad("Gamepad")
    print(gamepads)
    delete_gamepad("Gamepad2")
    print(gamepads)
