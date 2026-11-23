class SimulationWorld:

    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height

        # Fixed obstacles in the simulated environment
        self.obstacles = {
            (3, 3),
            (3, 4),
            (3, 5),
            (6, 6),
            (7, 6)
        }

    # Check if coordinates are inside the world
    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    # Check if a position contains an obstacle
    def is_obstacle(self, x, y):
        return (x, y) in self.obstacles

    # Check whether a position is safe to occupy
    def is_valid_position(self, x, y):
        return (
            self.is_within_bounds(x, y)
            and not self.is_obstacle(x, y)
        )

    # Display the world grid
    def display(self, robot=None):

        for y in range(self.height - 1, -1, -1):

            row = ""

            for x in range(self.width):

                if robot and (robot.x, robot.y) == (x, y):
                    row += " R "

                elif (x, y) in self.obstacles:
                    row += " # "

                else:
                    row += " . "

            print(row)

        print()