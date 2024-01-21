from datetime import datetime
from hashlib import sha256
from json import dumps

from typing import List, Tuple

from pydantic import BaseModel, Field

class BaseMission(BaseModel):
    name: str
    abbreviation: str
    devices: list[str]

class BaseDevice(BaseModel):
    mission: BaseMission
    dtype: str
    state: str

    def __post_init__(self):
        self.date = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
        self.hash_date = datetime.now().strftime("%d%m%y%H%M%S%f")
        self.generate_hash()
    def generate_hash(self):
        data = f"{self.hash_date}-{self.mission.name}-{self.dtype}-{self.state}".encode()
        hash_object = sha256(data)
        self._hash = hash_object.hexdigest()
    def get_info(self):
        info = dict(date=self.date,
                    mission=self.mission.name,
                    device_type=self.dtype,
                    device_status=self.state,
                    _hash=self._hash)
        return dumps(info, indent=4)
# class BaseDevice:
#     def __init__(self, mission: BaseMission, dtype: str, state: str):
#         self.date = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
#         self.hash_date = datetime.now().strftime("%d%m%y%H%M%S%f")
#         self.mission = mission
#         self.dtype = dtype
#         self.state = state
#         self.generate_hash()
#     def __str__(self):
#         return f"{self.mission.name[1]} - {self.dtype} - {self.state} - {self._hash}"
#     def generate_hash(self):
#         data = f"{self.hash_date}-{self.mission.name[1]}-{self.dtype}-{self.state}".encode()
#         hash_object = sha256(data)
#         self._hash = hash_object.hexdigest()
#     def get_info(self):
#         info = dict(date=self.date,
#                     mission=self.mission.name[0],
#                     device_type=self.device_type,
#                     device_status=self.device_status,
#                     _hash=self._hash)
#         return dumps(info, indent=4)