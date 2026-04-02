#******************************************************************************#
#* Name:     main.py                                                          *#
#*                                                                            *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#
from .heads import *
from flask import request, jsonify


def get_relation():
    data = request.json
    response = {'URIs': list(get_rel(data['question']))}
    return response

