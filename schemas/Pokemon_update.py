from pydantic import BaseModel,Field
from typing import List,Annotated,Optional
# The below model is exclusively for PUT method
class Pokemon_update(BaseModel):

    # No ID added as it will be accepted in the form of path params

    name : Annotated[
                    Optional[str],Field(  
                                default=None,
                                description='The name of the Pokemon'
                    )
    ]
    types : Annotated[
                    Optional[List[str]],Field(  
                                description='A list of values which represent the type of the pokemon',
                                default=None
                    )
    ]
    hp : Annotated[
                    Optional[int],Field(  
                                description='An integer representing the  HP value of the pokemon',
                                default=None
                    )
    ]
    attack : Annotated[
                    Optional[int],Field(  
                                description='An integer representing the attack stat of the pokemon',
                                default=None
                    )
    ]
    defense : Annotated[
                    Optional[int],Field(  
                                description='An integer representing the defense stat of the pokemon',
                                default=None
                    )
    ]
    speed : Annotated[
                    Optional[int],Field(  
                                description='An integer representing the speed  of the pokemon',
                                default=None
                    )
    ]
