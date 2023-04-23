import csv
import json
import pandas as pd
from apistar import App, Route, types, validators
from apistar.http import JSONResponse


def clean_dataset() -> None:
    data = pd.read_csv('marvel.csv')
    data = data.sort_values('page_id')
    data['page_id'] = data['page_id'].astype(int)
    data = data.applymap(lambda x:
                          x.replace("\/", "") 
                          if isinstance(x, str) else x)
    data.to_csv('./datos_limpio.csv', index=False)

def convert_csv_to_json() -> None:
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
CHARACTER = set([character['name'] for character in dataset.values()])
CHARACTER_ID = set([url['urlslug'] for url in dataset.values()])
PAGE_ID = set([id_marvel['page_id'] for id_marvel in dataset.values()])

# Definition
class MarvelCharacter(types.Type):
    page_id = validators.Integer(allow_null=True)
    name = validators.String(enum=list(CHARACTER))
    urlslug = validators.String(max_length=100)
    id = validators.String(allow_null=True)
    align = validators.String(max_length=100)
    eye = validators.String(max_length=50)
    hair = validators.String(max_length=50)
    sex = validators.String(max_length=15)
    gsm = validators.String(allow_null=True)
    alive = validators.String(max_length=50)
    appearances = validators.String(max_length=10)
    first_appearance = validators.String(max_length=8)
    year = validators.String(max_length=8)




# API Methods
def list_character() -> list:
    return [data for data in dataset.items()]


def create_character(marvel_character: MarvelCharacter) -> JSONResponse:
    character_id: int = len(dataset) + 1
    character = dataset.get(character_id)
    dataset[character_id] = marvel_character

    return JSONResponse(MarvelCharacter(marvel_character), 201)

    

def get_character(character_id: str) -> JSONResponse:
    character = dataset.get(character_id)

    if not character:
        error = {'Error': CHARACTER_NOT_FOUND}

        return JSONResponse(error, 404)
    
    return JSONResponse(character, 200)


# Routes
routes = [
    Route('/', method='GET', handler=list_character),
    Route('/', method='POST', handler=create_character),
    Route('/{character_id}', method='GET', handler=get_character),
]


app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)