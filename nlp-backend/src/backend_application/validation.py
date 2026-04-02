#******************************************************************************#
#* Name:     validation.py                                                    *#
#* Author:   ssa                                                              *#
#*                                                                            *#
#* Description:                                                               *#
#*  Validate user modifications and input and transform the company card      *#
#*  into the proper format for the SPARQL query generation.                   *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#

import json
import random
import requests
from pydantic import BaseModel, ValidationError, validator
from typing import Union


class User(BaseModel):
    property: str
    type: str
    value: Union[int, float, str]

    @validator('type')
    def check_type(cls, v, values):
        if not v in ["literal", "typed-literal", "added"]:
            raise ValueError('Illegal property type in property: %s' % values['property'])
        return v


def validate(data):
    properties = data['properties']
    try:
        cleaned_properties = [dict(User(**property)) for property in properties]

        user_added, not_modified = [], []
        for property in cleaned_properties:
            user_added.append(property) if property['type'] == 'added' else not_modified.append(property) 
        
        for property in user_added:
            if isinstance(property['value'], int) or isinstance(property['value'], float):
                property['type'] = 'typed-literal'
            else:
                property['type'] = 'literal'

        data['properties'] = not_modified + user_added
        return data

    except (ValidationError, ValueError) as e:
        for error in json.loads(e.json()):
            return error['msg']


def transformToNLPFormat(data):
    sparqlJSON = {
        "entity":data['entity'],
        "title":data['title']
    }

    if "thumbnail" in data:
        sparqlJSON['thumbnail'] = data['thumbnail']

    for property in data['properties']:
        sparqlJSON[property['property']] = property['value']

    return sparqlJSON



