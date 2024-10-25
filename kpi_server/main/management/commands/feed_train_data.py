import pandas as pd
import requests
from tqdm import tqdm

def get_data_entry(df):
    for index, row in df.iterrows():
        yield index, row

def feed_data():
    df = pd.read_csv("/Users/hodhaifabenouaklil/Documents/Me/Competitions/DevFest2K24/ai-model/kpi_server/main/management/commands/train_set_rec.csv")
    for _, row in tqdm(get_data_entry(df)):
        data = dict(row)
        data['timestamp'] = data['Timestamp']
        data.pop('Timestamp')
        data['kpi_value'] = float(data['KPI_Value'])
        data.pop('KPI_Value')
        data['kpi_name'] = data['KPI_Name']
        data.pop('KPI_Name')
        data['status'] = True if int(data['Status']) == 1 else False
        data.pop('Status')

        requests.post('https://devfest2k24-backend.onrender.com/kpi/', json=data)
