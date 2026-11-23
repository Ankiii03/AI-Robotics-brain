from simulation.pathfinder import PathFinder
from simulation.sensors import SimulatedSensors


class Navigator:

    def __init__(self, robot, world):
        self.robot = robot
        self.world = world
        self.pathfinder = PathFinder(world)
        self.sensors = SimulatedSensors(world)
        self.sensor_history = []

    def record_sensor_readings(self):
        readings = self.sensors.scan_all(self.robot)

        self.sensor_history.append({
            "position": (self.robot.x, self.robot.y),
            "readings": readings
        })

        return readings

    def navigate_to(self, target_x, target_y):

        start = (self.robot.x, self.robot.y)
        goal = (target_x, target_y)

        # Reset sensor history for this navigation
        self.sensor_history = []

        # Record initial environment scan
        self.record_sensor_readings()

        # Calculate route
        path = self.pathfinder.find_path(start, goal)

        if path is None:
            return {
                "success": False,
                "message": "No valid path found",
                "path": [],
                "sensor_history": self.sensor_history
            }

        # Remove starting position
        movement_path = path[1:]

        # Follow route
        for position in movement_path:

            x, y = position

            result = self.robot.move_step(x, y, self.world)

            if result != "Movement successful":
                return {
                    "success": False,
                    "message": result,
                    "path": path,
                    "sensor_history": self.sensor_history
                }

            # Scan environment after each movement
            self.record_sensor_readings()

        return {
            "success": True,
            "message": "Destination reached successfully",
            "path": path,
            "sensor_history": self.sensor_history
        }