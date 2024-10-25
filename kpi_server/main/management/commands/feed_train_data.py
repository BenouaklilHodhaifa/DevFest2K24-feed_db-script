import pandas as pd
import requests
from tqdm import tqdm
from pathlib import Path
import random

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

def feed_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "commands/train_set_rec.csv"

    df = pd.read_csv(file_path)
    
    # Split into separate DataFrames by KPI_Name
    kpi_name_values = df['KPI_Name'].unique()
    dfs = {kpi_name: df[df['KPI_Name'] == kpi_name] for kpi_name in kpi_name_values}
    
    # Create iterators for each DataFrame
    iterators = {
        kpi_name: get_data_entry(kpi_df) 
        for kpi_name, kpi_df in dfs.items()
    }
    
    # Keep track of which DataFrames still have data
    active_dfs = set(dfs.keys())
    
    with tqdm(total=len(df)) as pbar:
        while active_dfs:
            # Randomly select a DataFrame to process
            kpi_name = random.choice(list(active_dfs))
            try:
                # Get next row from selected DataFrame
                _, row = next(iterators[kpi_name])
                data = prepare_data(dict(row))
                
                # Send the data
                response = requests.post('https://devfest2k24-backend.onrender.com/kpi/', json=data)
                
                if response.status_code != 200:
                    print(f"Error sending data for {kpi_name}: {response.status_code}")
                
                pbar.update(1)
                
            except StopIteration:
                # This DataFrame has no more data
                active_dfs.remove(kpi_name)
                print(f"\nFinished processing {kpi_name}")
