import vgamepad as vg

# Dictionary to store gamepad objects for each value
gamepads = {}


# TODO: COMMENT
def get_or_create_gamepad(name):
    # If the gamepad already exists for this IP, return it
    if name in gamepads:
        return gamepads[name]
    else:
        # Otherwise, create a new gamepad and store it in the dictionary
        gamepad = vg.VX360Gamepad()
        gamepads[name] = gamepad
        print(f"Created new gamepad for {name}")
        return gamepad


# TODO: COMMENT
def delete_gamepad(name):
    # If the gamepad exists for the given IP, release all controls and remove it
    if name in gamepads:
        print(f"Deleting gamepad for {name}")
        gamepad = gamepads[name]

        # Optionally: Reset the gamepad (release buttons, reset sticks, etc.)
        gamepad.reset()
        gamepad.update()

        # Remove the gamepad from the dictionary
        del gamepads[name]
    else:
        print(f"No gamepad found for {name}")


# TODO: COMMENT
if __name__ == "__main__":
    TestGamepad = get_or_create_gamepad("Gamepad")
    print(gamepads)
    TestGamepad = get_or_create_gamepad("Gamepad2")
    print(gamepads)
    delete_gamepad("Gamepad")
    print(gamepads)
    delete_gamepad("Gamepad")
    print(gamepads)
