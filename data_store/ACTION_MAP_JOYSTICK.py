def handle_joystick_action(message, gamepad):
    parts = message.split('_')

    # Check if it's a joystick action (LEFT/RIGHT_JOYSTICK_x_y)
    if len(parts) >= 4 and parts[1] == "JOYSTICK":
        try:
            joystick = parts[0]
            x_val = float(parts[2])
            y_val = float(parts[3])

            if joystick == "LEFT":
                gamepad.left_joystick_float(x_val, y_val)
            elif joystick == "RIGHT":
                gamepad.right_joystick_float(x_val, y_val)
            return True
        except (ValueError, IndexError):
            pass
    return False