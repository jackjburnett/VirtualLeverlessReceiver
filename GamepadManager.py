import vgamepad as vg

# Dictionary to store gamepad objects for each value
gamepads = {}

# Gamepad types
XBOX_GAMEPAD = vg.VX360Gamepad
DS4_GAMEPAD = vg.VDS4Gamepad


def get_or_create_gamepad(name):
    """
    Get or create a gamepad based on the given name (IP Address).

    Args:
        name (str): The name (IP Address) of the gamepad.

    Returns:
        vg.VX360Gamepad: The gamepad object.
    """
    try:
        if name in gamepads:
            return gamepads[name]
        else:
            gamepad = XBOX_GAMEPAD()
            gamepads[name] = gamepad
            print(f"Created new gamepad for {name}")
            return gamepad
    except Exception as e:
        print(f"Error creating gamepad: {e}")
        return None


def delete_gamepad(name):
    """
    Safely delete a gamepad based on the given name (IP Address).

    Args:
        name (str): The name (IP Address) of the gamepad.
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
    TestGamepad = get_or_create_gamepad("Gamepad")
    print(gamepads)
    TestGamepad = get_or_create_gamepad("Gamepad2")
    print(gamepads)
    delete_gamepad("Gamepad")
    print(gamepads)
    delete_gamepad("Gamepad")
    print(gamepads)
