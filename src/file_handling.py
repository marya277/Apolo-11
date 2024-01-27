from typing import Generator
from pathlib import Path

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
    
    