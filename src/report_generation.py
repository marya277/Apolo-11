import os
import json
from pathlib import Path
import pandas as pd
import time
from datetime import datetime
from typing import List, Dict, Any

from tabulate import tabulate

devices_path: Path = Path('data/devices')
reports_path: Path = Path('data/reports')
reports_path.mkdir(exist_ok=True)

execution_number: int = len(list(reports_path.glob('activity_report_executionnumber_*.csv')))

def read_logs_and_create_dataframe(devices_path: Path) -> pd.DataFrame:
    current_year: int = datetime.now().year
    events_data: List[Dict[str, Any]] = []
    for folder in devices_path.iterdir():
        if str(current_year) in folder.name and folder.is_dir():
            for log_file in folder.glob('*.log'):
                with open(log_file, 'r') as file:
                    try:
                        log_data: Dict[str, Any] = json.load(file)
                        events_data.append(log_data)
                    except json.JSONDecodeError as e:
                        print(f"Error reading {log_file}: {e}")
    return pd.DataFrame(events_data)

def generate_report() -> None:
    global execution_number
    while True:
        if not any(devices_path.iterdir()):
            print("Waiting for event files...")
            time.sleep(20)
            continue

        df: pd.DataFrame = read_logs_and_create_dataframe(devices_path)
        
        if df.empty:
            print("No event files found to generate the report.")
            return

        # Análisis de eventos por estado para cada misión y tipo de dispositivo
        event_analysis: pd.DataFrame = df.groupby(['mission', 'device_type', 'device_status']).size().reset_index(name='count')

        # Gestión de desconexiones
        unknown_status_df: pd.DataFrame = df[df['device_status'] == 'Unknown']
        unknown_status: pd.DataFrame = unknown_status_df.groupby(['mission', 'device_type']).size().reset_index(name='unknown_count')
        unknown_status = unknown_status.sort_values(by='unknown_count', ascending=False)

        # Consolidación de misiones
        killed_status_df: pd.DataFrame = df[df['device_status'] == 'Killed']
        killed_status: pd.DataFrame = killed_status_df.groupby(['device_type']).size().reset_index(name='killed_count')

        # Cálculo de porcentajes
        percentages: pd.DataFrame = df.groupby(['mission', 'device_type']).size().reset_index(name='count')
        percentages['percentage'] = (percentages['count'] / df.shape[0]) * 100

        # Crear el dataframe para el reporte
        report_df: pd.DataFrame = pd.concat([event_analysis, unknown_status, killed_status, percentages], axis=1)

        # Guardar el dataframe como un archivo CSV
        execution_number += 1
        report_filename: str = f'activity_report_executionnumber_{execution_number}.csv'
        report_df.to_csv(reports_path / report_filename, index=False)
        print(f"Report generated: {report_filename}")
        report_df.fillna(0, inplace=True)

        # Generación de tabla en dos partes
        columns_part1: List[str] = ['mission', 'device_type', 'device_status']
        columns_part2: List[str] = ['mission', 'count', 'unknown_count', 'killed_count', 'percentage']

        report_part1: pd.DataFrame = report_df[columns_part1]
        report_part2: pd.DataFrame = report_df[columns_part2]

        # Primera parte de la tabla 
        print("\nTable (Part 1) representation of the report:")
        print(tabulate(report_part1, headers='keys', tablefmt='pretty', showindex=False))

        # Segunda parte de la tabla
        print("\nTable (Part 2) representation of the report:")
        print(tabulate(report_part2, headers='keys', tablefmt='pretty', showindex=False))

        break

if __name__ == "__main__":
    generate_report()
