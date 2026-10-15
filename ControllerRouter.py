"""Share controller ownership and the existing mapping modules across transports.

All methods run on the receiver's asyncio worker thread. No button mapping lives
here: GamepadParser and GamepadManager retain their original public interfaces.
"""

import logging

logger = logging.getLogger(__name__)


class ControllerRouter:
    def __init__(self, manager=None, parser=None, max_controllers=4):
        self.manager = manager
        self.parser = parser
        self.max_controllers = max_controllers
        self.clients = {}

    def initialize(self):
        if self.manager is None:
            import GamepadManager
            self.manager = GamepadManager
        if self.parser is None:
            import GamepadParser
            self.parser = GamepadParser

    def connect(self, client_id):
        if client_id in self.clients:
            return self.clients[client_id]
        if len(self.clients) >= self.max_controllers:
            raise RuntimeError(f"All {self.max_controllers} controller slots are in use")
        self.initialize()
        gamepad = self.manager.get_or_create_gamepad(client_id, "XBOX")
        if gamepad is None:
            raise RuntimeError("Unable to create virtual controller; check ViGEmBus")
        self.clients[client_id] = gamepad
        logger.info("Controller connected (%d/%d): %s",
                    len(self.clients), self.max_controllers, client_id)
        return gamepad

    @staticmethod
    def validate_message(message):
        message = message.strip()
        if not message:
            raise ValueError("Empty controller command")
        gamepad_type = None
        if message.startswith("Change gamepad type to:"):
            gamepad_type = message.removeprefix("Change gamepad type to:").strip().upper()
            if gamepad_type not in ("XBOX", "PS"):
                raise ValueError("Invalid gamepad type; use XBOX or PS")
        return message, gamepad_type

    def receive(self, client_id, message):
        message, gamepad_type = self.validate_message(message)
        gamepad = self.connect(client_id)
        if gamepad_type:
            # Drop our old reference as well as the manager's reference.
            self.clients.pop(client_id)
            gamepad = None
            self.manager.delete_gamepad(client_id)
            gamepad = self.manager.get_or_create_gamepad(client_id, gamepad_type)
            if gamepad is None:
                raise RuntimeError("Unable to create virtual controller; check ViGEmBus")
            self.clients[client_id] = gamepad
        else:
            self.parser.parse_gamepad(message, gamepad)

    def disconnect(self, client_id):
        if client_id in self.clients:
            self.clients.pop(client_id)
            self.manager.delete_gamepad(client_id)  # Existing reset/update cleanup.
            logger.info("Controller disconnected: %s", client_id)

    def close(self):
        for client_id in list(self.clients):
            try:
                self.disconnect(client_id)
            except Exception:
                logger.exception("Unable to release controller %s", client_id)
