#******************************************************************************#
#* Name:     virtuoso.py                                                      *#
#*                                                                            *#
#* Description:                                                               *#
#*  Generate SPARQL queries and wrap API4KB requests.                         *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#

import os
import json
import requests

SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT', "http://virtuoso:8890/sparql/")

# List all Graphs
#SELECT  DISTINCT ?g 
#   WHERE  { GRAPH ?g {?s ?p ?o} } 
#ORDER BY  ?g


#CLEAR GRAPH <CompanyKB>
def deleteGraph(graphName):
    query = """
            CLEAR GRAPH <""" + graphName + """>
    """
    try:
        data = requests.get(SPARQL_ENDPOINT, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text
    except Exception as e:
        raise RuntimeError('Triple Store Graph Deletion Error')
    return data


#DROP GRAPH <CompanyKB>
def dropGraph(graphName):
    query = """
            DROP GRAPH <""" + graphName + """>
    """
    try:
        data = requests.get(SPARQL_ENDPOINT, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text
    except Exception as e:
        raise RuntimeError('Triple Store Graph Dropping Error')
    return data


#CREATE GRAPH <CompanyKB>
def createGraph(graphName):
    query = """
            CREATE GRAPH <""" + graphName + """>
    """
    try:
        data = requests.get(SPARQL_ENDPOINT, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text
    except Exception as e:
        raise RuntimeError('Triple Store Graph Creation Error')
    return data


#SELECT * WHERE {
#                   GRAPH <CompanyKB>{ 
#                   ?company <latest-news> ?search . 
#                   FILTER(regex(?company, <Adidas>, "i"))   }}
def selectTriple(graphName, company, prop):
    query = """
            SELECT * WHERE {
                GRAPH <""" + graphName + """>{ 
                ?company <""" + prop + """> ?search . 
                FILTER(regex(?company, <""" + company + """>, "i"))   
                }
            }
    """
    try:
        data = requests.get(SPARQL_ENDPOINT, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).json()
    except Exception as e:
        raise RuntimeError(str(e) + 'Triple Store Triple Select Error')
    return data['results']['bindings']


#INSERT DATA {
#    GRAPH <CompanyKB> {
#    <adidas> <latest-news> "New News URL: http://news.com" .} }
def insertTriple(graphName, company, prop, insert, datatype=""):
    query = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>       
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX foaf: <http://xmlns.com/foaf/spec/>
            PREFIX xsd: <http://www.w3.org/TR/swbp-xsch-datatypes/>
            PREFIX db-datatypes: <http://dbpedia.org/datatype/>       
            PREFIX user-modified-cisqa: <http://user-modified-dbpedia/>       

            INSERT DATA
            {{
                GRAPH <{graphName}> {{
                {company} {prop} {insert}{datatype} .
                }}
            }}
    """
    try:
        data = requests.get(SPARQL_ENDPOINT, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text
    except Exception as e:
        raise RuntimeError('Triple Store Triple Insert Error')
    return data

#INSERT DATA {
#    GRAPH <CompanyKB> {
#    <adidas> <latest-news> "New News URL: http://news.com" .} }
def insertTriples(graphName, triples):
    queryTriples = " \n".join([f"{triple[0]} {triple[1]} {triple[2]}{triple[3]} ." for triple in triples])
    query = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>       
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX foaf: <http://xmlns.com/foaf/spec/>
            PREFIX xsd: <http://www.w3.org/TR/swbp-xsch-datatypes/>
            PREFIX db-datatypes: <http://dbpedia.org/datatype/>       
            PREFIX user-modified-cisqa: <http://user-modified-dbpedia/>       

            INSERT DATA
            {{
                GRAPH <{graphName}> {{
                {queryTriples}
                }}
            }}
            """
    try:
        data = requests.get(SPARQL_ENDPOINT, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text
    except Exception as e:
        raise RuntimeError('Triple Store Triple Insert Error')
    return data

#DELETE DATA {
#    GRAPH <CompanyKB> {
#    <adidas> <latest-news> "New News URL: http://news.com" .} }
def deleteTripleSpecific(graphName, company, prop, delete):
    query = """
            DELETE DATA
            {
                GRAPH <""" + graphName + """> {
                <""" + company + """> <""" + prop + """> """ + delete + """ .
                } 
            }
    """
    try:
        data = requests.get(SPARQL_ENDPOINT, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text
    except Exception as e:
        raise RuntimeError('Triple Store Graph Deletion Error')
    return data


#DELETE {GRAPH <CompanyKB> {?s ?p ?o}}
#WHERE  { ?s ?p ?o . 
#         FILTER (?s = <adidas> && ?p = <latest-news>) }
def deleteTriple(graphName, company, prop):
    query = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>       
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX foaf: <http://xmlns.com/foaf/spec/>
            PREFIX xsd: <http://www.w3.org/TR/swbp-xsch-datatypes/>
            PREFIX db-datatypes: <http://dbpedia.org/datatype/>       
            PREFIX user-modified-cisqa: <http://user-modified-dbpedia/>  

            DELETE {{GRAPH <{graphName}> {{?s ?p ?o}}}}
            WHERE  {{ ?s ?p ?o . 
                        FILTER (?s = {company} && ?p = {prop}) 
            }}
    """
    try:
        data = requests.get(SPARQL_ENDPOINT, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text
    except Exception as e:
        raise RuntimeError('Triple Store Triple Deletion Error')
    return data


def insertCard(graphName, cardData):
    separateNameEntities = ['foundedBy', 'foundationPlace', 'keyPerson']
    separateLabelEntities = ['industry', 'product', 'locationCity']
    optionalAttributes = ['assets', 'equity', 'revenue', 'netIncome', 'thumbnail']

    query = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>       
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX foaf: <http://xmlns.com/foaf/spec/>
            PREFIX xsd: <http://www.w3.org/TR/swbp-xsch-datatypes/>
            PREFIX db-datatypes: <http://dbpedia.org/datatype/>       
            PREFIX user-modified-cisqa: <http://user-modified-dbpedia/>       

            INSERT DATA
            {{
                GRAPH <{graphName}> {{
                    <{cardData['entity']}> rdfs:label "{cardData['title']}"@en ;
                    rdfs:label "{cardData['title']}"@de ;
                    rdf:type dbo:Company ;
                    dbo:abstract "{cardData['description']}"@de .
                }}
            }}
    """

    for entity in separateNameEntities:
        deleteTriple(graphName, "user-modified-cisqa:" + cardData['title'] + "_" + entity, "foaf:name")
        if entity in cardData:
            entityLink = [f"<{cardData['entity']}>", "dbo:" + entity, "user-modified-cisqa:" + cardData['title'] + "_" + entity, ""]
            entityTriple = ["user-modified-cisqa:" + cardData['title'] + "_" + entity, "foaf:name", f"\"{cardData[entity]}\"", "@de"]
            insertTriples(graphName, [entityLink, entityTriple])

    for entity in separateLabelEntities:
        deleteTriple(graphName, "user-modified-cisqa:" + cardData['title'] + "_" + entity, "rdfs:label")
        if entity in cardData:
            entityLink = [f"<{cardData['entity']}>", "dbo:" + entity, "user-modified-cisqa:" + cardData['title'] + "_" + entity, ""]
            entityTriple = ["user-modified-cisqa:" + cardData['title'] + "_" + entity, "rdfs:label", f"\"{cardData[entity]}\"", "@de"]
            insertTriples(graphName, [entityLink, entityTriple])

    for attribute in optionalAttributes:
        deleteTriple(graphName, f"<{cardData['entity']}>", "dbo:" + attribute)
        if attribute in cardData:
                if attribute == 'thumbnail':
                    insertTriple(graphName, f"<{cardData['entity']}>", "dbo:" + attribute, f"<{cardData[attribute]}>")
                else:
                    insertTriple(graphName, f"<{cardData['entity']}>", "dbo:" + attribute, f"\"{str(cardData[attribute])}\"", datatype="^^db-datatypes:euro")

    try:
        data = requests.get(SPARQL_ENDPOINT, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query})
        return data

    except Exception as e:
        raise RuntimeError('Triple Store Card Insertion Error')

