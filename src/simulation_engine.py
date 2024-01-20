from main import *

# Librerias para manejo de archivos y directorios
from pathlib import Path
from os.path import isfile
from os import mkdir, listdir
from shutil import move
# Librerias para manejo de archivos y directorios

from time import sleep
from random import choice, randint

from signal import signal, SIGINT

from json import dumps

class Simulator:
    MISSIONS = ("ORBONE", "CLNM", "VCMS", "GXTO")
    def __init__(self, dfp: Path, bfp: Path, interval: int=20):
        self.DEVICES_FOLDER_PATH = dfp
        self.BASE_BACKUP_FOLDER_PATH = bfp
        self.INTERVAL = interval
        self.DEVICES_STATES = ("excellent", "good", 
                                "warning", "faulty", 
                                "killed", "unknow")

    def start_simulation(self):
        while True:
            mission = choice(self.MISSIONS)
            print(mission)
            total_files = randint(1, 101)
            match mission:
                case "ORBONE":
                    mission = OrbitOne()
                    data = self.generate_devices_data(mission=mission, files_number=total_files)
                    self.write_data(data=data, mission=mission.mission_name[1])
                case "CLNM":
                    mission = ColonyMoon()
                    data = self.generate_devices_data(mission=mission, files_number=total_files)
                    self.write_data(data=data, mission=mission.mission_name[1])
                case "VCMS":
                    mission = VacMars()
                    data = self.generate_devices_data(mission=mission, files_number=total_files)
                    self.write_data(data=data, mission=mission.mission_name[1])
                case "GXTO":
                    mission = GalaxyTwo()
                    data = self.generate_devices_data(mission=mission, files_number=total_files)
                    self.write_data(data=data, mission=mission.mission_name[1])
            sleep(10)
    def generate_devices_data(self, mission, files_number):
        print("Numero total de archivos en esta iteracion:", files_number)
        # The "data" variable will contains all the records generated afterwards
        data = []

        # Set the number of records per device to 0 initially inside a dictionary
        files_per_device = {d: 0 for d in mission.DEVICES}

        # Set initially the value of the variable that will contain the remaining number
        # of records for create equal to the total number of records
        remaining = files_number

        # Iterates over each key of the "files_per_device" dictionary to get the devices
        # one by one and randomly assign a number of records to that device
        for device in files_per_device.keys():
            # Random number generation
            n = randint(0, remaining)
            # Assign that random number to the device on the current iteration
            files_per_device[device] = n
            # Decreasing the number of the variable "remaining" by substracting
            # the value of the random number
            remaining -= n

        # If there is any value on the "remaining" variable it will be assigned
        # to the unknow devices
        remaining = files_number - sum(files_per_device.values())
        files_per_device['unknow'] = remaining
        print("Diccionario que contiene el numero de registros para cada dispositivo:", files_per_device)

        # Generate records for each device based on its number of records
        # using list comprehensions generate devices with atributes and data
        for device, number in files_per_device.items():
            # If the device is not unknow, generate the records normally
            if device != "unknow":
                generated_data = [BasicComponent(device_state=choice(self.DEVICES_STATES[:5]),
                                                device_type=device,
                                                mission=mission) for d in range(0, number)]
                data.extend(generated_data)
            # 
            else:
                generated_data = [BasicComponent(device_state="unknow",
                                                device_type="unknow",
                                                mission=mission) for d in range(0, number)]
                data.extend(generated_data)
        return data

    def write_data(self, data, mission):
        date_backup_folder = data[0].hash_date[:12]
        for index, record in enumerate(data, start=1):
            filename = f"APL{mission}-{index}.log"
            file_path = self.DEVICES_FOLDER_PATH / filename
            data = {"index": index, "data": record.get_info()}
            with open(file_path, "w+") as file:
                file.write(dumps(data, indent=2))
        self.generate_backup_folder(date=date_backup_folder)
        self.files_to_backup(origin=self.DEVICES_FOLDER_PATH, destination=self.current_backup_folder_path)
    
    def generate_backup_folder(self, date):
        self.current_backup_folder_path = self.BASE_BACKUP_FOLDER_PATH / date
        mkdir(path=self.current_backup_folder_path)
    def files_to_backup(self, origin=None, destination=None):
        # backup_path = self.current_backup_folder_path
        files = [f for f in listdir(self.DEVICES_FOLDER_PATH) if isfile(self.DEVICES_FOLDER_PATH / f)]
        for file in files:
            origin_path = origin / file
            destination_path = destination / file
            move(src=origin_path, dst=destination_path)
def signal_handler(signum, frane):
    print("Exiting...")
    exit(0)
    #entry point
if __name__ == "__main__":
    signal(SIGINT, signal_handler)
    dfp = Path(__file__).parent.parent / "data" / "devices"
    bfp = Path(__file__).parent.parent / "data" / "backup"
    simulator = Simulator(dfp=dfp, bfp=bfp)
    simulator.start_simulation()