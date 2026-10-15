## Joystick Action Map Module
# Breaks a message down to attempt parsing it as a joystick command (LEFT/RIGHT_JOYSTICK_X_Y)

# Updates the relevant gamepad joystick or raises an exception

# Function call for handling joysticks, takes message and gamepad object
def handle_joystick_action(message, gamepad):
    # Split message by underscores
    parts = message.split("_")

    # Check if it's a joystick action (LEFT/RIGHT_JOYSTICK_x_y)
    if len(parts) == 4 and parts[1] == "JOYSTICK":
        try:
            # Allocates split into variables
            joystick = parts[0]
            x_val = float(parts[2])
            y_val = float(parts[3])

            # Updates the relevant joystick
            if joystick == "LEFT":
                gamepad.left_joystick_float(fix_joystick_range(x_val), fix_joystick_range(y_val))
                return True
            elif joystick == "RIGHT":
                gamepad.right_joystick_float(fix_joystick_range(x_val), fix_joystick_range(y_val))
                return True
        # Any gamepad issues raise a joystick value error
        except (ValueError, IndexError):
            print("Joystick Value Error")
    return False

# Clamps X and Y values between 1.0 to -1.0 rather than raising an exception
def fix_joystick_range(value):
    if value < -1.0:
        return -1.0
    elif value > 1.0:
        return 1.0
    else:
        return value
