from datetime import datetime
from hashlib import sha256
from json import dumps

from typing import List, Tuple

from pydantic import BaseModel, Field

from dataclasses import dataclass

@dataclass
class BaseMission:
    name: str
    abbreviation: str
    devices: List[str]

    def __str__(self):
        return f"{self.name}-{self.abbreviation} | {self.devices}"

@dataclass
class BaseDevice:
    msn: BaseMission
    dev_type: str
    state: str
    date_fmt: str
    hash_dt_fmt: str

    def __post_init__(self):
        self.date = datetime.now().strftime(self.date_fmt)
        self.hash_date = datetime.now().strftime(self.hash_dt_fmt)
        self.generate_hash()
    def generate_hash(self) -> None:
        data = f"{self.hash_date}-{self.msn.name}-{self.dev_type}-{self.state}".encode()
        hash_object = sha256(data)
        self._hash = hash_object.hexdigest()
    def get_info(self):
        info = dict(date=self.date,
                    mission=self.msn.name,
                    device_type=self.dev_type,
                    device_status=self.state,
                    _hash=self._hash)
        return dumps(info, indent=4)
