import re


class DecisionEngine:

    def __init__(self, robot, navigator, sensors):
        self.robot = robot
        self.navigator = navigator
        self.sensors = sensors

        self.home_position = (0, 0)

    def process_command(self, command):

        command = command.strip().lower()

        if not command:
            return "Please enter a command."

        # Stop command
        if command in ["stop", "halt", "emergency stop"]:
            self.robot.stop()
            return "Robot stopped."

        # Current position
                
        position_commands = [
            "current position",
            "where are you",
            "where are u",
            "where am i",
            "your position",
            "position",
            "location"
        ]

        if any(phrase in command for phrase in position_commands):
            return f"Robot position: ({self.robot.x}, {self.robot.y})"

        # Scan surroundings
        
        scan_commands = [
            "scan surroundings",
            "scan surrondings",
            "scan environment",
            "scan area",
            "scan",
            "look around"
        ]

        if any(phrase in command for phrase in scan_commands):
            return self.sensors.scan_all(self.robot)
        # Return home
        if any(phrase in command for phrase in [
            "go home",
            "return home",
            "return to base"
        ]):
            x, y = self.home_position
            return self.navigator.navigate_to(x, y)

        # Navigate to coordinates
        match = re.search(
            r"(?:move|go|navigate|travel)\s+(?:to\s+)?"
            r"(-?\d+)\s*[, ]\s*(-?\d+)",
            command
        )

        if match:

            target_x = int(match.group(1))
            target_y = int(match.group(2))

            return self.navigator.navigate_to(target_x, target_y)

        return "Command not recognized."