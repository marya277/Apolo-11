from argparse import ArgumentParser
from simulation_engine import Simulator

from pathlib import Path

from json import dumps

from base_classes import BaseMission, BaseDevice

from time import sleep as delay
from typing import Dict, Tuple, Generator

import file_handling as fh


def run_command(args) -> None:
    try:
        simulator: Simulator = Simulator()
        # Iterations File Path
        # IFP: Path = Path(__file__).parent.parent / "data" / \
        # "iterations.json"
        # if not if_exists(IFP):
        #     create_if(IFP)
        while True:
            # print(simulator.config.root_folder_storage)
            msn = BaseMission(**simulator.select_mission())
            # print(mission)
            # Max Number Of Devices
            max_devs = simulator.total_number_of_devices()
            # print(max_devs)

            rec_per_dev = simulator. \
            randomly_distribute_devices(
                mission=msn,
                total_amount=max_devs)
            # print(rec_per_dev)
            records: Generator[BaseDevice, None, None] = simulator.generate_records(dev_dist=rec_per_dev,
                    msn=msn)
            iter_path = simulator.create_iteration_folder()
            fh.save_records(devs=records, path=iter_path)
            delay(simulator.operation_interval)
    except KeyboardInterrupt:
        print("Exiting...")
        exit(1)

def main() -> None:
    parser = ArgumentParser(description="Apolo-11 Simulator")
    subparsers = parser. \
    add_subparsers(dest="command", help="Available commands")

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