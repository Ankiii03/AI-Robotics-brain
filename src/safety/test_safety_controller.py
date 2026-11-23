import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulation.robot import Robot
from simulation.world import SimulationWorld
from safety.safety_controller import SafetyController


world = SimulationWorld()
robot = Robot("R001", "Explorer")
safety = SafetyController(world)

print("Test 1: Safe movement")
print(safety.evaluate_move(robot, 0, 1))

print("\nTest 2: Obstacle")
robot.x = 2
robot.y = 3
print(safety.evaluate_move(robot, 3, 3))

print("\nTest 3: Outside boundaries")
robot.x = 0
robot.y = 0
print(safety.evaluate_move(robot, -1, 0))

print("\nTest 4: Invalid multi-cell movement")
print(safety.evaluate_move(robot, 2, 2))

print("\nTest 5: Low battery")
robot.battery = 5
print(safety.evaluate_move(robot, 0, 1))

print("\nTest 6: Battery depleted")
robot.battery = 0
print(safety.evaluate_move(robot, 0, 1))