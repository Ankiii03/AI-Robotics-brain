import sys
from pathlib import Path

# Make src available for imports
sys.path.insert(0, str(Path(__file__).parent))

from simulation.robot import Robot
from simulation.world import SimulationWorld
from simulation.sensors import SimulatedSensors
from simulation.navigator import Navigator
from brain.decision_engine import DecisionEngine


def main():

    world = SimulationWorld()
    robot = Robot("R001", "Explorer")
    sensors = SimulatedSensors(world)
    navigator = Navigator(robot, world)

    engine = DecisionEngine(robot, navigator, sensors)

    print("=" * 40)
    print(" AI ROBOTICS BRAIN")
    print("=" * 40)
    print("Robot initialized successfully.")
    print("Type 'help' to see available commands.")
    print("Type 'exit' to shut down.\n")

    world.display(robot)

    while True:

        command = input("Robot> ").strip()

        if command.lower() in ["exit", "quit"]:
            print("Robot system shutting down.")
            break

        if command.lower() == "help":
            print("""
Available commands:

1. move to X,Y
2. go X,Y
3. navigate to X,Y
4. where are you
5. scan surroundings
6. go home
7. stop
8. exit
""")
            continue

        response = engine.process_command(command)

        print("\nRobot Response:")

        if isinstance(response, dict):

            if "success" in response:
                print("Success:", response["success"])
                print("Message:", response["message"])
                print("Path:", response.get("path", []))
            else:
                print(response)

        else:
            print(response)

        print("\nCurrent Robot Position:")
        print(f"X: {robot.x} | Y: {robot.y}")

        world.display(robot)


if __name__ == "__main__":
    main()
    