from typing import Generator
from pathlib import Path
from time import sleep as delay
def save_records(devs: Generator[int, None, None],
        path: Path):
    # Obtener abreviacion de la mision
    abbreviation = next(devs).msn.abbreviation
    # Nombre de archivo
    for number, record in enumerate(devs, start=1):
        print(number, record)
        filename = f"APL{abbreviation}-{number}.log"
        file_path = path / filename
        with open(file_path, "w") as file:
            file.write(record.get_info())
    print(abbreviation)
    
    def move_folder(src: Path, dst: Path) -> None:
        move(src=src, dst=dst)