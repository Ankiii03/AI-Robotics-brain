import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulation.robot import Robot
from simulation.world import SimulationWorld


world = SimulationWorld()
robot = Robot("R001", "Explorer")

# Test 1: Valid movement
print("Test 1: Safe movement")
print(robot.move_step(0, 1, world))
print("Position:", robot.x, robot.y)

# Test 2: Attempt to enter obstacle
print("\nTest 2: Obstacle rejection")
robot.x = 2
robot.y = 3
result = robot.move_step(3, 3, world)
print(result)
print("Position:", robot.x, robot.y)

# Test 3: Boundary violation
print("\nTest 3: Boundary rejection")
robot.x = 0
robot.y = 0
result = robot.move_step(-1, 0, world)
print(result)
print("Position:", robot.x, robot.y)

# Test 4: Depleted battery
print("\nTest 4: Battery rejection")
robot.battery = 0
result = robot.move_step(0, 1, world)
print(result)
print("Position:", robot.x, robot.y)