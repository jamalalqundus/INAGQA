#******************************************************************************#
#* Name:     main.py                                                          *#
#*                                                                            *#
#* Desc clientIDtion:                                                               *#
#*  Accepts the requests of semantic-api. Either a question (query) is asked  *#
#*  and forwarded to answerFromAPI4KB() or a company card is written to API4KB.  *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#

import os
import sys
from flask import request, make_response, send_file

from .fromAPI4KB import *
from .spellCheck import *
from .virtuoso import *
from .performQuery import *
from .validation import *
from .getEntity import *
from .suggestAnswer import *
from .suggestQuestion import *

import logging

def getText(text):
    filename = "text-generator.txt"
    with open(filename, "w") as fp:
        fp.write(text)
    return makeResponse(request, send_file(filename, as_attachment=True, attachment_filename = filename))


def handleCookie(request):
    if 'client-id' in request.cookies:
        return request.cookies.get('client-id')
    else:
        return str(uuid.uuid4())

def makeResponse(request, content, clientID=None):
    if clientID is None:
        clientID = handleCookie(request)
    response = make_response(content)
    response.set_cookie("client-id", value=clientID)
    return response 

def query(query, generatorMode):
    print("generatorMode: ", generatorMode)
    try:

        if 'client-id' in request.cookies:
            clientID = request.cookies.get('client-id')
        else:
            clientID = str(uuid.uuid4())
        print("Query: ", query)
        
        questionID = '[' + str(uuid.uuid4()) + ']'

        if query:
            questionOrig = query
            response = []
            # First try without spell check
            try:
                response = answerFromAPI4KB(query, clientID, questionID, questionOrig, '')
                print(response)
            # If error try with spell check
            except Exception as e:
                response = answerFromAPI4KB(spelltestword(query), clientID, questionID, questionOrig, spelltestword(query))
                print(response)
                return makeResponse(request, performQuery(response), clientID), 200
        return makeResponse(request, performQuery(response), clientID), 200
            
    except Exception as e:
        return {"error": str(e)}, 500


def insert():
    try:  
        data = validate(connexion.request.json)
        insertRequest = insertCard("user-modified-dbpedia", data)
        if insertRequest.status_code == 200:
            response = jsonify(success=True)
            response.status_code = 200
            return makeResponse(request, response.json())
        else:
            response = jsonify(error="Triple Store Card Insertion Error")
            response.status_code = data.status_code
            return makeResponse(request, response.json())           
    except Exception as e:
        return {"error": str(e)}, 500

def suggestQuestion(count=5):
    return makeResponse(request, suggestQuestions(count))

def suggestAnswer():
    return makeResponse(request, suggestAnswers())

def autosuggest(query):
    return getEntity(query)
    # return makeResponse(request, getEntity(query))
