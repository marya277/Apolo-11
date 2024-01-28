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
reports_path.mkdir(exist_ok=True)  # Crea la carpeta si no existe

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
        event_analysis = df.groupby(['mission', 'device_type', 'device_status']).size()

        # Gestión de desconexiones
        unknown_status = df[df['device_status'] == 'Unknown'].groupby(['mission', 'device_type']).size().sort_values(ascending=False)

        # Consolidación de misiones
        killed_status = df[df['device_status'] == 'Killed'].groupby('device_type').size()

        # Cálculo de porcentajes
        total_events = df.shape[0]
        percentages = (df.groupby(['mission', 'device_type']).size() / total_events) * 100

        # Crear el dataframe para el reporte
        report_df = pd.DataFrame({
            'Event Analysis': event_analysis,
            'Disconnections': unknown_status,
            'Killed Status Consolidation': killed_status,
            'Percentages': percentages
        })

        # Guardar el dataframe como un archivo CSV
        execution_number += 1
        report_filename = f'activity_report_executionnumber_{execution_number}.csv'
        report_df.to_csv(reports_path / report_filename)
        print(f"Report generated: {report_filename}")
        break

# Llama a la función principal si reports.py se ejecuta directamente
if __name__ == "__main__":
    generate_report()
