#******************************************************************************#
#* Name:     suggestQuestion.py                                               *#
#*                                                                            *#
#* Description:                                                               *#
#*  Suggest possible questions to the user on the landing page animation      *#
#*  of the application. DBpedia is queried for possible entities.             *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#

import json
import random
import requests
import os

def get_companies():
    SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')
    query = """
            PREFIX  dbo:  <http://dbpedia.org/ontology/>
            PREFIX  dbp:  <http://dbpedia.org/property/>

            SELECT DISTINCT  str(?lbl)
            WHERE
            { ?s a dbo:Company ; rdfs:label ?lbl .
                FILTER( langMatches(lang(?lbl),"de") )
                ?s dbp:tradedAs <http://dbpedia.org/resource/S&P_500_Index>
            }
            """
    try:
        data = requests.get(SPARQL_ENDPOINT, params = {'query': query}).json()
    except Exception as e:
        raise RuntimeError('dbPedia Request Error' + requests.get(SPARQL_ENDPOINT, params = {'query': query}).text)
    companies = [callret['callret-0']['value'] for callret in data['results']['bindings']]
    return companies

def getQuestionsForEntity(entity, count):
    companies = get_companies()
    if not companies:
        companies = ['Daimler', 'Wirecard', 'Lufthansa', 'Adidas']

    questionSkeletons = [
        f"Wo ist {entity}?",
        f"Wo befindet sich {entity}?",
        f"{random.choice(companies)}",
        f"{random.choice(companies)}",
        f"{random.choice(companies)}",
        f"Informationen zu {entity}",
        f"Aktuelle Nachrichten zu {entity}",
        f"Nachrichten zu {entity}",
        f"Alle Nachrichten zu {entity}",
        f"Wie viele aktuelle Nachrichten gibt es zu {entity}?",
        f"Wie viele Nachrichten gibt es zu {entity}?"
        ]
    return random.sample(questionSkeletons, k=count)

def getQuestionsForEntities(entities, count):
    questions = []
    for entity in entities:
        questions.extend(getQuestionsForEntity(entity, 5))
    return random.sample(questions, k=count)

def suggestQuestions(count):
    dummyEntities = ['Daimler', 'Wirecard', 'Lufthansa', 'Adidas']
    return json.dumps({"questions":getQuestionsForEntities(dummyEntities, count)})

