
from datetime import datetime
from hashlib import sha256
from json import dumps

# MISSIONS BLOCK
class BasicMission:
    def __init__(self, mission_name: tuple):
        # 0- Nombre normal
        self.mission_name = (mission_name[0],
        # 1- Nombre clave
                            mission_name[1])
    def __str__(self):
        return self.mission_name[0]

class OrbitOne(BasicMission):
    DEVICES = ("satellite", "spacecraft", "spacesuit")
    def __init__(self):
        super().__init__(mission_name=("OrbitOne",
                                        "ORBONE"))
class ColonyMoon(BasicMission):
    DEVICES = ("satellite", "spacecraft", "spacesuit", "spacecars")
    def __init__(self):
        super().__init__(mission_name=("ColonyMoon",
                                        "CLNM"))
class VacMars(BasicMission):
    DEVICES = ("satellite", "spacecraft", "spacesuit", "spacecars")
    def __init__(self):
        super().__init__(mission_name=("VacMars",
                                        "VCMS"))
class GalaxyTwo(BasicMission):
    DEVICES = ("satellite", "spacecraft", "spacesuit", "scientific_equipment")
    def __init__(self):
        super().__init__(mission_name=("GalaxyTwo",
                                        "GXTO"))
# END MISSIONS BLOCK


# COMPONENTS BLOCK
class BasicComponent:
    def __init__(self, mission: BasicMission, **kwargs):
        self.date = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
        self.hash_date = datetime.now().strftime("%d%m%y%H%M%S%f")
        self.mission = mission
        self.__dict__.update(kwargs)
        self.generate_hash()
    def __str__(self):
        return f"{self.mission.mission_name[1]} - {self.device_type} - {self.device_state} - {self._hash}"
    
    def generate_hash(self):
        data_to_hash = f"{self.hash_date}-{self.mission.mission_name[1]}-{self.device_type}-{self.device_state}".encode()
        hash_object = sha256(data_to_hash)
        self._hash = hash_object.hexdigest()

    def get_info(self):
        info = {
            "date": self.date,
            "mission": self.mission.mission_name[0],
            "device_type": self.device_type,
            "device_status": self.device_state,
            "hash": self._hash
        }
        return dumps(info)
# END COMPONENTS BLOCK