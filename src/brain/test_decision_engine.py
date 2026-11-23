import sys
sys.path.insert(0, "src")

from simulation.robot import Robot
from simulation.world import SimulationWorld
from simulation.navigator import Navigator
from simulation.sensors import SimulatedSensors
from brain.decision_engine import DecisionEngine


robot = Robot("R001", "Explorer")
world = SimulationWorld()

sensors = SimulatedSensors(world)
navigator = Navigator(robot, world)

engine = DecisionEngine(robot, navigator, sensors)


print(engine.process_command("where are you"))

print(engine.process_command("scan surroundings"))

print(engine.process_command("move to 5,5"))

print(engine.process_command("where are you"))

world.display(robot)