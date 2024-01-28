from argparse import ArgumentParser
from simulation_engine import Simulator

from pathlib import Path

from base_classes import BaseMission, BaseDevice

from time import sleep as delay
from typing import Dict, Generator

from storing_handling import (save_records,
    create_folder, move_folder)

from tabulate import tabulate
from colorama import Fore


def run_command(args) -> None:
    try:
        simulator: Simulator = Simulator(config_path=args.config[0])
        
        while True:
            # print(simulator.config.root_folder_storage)
            msn: BaseMission = BaseMission(**simulator.select_mission())
            # print(mission)
            # Max Number Of Devices
            max_devs: int = simulator.total_number_of_devices()
            rec_per_dev: Dict[str, int] = simulator. \
            randomly_distribute_devices(
                mission=msn,
                total_amount=max_devs)
            table = list(rec_per_dev.items())
            table.append(("Total", sum(rec_per_dev.values())))
            headers = ["Device", "Amount"]
            print(tabulate(table, headers, tablefmt="grid"))
            records: Generator[BaseDevice, None, None] = simulator.generate_records(dev_dist=rec_per_dev,
                    msn=msn)
            store_path: Path = create_folder(dev_folder_path=simulator. \
                config.devices_folder)
            save_records(devs=records, store_path=store_path)
            delay(simulator.operation_interval)
            move_folder(src=store_path, dst=simulator.config.backup_folder)
    except KeyboardInterrupt:
        print("Exiting...")
        exit(1)

def main() -> None:
    parser = ArgumentParser(description="Apolo-11 Simulator")
    subparsers = parser. \
    add_subparsers(dest="command", help="Available commands")

    # Create a 'run' subcommand
    run_parser = subparsers.add_parser("run", help="Run the simulator")
    run_parser.add_argument("-c", "--config",
        action="store", nargs=1, default="configuration.toml",
        required=False, help="Specify the path to the configuration file",
        metavar="PATH", dest="config", type=str)
    run_parser.set_defaults(func=run_command)

    args = parser.parse_args()

    # Check if a subcommand was provided
    if not hasattr(args, 'func'):
        parser.print_help()
    else:
        args.func(args)

if __name__ == "__main__":
    main()  