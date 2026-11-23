class SimulatedSensors:

    def __init__(self, world, max_range=3):
        self.world = world
        self.max_range = max_range

    def scan_direction(self, robot, direction):

        directions = {
            "north": (0, 1),
            "south": (0, -1),
            "east": (1, 0),
            "west": (-1, 0)
        }

        if direction not in directions:
            return {"error": "Invalid direction"}

        dx, dy = directions[direction]

        detected_distance = None
        detected_type = "clear"
        free_cells = 0

        for distance in range(1, self.max_range + 1):

            x = robot.x + dx * distance
            y = robot.y + dy * distance

            # Detect world boundary
            if not self.world.is_within_bounds(x, y):
                detected_distance = distance
                detected_type = "boundary"
                break

            # Detect obstacle
            if self.world.is_obstacle(x, y):
                detected_distance = distance
                detected_type = "obstacle"
                break

            free_cells += 1

        return {
            "direction": direction,
            "detected_type": detected_type,
            "distance": detected_distance,
            "free_cells": free_cells
        }

    def scan_all(self, robot):

        directions = ["north", "south", "east", "west"]

        readings = {}

        for direction in directions:
            readings[direction] = self.scan_direction(
                robot, direction
            )

        return readings