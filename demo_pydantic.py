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

from pydantic import BaseModel

# Always use BaseModel as we dont have __init_ function and use hints to validate dtype instead .
class Pokemon(BaseModel):

    # Defined schema / Rules
    name : str 
    age : int 

# Our Main function
def load_pokemon(pokemon : Pokemon): # Now instead of getting the variables independently we get a Pokemon object , so we modify the logic accordingly.
    print(f'{pokemon.name}\n{pokemon.age}')
    print('Variables validated successfuly !')

pokemon_info = { 'name' : 'Ghastly' , 'age' : 'hellow'}

poke1 = Pokemon(**pokemon_info)
load_pokemon(poke1)