'''
def load_pokemon(name : str , age : int):
    print(name,age)
    print('Variables validated successfuly !')
load_pokemon('ghastly','one')
'''
# If we execute the above code it will run without error cause python does not have a error raising mechanism 
# for the data when passed , instead the variables are dynamically associated with the data passed.

# To counter this we might use something like this 

'''
def load_pokemon(name : str , age : int):
    if type(name) == str and type(age) == int:
        return('Variables validated successfuly !')
    else:
        raise TypeError('Invalid Datatype')
load_pokemon('ghastly','one')
'''
# Now if we run this we would we able to validate the dtype , now imaging doing this for bigger tasks.
# Not SCALABLE right ? Alson we havent even talked about the data validation inside : 
# for example : age must be in the range 0 - 100 . 
# Now more code @-@ , to handle this we have the pydantic module.


# Steps for Pydantic : 
'''
'''

# Now rewrittng with pydantic version

from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Optional,Annotated

# Always use BaseModel as we dont have __init_ function and use hints to validate dtype instead .
class Pokemon(BaseModel):

    # Defined schema / Rules for Data Validation
    # By default the values are necessary when object is instantiated and if any of the value is not passed we would get a error.
    # The Field keyword is use to set data constraints / Custom Data Validation

    # We use Annotated to provide some metadata ; syntax : Annotated[dtype,Field(Params)]

    name : Annotated[
                        str,Field(
                        max_length=20,
                        title='Name of the pokemon',
                        description='The Name must be of type `str` and must be of max length 20',
                        examples=['haunter','gangar']
                        )
                    ]
    age : int 
    attack : int = Field(gt=0 ,lt=100)
    defense : int = Field(gt=0 ,lt=100)
    desc : List[str] # We are validating the container and the elemnt also (2Way).
    legendary : Annotated[
                            bool,Field(
                            default=False,
                            strict=True  # No Type Conversion
                            )
                    ]
    photo : AnyUrl
    email : EmailStr
    
    # We use this when we have custom logic which cant be handled by the CustomDtypes by Pydantic
    @field_validator('email') # To validate the email
    @classmethod # To specify the method type , can be ommited as it is by default behavioue

    def email_validator(cls,value): # To pass the class instance and the value for which we are validating

        valid_domains = ['gmail.com','yahoo.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a Valid Domain')
        return value

    @field_validator('name')
    @classmethod
    def upper_name(cls,value):
        return value.upper()
    
    # Field Validator is only for a single field
    @field_validator('age',mode='after') 
    # The mode when set to after will first perform the type coercion and then validate using the function ;
    #  by default we have default mode = 'after'
    @classmethod
    def validate_age(cls,value):
        if value>0 and value<26:
            return value
        else:
            raise ValueError('Age Should be in range 1 - 25')
    
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
    # Deprecated
    @model_validator(mode='after')
    def power_balance_validator(cls,model): # Here the model is the model of all the objects
        if (model.attack+model.defense)/2 < 10:
            raise ValueError('Pokemon Too Weak Try a Pokemon with better Attack and Defence Stats')
        return model
'''

# Our Main function
def load_pokemon(pokemon : Pokemon): # Now instead of getting the variables independently we get a Pokemon object , so we modify the logic accordingly.
    print(f'{pokemon.name}')
    print(pokemon.age)
    print(pokemon.legendary) 
    print(pokemon.average_strength)
    print('Variables validated successfuly !')

 # It is smart and will convert '20' if passed into int field automatically.
pokemon_info = {    
                    'name' : 'Ghastly' ,
                    'age' : '1' ,
                    'attack' : 1,
                    'defense' : 19,
                    'desc' : [
                                    'A cool Ghost type pokemon .'
                    ],
                    'legendary' : True,
                    'photo' : 'https://www.nicepng.com/maxp/u2w7w7q8q8w7w7e6/',
                    'email' : 'hello@gmail.com'
               }    

poke1 = Pokemon(**pokemon_info)
load_pokemon(poke1)