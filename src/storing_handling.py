from typing import Generator
from pathlib import Path
from datetime import datetime
from shutil import move

def create_folder(dev_folder_path) -> Path:
    date_time: str = datetime.now().strftime("%Y%m%d%H%M%S")
    path: Path = dev_folder_path / date_time
    if not path.is_dir() or not path.exists():
        path.mkdir()
    return path
def save_records(devs: Generator[int, None, None],
        store_path: Path):
    # Obtener abreviacion de la mision
    abbr: str = next(devs).msn.abbreviation
    # Nombre de archivo
    for number, record in enumerate(devs, start=1):
        # print(number, record)
        filename: str = f"APL{abbr}-{number}.log"
        file_path: Path = store_path / filename
        with open(file_path, "w") as file:
            file.write(record.get_info())
def move_folder(src: Path, dst: Path) -> None:
    move(src=src, dst=dst)