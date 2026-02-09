def handle_trigger_action(message, gamepad):
    parts = message.split('_')
    
    # Check if it's a trigger action (LEFT/RIGHT_TRIGGER_x)
    if len(parts) >= 3 and parts[1] == "TRIGGER":
        try:
            trigger = parts[0]
            value = float(parts[2])
            
            if trigger == "LEFT":
                gamepad.left_trigger_float(value_float=value)
            elif trigger == "RIGHT":
                gamepad.right_trigger_float(value_float=value)
            return True
        except (ValueError, IndexError):
            pass
    return False
