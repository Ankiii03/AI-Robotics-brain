class Robot:

    def __init__(self, robot_id, name, x=0, y=0):
        self.robot_id = robot_id
        self.name = name

        # Robot position
        self.x = x
        self.y = y

        # Robot state
        self.status = "idle"
        self.mode = "manual"
        self.battery = 100

    def get_status(self):
        return {
            "robot_id": self.robot_id,
            "name": self.name,
            "position": {
                "x": self.x,
                "y": self.y
            },
            "status": self.status,
            "mode": self.mode,
            "battery": self.battery
        }

    def set_mode(self, mode):
        if mode not in ["manual", "autonomous"]:
            raise ValueError("Invalid robot mode")

        self.mode = mode

    # Move robot one cell at a time
    def move_step(self, x, y, world):

        # Check battery
        if self.battery <= 0:
            self.status = "idle"
            return "Movement rejected: Battery depleted"

        # Movement must be exactly one cell in one direction
        distance = abs(x - self.x) + abs(y - self.y)

        if distance != 1:
            return "Movement rejected: Move only one cell at a time"

        # Check world boundaries
        if not world.is_within_bounds(x, y):
            return "Movement rejected: Outside world boundaries"

        # Check obstacles
        if world.is_obstacle(x, y):
            return "Movement rejected: Obstacle detected"

        # Execute safe movement
        self.status = "moving"
        self.x = x
        self.y = y

        # Consume battery for movement
        self.battery -= 1

        self.status = "idle"

        return "Movement successful"

    def stop(self):
        self.status = "idle"
        return "Robot stopped"