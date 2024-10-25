import pandas as pd
import requests
from tqdm import tqdm
from pathlib import Path
import random
import concurrent.futures

def get_data_entry(df):
    for index, row in df.iterrows():
        yield index, row

def prepare_data(data):
    data['timestamp'] = data['Timestamp']
    data.pop('Timestamp')
    data['kpi_value'] = float(data['KPI_Value'])
    data.pop('KPI_Value')
    data['kpi_name'] = data['KPI_Name']
    data.pop('KPI_Name')
    data['status'] = True if int(data['Status']) == 1 else False
    data.pop('Status')
    return data



def process_kpi_df(kpi_name, kpi_df):
    print(f"\nProcessing {kpi_name}")
    for _, row in tqdm(get_data_entry(kpi_df)):
        data = prepare_data(dict(row))
        response = requests.post('https://devfest2k24-backend.onrender.com/kpi/', json=data)

def feed_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "commands/train_set_rec.csv"
    
    # Read the main DataFrame
    df = pd.read_csv(file_path)
    
    # Split into separate DataFrames by KPI_Name
    kpi_name_values = df['KPI_Name'].unique()
    dfs = {kpi_name: df[df['KPI_Name'] == kpi_name] for kpi_name in kpi_name_values}
    
    # Process DataFrames concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(kpi_name_values)) as executor:
        futures = [
            executor.submit(process_kpi_df, kpi_name, kpi_df) 
            for kpi_name, kpi_df in dfs.items()
        ]
        concurrent.futures.wait(futures)