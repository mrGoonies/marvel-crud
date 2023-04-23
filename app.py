import csv
import pandas as pd

def clean_dataset():
    data = pd.read_csv('marvel.csv')
    data = data.sort_values('page_id')
    data['page_id'] = data['page_id'].astype(int)
    data = data.applymap(lambda x: x.replace("\/", "") if isinstance(x, str) else x)
    data.to_csv('./datos_limpio.csv', index=False)

def load_data() -> list:
    with open('datos_limpio.csv') as csvfile:
        content = csv.reader(csvfile, delimiter=';', quotechar='"')
        
        return [data for data in content]


clean_dataset()
dataset = load_data()
CHARACTER_NOT_FOUND = 'Character not found'



