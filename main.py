# Libraries
from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import List,Annotated
import json

# The class to which we are gonna send variables when validating
class Pokemon(BaseModel):
    # Now the variables here will be the same as the variables in pokemon.json
    id : Annotated[
                    str,Field(  
                                ...,
                                description='An Integer value ID for the pokemon',
                                examples = ['10']
                    )
    ]
    name : Annotated[
                    str,Field(  
                                ...,
                                description='The name of the Pokemon',
                                examples = ['Raichu']
                    )
    ]
    types : Annotated[
                    List[str],Field(  
                                ...,
                                description='A list of values which represent the type of the pokemon',
                                examples = [['Grass' , 'Water']]
                    )
    ]
    hp : Annotated[
                    int,Field(  
                                ...,
                                description='An integer representing the  HP value of the pokemon',
                                examples = ['69'],
                                le=255,
                                ge=0
                    )
    ]
    attack : Annotated[
                    int,Field(  
                                ...,
                                description='An integer representing the attack stat of the pokemon',
                                examples = ['33'],
                                le=255,
                                ge=0
                    )
    ]
    defense : Annotated[
                    int,Field(  
                                ...,
                                description='An integer representing the defense stat of the pokemon',
                                examples = ['22'],
                                le=255,
                                ge=0
                    )
    ]
    speed : Annotated[
                    int,Field(  
                                ...,
                                description='An integer representing the speed  of the pokemon',
                                examples = ['98'],
                                le=150,
                                ge=0
                    )
    ]

    # We dont have any complex variables which are computed from other variables,but NOTE: we can also do that 
    # below is an example
    '''
    
    @computed_field
    @property
    # The function name is the name of the attribute for the object
    def average_strength(self) -> float:
        average_strength = round((self.attack+self.defense)/2,2)
        return average_strength
    

    # Suppose if we want to apply conditions to multiple field then we will use the model validator
    @model_validator(mode='after')
    def power_balance_validator(self): # Here the model is the model of all the objects
        if self.average_strength < 10:
            raise ValueError('Pokemon  Too Weak Try a Pokemon with better Attack and Defence Stats')
        return self
    
    '''

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

    # demo url : http://localhost:8000/sort?sort_by=attack&order=desc | http://localhost:8000/docs