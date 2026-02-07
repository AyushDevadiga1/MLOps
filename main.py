# Libraries
from fastapi import FastAPI,Path,HTTPException,Query
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
                                            example = '10'
                            )
):

    data = load_data()

    if pokemon_id in data:
        return data[pokemon_id]
    raise HTTPException(
                            status_code=404,
                            detail = 'Pokemon Not Found @_@'
    )


# Query Parameter 
@app.get('/sort')
def sort_pokemons(
                    sort_by : str = Query(
                                            ..., #The dots mean the values are required
                                            description = 'Sort Values Based on attack or defense .'
                                        ),
                    order : str = Query(
                                            'asc', # This value is not requried to fill
                                            description = 'Sort Values in Ascending or Descending order.'
                                        )
):
    valid_fields = ['attack','defense']

    # Check whether the fields are valid or not
    if sort_by not in valid_fields:
        raise HTTPException(
                            status_code=404,
                            detail = f' Invalid field select from valid_fields : {valid_fields} '
        )
    
    # Load the data
    data = load_data()

    # Sorting Logic
    is_reverse = True if order.lower() == 'desc' else False

    sorted_data = sorted(
        data.items(),
        key=lambda x: x[1].get(sort_by, 0),
        reverse=is_reverse
    )

    return dict(sorted_data)

    # demo url : http://localhost:8000/sort?sort_by=attack&order=desc | http://localhost:8000/docs