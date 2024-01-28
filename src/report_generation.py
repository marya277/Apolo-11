import os
import json
import pandas as pd
import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Define las rutas a las carpetas 'devices' y 'reports'
devices_path = Path('data/devices')
reports_path = Path('data/reports')
reports_path.mkdir(exist_ok=True)

# Inicializa variables para contar las ejecuciones
execution_number = 0

# Función para leer los archivos log y convertirlos en un dataframe
def read_logs_and_create_dataframe(devices_path):
    current_year = datetime.now().year
    events_data = []
    for folder in devices_path.iterdir():
        if str(current_year) in folder.name and folder.is_dir():
            for log_file in folder.glob('*.log'):
                with open(log_file, 'r') as file:
                    try:
                        log_data = json.load(file)
                        events_data.append(log_data)
                    except json.JSONDecodeError:
                        print(f"Error reading {log_file}")
    return pd.DataFrame(events_data)

# Función principal que genera el reporte
def generate_report():
    global execution_number
    while True:
        if not any(devices_path.iterdir()):
            print("Waiting for event files...")
            time.sleep(20)
            continue

        df = read_logs_and_create_dataframe(devices_path)
        
        if df.empty:
            print("No event files found to generate the report.")
            return

        # Análisis de eventos por estado para cada misión y tipo de dispositivo
        event_analysis = df.groupby(['mission', 'device_type', 'device_status']).size().reset_index(name='count')

        # Gestión de desconexiones
        unknown_status_df = df[df['device_status'] == 'Unknown']
        unknown_status = unknown_status_df.groupby(['mission', 'device_type']).size().reset_index(name='unknown_count')
        unknown_status = unknown_status.sort_values(by='unknown_count', ascending=False)

        # Consolidación de misiones
        killed_status_df = df[df['device_status'] == 'Killed']
        killed_status = killed_status_df.groupby(['device_type']).size().reset_index(name='killed_count')

        # Cálculo de porcentajes
        percentages = df.groupby(['mission', 'device_type']).size().reset_index(name='count')
        percentages['percentage'] = (percentages['count'] / df.shape[0]) * 100

        # Crear el dataframe para el reporte
        report_df = pd.concat([event_analysis, unknown_status, killed_status, percentages], axis=1)

        # Guardar el dataframe como un archivo CSV
        execution_number += 1
        report_filename = f'activity_report_executionnumber_{execution_number}.csv'
        report_df.to_csv(reports_path / report_filename, index=False)
        print(f"Report generated: {report_filename}")
        break

# Llama a la función principal si reports.py se ejecuta directamente
if __name__ == "__main__":
    generate_report()