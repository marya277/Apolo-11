import os
import json
from pathlib import Path
import pandas as pd
import time
from datetime import datetime
from typing import List, Dict, Any

from tabulate import tabulate

# Define las rutas a los directorios de dispositivos y reportes.
devices_path: Path = Path('data/devices')
reports_path: Path = Path('data/reports')
reports_path.mkdir(exist_ok=True)

# Calcula el número de ejecución basándose en los reportes existentes.
execution_number: int = len(list(reports_path.glob('activity_report_executionnumber_*.csv')))

def read_logs_and_create_dataframe(devices_path: Path) -> pd.DataFrame:
    current_year: int = datetime.now().year
    events_data: List[Dict[str, Any]] = []
    
    # Itera sobre cada carpeta dentro del directorio de dispositivos.
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

        # Análisis de eventos por estado para cada misión y tipo de dispositivo.
        event_analysis: pd.DataFrame = df.groupby(['mission', 'device_type', 'device_status']).size().reset_index(name='count')

        # Gestión de desconexiones.
        unknown_status_df: pd.DataFrame = df[df['device_status'] == 'Unknown']
        unknown_status: pd.DataFrame = unknown_status_df.groupby(['mission', 'device_type']).size().reset_index(name='unknown_count')

        # Consolidación de misiones.
        killed_status_df: pd.DataFrame = df[df['device_status'] == 'Killed']
        killed_status: pd.DataFrame = killed_status_df.groupby(['mission', 'device_type']).size().reset_index(name='killed_count')

        # Cálculo de porcentajes.
        percentages: pd.DataFrame = df.groupby(['mission', 'device_type']).size().reset_index(name='event_count')
        total_events = df.shape[0]
        percentages['percentage'] = (percentages['event_count'] / total_events) * 100

        # Combina los DataFrames manteniendo las claves consistentes.
        combined_df: pd.DataFrame = pd.merge(event_analysis, unknown_status, on=['mission', 'device_type'], how='left')
        combined_df = pd.merge(combined_df, killed_status, on=['mission', 'device_type'], how='left')
        combined_df = pd.merge(combined_df, percentages, on=['mission', 'device_type'], how='left')

        # Rellena los valores NaN con 0 para las columnas de conteos.
        combined_df.fillna(0, inplace=True)

        # Guarda el dataframe como archivo CSV.
        execution_number += 1
        report_filename: str = f'activity_report_executionnumber_{execution_number}.csv'
        combined_df.to_csv(reports_path / report_filename, index=False)
        print(f"Report generated: {report_filename}")

        # Imprime la representación de la tabla.
        print("\nTable representation of the report:")
        print(tabulate(combined_df, headers='keys', tablefmt='pretty', showindex=False))
        break

if __name__ == "__main__":
    generate_report()

