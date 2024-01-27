from tomllib import loads as toml_loads
from random import choice as random_choice
from random import randint
from datetime import datetime
from base_classes import BaseMission, BaseDevice
from typing import Dict, List, Any, Generator, Union
from pydantic import BaseModel, validator


from custom_exceptions import (
    InvalidIntervalError,
    InvalidStoringPath,
    InvalidMaxNumber
)

from pathlib import Path


class MissionConfig(BaseModel):
    name: str
    abbreviation: str
    devices: List[str]

class Configuration(BaseModel):
    root_folder_storage: str
    devices_folder: str
    backup_folder: str
    interval: int
    max_number_devices: int
    states: List[str]
    date_format: str
    hash_date_format: str
    log_file_pattern: str
    exit_message: str
    missions: Dict[str, Any]
    @validator("interval")
    def validate_interval(cls, value):
        if value < 10 or value > 30:
            raise InvalidIntervalError(itvl=value)
        return value
    @validator("root_folder_storage", "devices_folder",
        "backup_folder")
    def validate_storing_folders(cls, v):
        if r"<root>" in v:
            path = v.replace(r"<root>", str(Path(__file__).parent.parent))
            path = Path(path)
            if not path.exists() and not path.is_dir():
                raise InvalidStoringPath(path=path)
            return path
        return v
    @validator("max_number_devices")
    def validate_max_n_devices(cls, value):
        if value < 10 or value > 300:
            raise InvalidMaxNumber(nbr=value)
        return value
class Simulator:
    def __init__(self):

        self.load_configuration()

        self.load_max_number_devices()

        self.load_devices_states()

        self.load_operation_interval()

        self.load_missions_data()


    def load_configuration(self) -> None:
        try:
            with open("new-configuration.toml", "r+") as file:
                # Read the content of the configuration file
                data: str = file.read()
                # Assign the whole content of the configuration file
                # to a class attribute
                config_content: Dict[str, Any] = toml_loads(data)
                self.config: Configuration = \
                Configuration(**config_content)

        except FileNotFoundError:
            print("[-] The configuration file does not exists")
            exit(1)

    def load_max_number_devices(self) -> None:
        self.max_number_devices: int = self.config. \
        max_number_devices

    def load_devices_states(self) -> None:
        self.devices_states: List[str] = self.config.states

    def load_operation_interval(self) -> None:
        self.operation_interval: int = self.config.interval

    def load_missions_data(self) -> None:
        self.orbit_one: Dict[str, MissionConfig] = self.config. \
        missions["orbit_one"]
        self.colony_moon: Dict[str, MissionConfig] = self.config. \
        missions["colony_moon"]
        self.vac_mars: Dict[str, MissionConfig] = self.config. \
        missions["vac_mars"]
        self.galaxy_two: Dict[str, MissionConfig] = self.config. \
        missions["galaxy_two"]

    def select_mission(self) -> dict[str, MissionConfig]:
        return random_choice((
                            self.orbit_one,
                            self.colony_moon,
                            self.vac_mars,
                            self.galaxy_two
                            ))

    def total_number_of_devices(self) -> int:
        return randint(1, self.max_number_devices+1)

    def randomly_distribute_devices(self, mission: BaseMission,
                                    total_amount: int) -> dict:
        records_per_device: Dict[str, int] = {d: 0 for d in mission.devices}
        remaining: int = total_amount

        for device in records_per_device.keys():
            n: int = randint(0, remaining)
            records_per_device[device] = n
            remaining -= n

        remaining = total_amount - sum(records_per_device.values())
        records_per_device["unknow"] = remaining
        return records_per_device

    
    def generate_records(self, dev_dist: Dict[str, int],
            msn: BaseMission) -> Generator:
        for dev, amount in dev_dist.items():
            # mission: BaseMission = msn
            # print(rcd)
            for _ in range(0, amount):
                dve: BaseDevice = BaseDevice(msn=msn, dev_type=dev,
                    state=random_choice(self.config.states),
                    date_fmt=self.config.date_format,
                    hash_dt_fmt=self.config.hash_date_format)
                yield dve
    
    # def create_iteration_folder(devices_folder: Path) -> Path:
    def create_iteration_folder(self) -> Path:
        # Crea una subcarpeta basada en la fecha y hora actual para la iteración
        iteration_folder: Path = self.config.devices_folder / datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Verifica si la carpeta ya existe, y si no, la crea
        if not iteration_folder.exists():
            iteration_folder.mkdir()

        # print(f"Iteration folder created: {iteration_folder}")
        return iteration_folder
