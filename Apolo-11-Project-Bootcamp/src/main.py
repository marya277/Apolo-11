from argparse import ArgumentParser
from simulation_engine import Simulator

from pathlib import Path

from json import dumps

from random import choice, randint

from base_classes import BaseMission

from time import sleep as delay

# IF - if = Iterations File
def if_exists(ifp: Path, /) -> bool:
    if ifp.is_file() and ifp.exists():
        return True
    else:
        return False

def create_if(ifp: Path, mission_names: list[str]) -> None:
    content = {mission: 0 for mission in mission_names}
    with open(ifp, "w+") as file:
        data = dumps(content, indent=4)
        file.write(data)

def run_command(args) -> None:
    simulator = Simulator()
    IFP = Path(__file__).parent.parent / "data" /  "iterations.json"
    if not if_exists(IFP):
        create_if(ifp=IFP, mission_names=simulator.missions_names)
    while True:
        m = BaseMission(**simulator.select_mission())
        print(simulator.select_mission())
        # Max Number Of Devices
        mnod = simulator.total_number_of_devices()
        print(mnod)

        files_per_device = simulator.randomly_distribute_devices(mission=m,
                                                                total_amount=mnod)
        print("Archivos por dispositivo")
        print(files_per_device)
        delay(simulator.operation_delay)

    # match simulator.select_mission():
    #     case "orbit_one":
    #         m = BaseMission(**simulator.orbit_one)
    #         print(m)
    #     case "colony_moon":
    #         pass
    #     case "vac_mars":
    #         pass
    #     case "galaxy_two":
    #         pass
    # print(list(simulator.select_mission()))

def main() -> None:
    parser = ArgumentParser(description="Apolo-11 Simulator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create a 'run' subcommand
    run_parser = subparsers.add_parser("run", help="Run the simulator")
    run_parser.set_defaults(func=run_command)

    args = parser.parse_args()

    # Check if a subcommand was provided
    if not hasattr(args, 'func'):
        parser.print_help()
    else:
        args.func(args)

if __name__ == "__main__":
    main()
