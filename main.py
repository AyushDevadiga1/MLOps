# Libraries
from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json

# Modularity Imports --> Reduces Bulky code and increases modularity and is scalable
from schemas.Pokemon import Pokemon
from schemas.Pokemon_update import Pokemon_update

# App object Instantiated
app = FastAPI()

# Path to data.
file_path = 'pokemon.json'

# A simple helper function to load data and return pokemon data.
def load_data():
    with open(file_path,'r') as f:
        data = json.load(f)
    return data

# A simple helper function to write data 
def write_data(data):
    with open(file_path,'w') as f:
        json.dump(data,f,indent=4)

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
                                            examples = '10'
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
                            status_code=400,
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

# Now we have finished the Read part of the CRUD operations , but we need a request body for the other operations.
# The request body is the portion of the HTTP request that contains data sent by the client to the server typically used in 
# methods like PUT,POST and DELETE.

@app.post('/create') 
def create_pokemon(pokemon:Pokemon): # the object : our class

    # Load Existing data 
    data = load_data()

    # Check if the pokemon_id already exist 
    if pokemon.id in data :
        raise HTTPException(
                                status_code=400,
                                detail='Pokemon ID Already Exists '
        )

    # Now the logic for adding the id if the Pokemon id doesnt exist :

    data[pokemon.id] = pokemon.model_dump(exclude={'id'}) # The curly braces is needed as 

    write_data(data)

    return JSONResponse(
                            status_code=201,
                            content = 'Pokemon Added Successfully'
    )

    # Save the data into json file

 # We now for update create a new pydantic model but this time we will create such a model that the fields
 # are not required but are optional , as we dont know what the user wants to update.

 # Also we need the pokemon id to validate the existence of the pokemon and then if then update it.

@app.put('/edit/{pokemon_id}')
def update_pokemon_info(pokemon_id : str , pokemon_update : Pokemon_update):
    
    data = load_data()

    # Check if the pokemon_id exisS 
    if pokemon_id not in data :
        raise HTTPException(
                                status_code=400,
                                detail='Pokemon ID Does Not Exists '
        )

    existing_pokemon_info = data[pokemon_id]

    updated_pokemon_info = pokemon_update.model_dump(exclude_unset=True)
    # Why exclude_unset cause it only returns those dict elements which are send in the requesting body by the user

    for key,value in updated_pokemon_info.items():
        existing_pokemon_info[key] = value
        
    '''
    # Now below is the code If we had some fields that might need to be recalculated whent the field are udpated:
    # so first we create a new dict object having the new updated values

    existing_pokemon_info['id'] = pokemon_id # 
    pokemon_pydantic_obj = Pokemon(**existing_pokemon_info)

    pokemon_pydantic_obj = pokemon_pydantic_obj.model_dump(exclude='id')
    '''

    data[pokemon_id] = existing_pokemon_info

    # SAVE data
    write_data(data)

    return JSONResponse(
                            status_code=200,
                            content = 'Pokemon info updated successfully.'
    )

# Now creating the DELETE endpoint
@app.delete('/delete/{pokemon_id}')
def delete_pokemon(pokemon_id : str):

    # Load Data
    data = load_data()

    # Check if the pokemon_id exisS 
    if pokemon_id not in data :
        raise HTTPException(
                                status_code=400,
                                detail='Pokemon ID Does Not Exists '
        )
    
    # Delete the pokemon based on id
    del data[pokemon_id]

    write_data(data)

    return JSONResponse(
                            status_code = 200,
                            content = 'Pokemon Deleted Successfully'
    )

    # demo url : http://localhost:8000/sort?sort_by=attack&order=desc | http://localhost:8000/docs