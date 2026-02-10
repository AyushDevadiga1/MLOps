from typing import List,Annotated
from pydantic import BaseModel,Field

# The class to which we are gonna send variables when validating
class Pokemon(BaseModel):
    # Now the variables here will be the same as the variables in pokemon.json
    id : Annotated[
                    str,Field(  
                                ...,
                                description='An Integer value ID for the pokemon',
                                examples = ['26']
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