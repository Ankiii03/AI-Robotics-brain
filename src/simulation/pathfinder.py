import heapq


class PathFinder:

    def __init__(self, world):
        self.world = world

    # Estimate distance between two points
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Find a route from start to goal
    def find_path(self, start, goal):

        # Validate starting and ending positions
        if not self.world.is_valid_position(*start):
            return None

        if not self.world.is_valid_position(*goal):
            return None

        open_list = []
        heapq.heappush(open_list, (0, start))

        came_from = {}
        g_score = {start: 0}

        while open_list:

            _, current = heapq.heappop(open_list)

            # Destination reached
            if current == goal:
                return self.reconstruct_path(came_from, current)

            x, y = current

            # Possible movements
            neighbors = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1)
            ]

            for neighbor in neighbors:

                nx, ny = neighbor

                # Reject invalid cells
                if not self.world.is_valid_position(nx, ny):
                    continue

                tentative_g = g_score[current] + 1

                if tentative_g < g_score.get(neighbor, float("inf")):

                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g

                    f_score = tentative_g + self.heuristic(neighbor, goal)

                    heapq.heappush(open_list, (f_score, neighbor))

        return None

    # Reconstruct the route
    def reconstruct_path(self, came_from, current):

        path = [current]

        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()

        return path
    