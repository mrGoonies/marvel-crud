import csv
import json
import pandas as pd

def clean_dataset():
    data = pd.read_csv('marvel.csv')
    data = data.sort_values('page_id')
    data['page_id'] = data['page_id'].astype(int)
    data = data.applymap(lambda x:
                          x.replace("\/", "") 
                          if isinstance(x, str) else x)
    data.to_csv('./datos_limpio.csv', index=False)

def convert_csv_to_json():
    with open('datos_limpio.csv', 'r') as csvfile:
        read_csv = csv.DictReader(csvfile)
        list_dict = [row for row in read_csv]

        with open('dataset.json', 'w') as jsonfile:
            json.dump(list_dict, jsonfile, indent=4)



def load_data() -> dict:
    with open('dataset.json') as jsonfile:
        content = json.loads(jsonfile.read())
        
        return {data['page_id']: data for data in content}

clean_dataset()
convert_csv_to_json()
dataset = load_data()
CHARACTER_NOT_FOUND = 'Character not found'



