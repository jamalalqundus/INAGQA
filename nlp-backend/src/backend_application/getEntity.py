#******************************************************************************#
#* Name:     getEntity.py                                                     *#
#*                                                                            *#
#* Description:                                                               *#
#*  Queries DBpedia for autosuggestion entities.                              *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#

import requests
import json
from flask import jsonify

proxies = {}


def getEntity(searchString):
    url = 'https://dbpedia.org/sparql'
    query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>       
            SELECT DISTINCT
            ?iri
            (str(?lbl) as ?Titel)
                (COUNT(?property) as ?propertyCount)
            WHERE {
              ?iri a dbo:Company ;
                   rdfs:label ?lbl .
                          FILTER strStarts(lCase(?lbl), lCase(""" + "'" + searchString + "'" + """))
                          FILTER( langMatches(lang(?lbl),"de") )
              
              OPTIONAL {
                VALUES ?p { dbo:assets dbo:equity foaf:depiction dbo:thumbnail dbo:foundationPlace dbo:keyPerson dbo:revenue dbo:netIncome dbo:industry dbo:product dbo:location}
                ?iri ?p ?property .
              }
             
            }
            ORDER BY DESC (?propertyCount)
            LIMIT 5
        """

        #""" + "'" + company + "'" + """
    try:
        data = json.loads(requests.post(url, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text)['results']['bindings']
            
    except Exception as e:
        raise RuntimeError('dbPedia Request Error' + requests.post(url, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text)
    zs = []
    for entity in data:
        zs.append({"entity": entity["iri"]["value"], "label": entity["Titel"]["value"]})
    return zs

'''
    print(searchString)
    req = requests.get(
        'https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&search=' + searchString + '&language=de')
    if(not req.json().get("error", False)):
        zs = []
        for i in req.json()["search"]:
            zs.append({"entity": i["title"], "label": i["label"]})
        print(zs)
        return zs
    else:
        return "Wikidata Error", 500
'''

if __name__ == "__main__":
    getEntity("abc")
