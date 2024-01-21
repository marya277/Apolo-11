from tomllib import loads as toml_loads
from random import choice as random_choice
from random import randint

from base_classes import BaseMission

class Simulator:
    missions = ("orbit_one", "colony_moon", "vac_mars", "galaxy_two")
    def __init__(self):
        self.load_configuration()

        self.load_max_number_of_devices()

        self.load_devices_states()

        self.load_operation_delay()

        self.load_missions_data()

    
    def load_configuration(self):
        try:
            with open("new-configuration.toml", "r+") as file:
                # Read the content of the configuration file
                data = file.read()
                # Assign the whole content of the configuration file
                # to a class attribute
                self.raw_config = toml_loads(data)
                
                # Load the devices states 
                # self.states: list(str) = self.raw_config["states"]

        except FileNotFoundError:
            print("[-] The configuration file does not exists")
            exit(1)
    
    def load_max_number_of_devices(self):
        self.max_number_devices: int = self.raw_config["max_number_of_devices"]

    def load_devices_states(self) -> None:
        self.devices_states: list[str] = self.raw_config["states"]

    def load_operation_delay(self) -> None:
        self.operation_delay: int = self.raw_config["delay"]

    def load_missions_data(self) -> None:
        self.orbit_one = self.raw_config["missions"]["orbit_one"]
        self.colony_moon = self.raw_config["missions"]["colony_moon"]
        self.vac_mars = self.raw_config["missions"]["vac_mars"]
        self.galaxy_two = self.raw_config["missions"]["galaxy_two"]

    def select_mission(self) -> str:
        return self.orbit_one
    
    def total_number_of_devices(self) -> int:
        return randint(1, self.max_number_devices+1)

    def randomly_distribute_devices(self, mission: BaseMission,
                                    total_amount: int) -> dict:
        files_per_device = {d: 0 for d in mission.devices}
        remaining = total_amount

        for device in files_per_device.keys():
            n = randint(0, remaining)
            files_per_device[device] = n
            remaining -= n

        remaining = total_amount - sum(files_per_device.values())
        files_per_device["unknow"] = remaining
        return files_per_device