class SafetyController:

    def __init__(self, world, minimum_battery=10):
        self.world = world
        self.minimum_battery = minimum_battery

    def evaluate_move(self, robot, target_x, target_y):

        # Battery check
        if robot.battery <= 0:
            return {
                "safe": False,
                "reason": "Battery depleted"
            }

        # Movement distance check
        distance = (
            abs(target_x - robot.x)
            + abs(target_y - robot.y)
        )

        if distance != 1:
            return {
                "safe": False,
                "reason": "Movement must be exactly one cell"
            }

        # Boundary check
        if not self.world.is_within_bounds(target_x, target_y):
            return {
                "safe": False,
                "reason": "Target outside world boundaries"
            }

        # Obstacle check
        if self.world.is_obstacle(target_x, target_y):
            return {
                "safe": False,
                "reason": "Obstacle detected"
            }

        # Battery reserve warning
        if robot.battery <= self.minimum_battery:
            return {
                "safe": True,
                "reason": "Move safe, but battery reserve is low"
            }

        return {
            "safe": True,
            "reason": "Movement approved"
        }