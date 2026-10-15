## Trigger Action Map Module
# Breaks a message down to attempt parsing it as a trigger command (LEFT/RIGHT_JOYSTICK_X_Y)
# Checks if an alias was used and resolves this (LT/RT/L2/R2)
# Updates the relevant gamepad trigger or raises an exception

def handle_trigger_action(message, gamepad):
    # Split the message on the last underscore
    parts = message.rsplit("_", 1)

    # Set the aliases and the trigger they represent
    aliases = {
        "LT": "LEFT",
        "L2": "LEFT",
        "LEFT_TRIGGER": "LEFT",
        "RT": "RIGHT",
        "R2": "RIGHT",
        "RIGHT_TRIGGER": "RIGHT",
    }

    # Check if the message has two parts
    if len(parts) == 2:
        try:
            # Set the trigger to the relevant alias and get the trigger value
            trigger = aliases.get(parts[0])
            value = fix_trigger_range(float(parts[1]))

            # Updates the relevant trigger
            if trigger == "LEFT":
                gamepad.left_trigger_float(value_float=value)
                return True
            elif trigger == "RIGHT":
                gamepad.right_trigger_float(value_float=value)
                return True
        # Any gamepad issues raise a trigger value error
        except (ValueError, IndexError):
            print("Trigger Value Error")
    return False

# Clamps X and Y values between 1.0 to -1.0 rather than raising an exception
def fix_trigger_range(value):
    if value < 0.0:
        return 0.0
    elif value > 1.0:
        return 1.0
    else:
        return value
