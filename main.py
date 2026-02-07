# Libraries
from fastapi import FastAPI,Path
import json

# App object Instantiated
app = FastAPI()

# Path to data.
file_path = 'pokemon.json'

# A simple helper function to load data and return pokemon data.
def load_data():
    with open(file_path,'r') as f:
        data = json.load(f)
    return data

# The Main Pokemon Management System Page
@app.get('/')
def main_page():
    return {
                'message' : 'A Pokemon Management System'
    }

# The About Page of the website
@app.get('/about')
def about_page():
    return {
                'message' : 'A simple Pokemon Management System to get a overview of the Pokemons when we '
                             'dont have our poketab with us.'
    }

# The view page which will display the overall information of the pokemons.
@app.get('/view')
def view():
    data = load_data()
    return data

# Path Param function
@app.get('/view/{pokemon_id}')
def view_pokemon(pokemon_id:str = Path(     
                                            # Path Function parameters and Validation.
                                            ...,
                                            description = 'A Integer Number ID of the Pokemon',
                                            example = '1,5,10'
                            )
):

    data = load_data()

    if pokemon_id in data:
        return data[pokemon_id]
    return {
                'message' : 'Pokemon Not Found @__@'
            }
