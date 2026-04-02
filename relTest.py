## Start elasticsearch Docker and relation-api Docker
## Then run this code for testing


import requests
import json


def create_query2(entity, relation):
	print(relation)
	print(relation["URIs"])
	variables = ""
	optional = ""
	for i, rel in enumerate(relation["URIs"]):
		variables = variables + "?" + str(i) + "_" + rel[1] + " "
		optional = optional + "OPTIONAL {?iri <" + rel [0]+ "> ?" + str(i) + "_" + rel[1] + "} " + "\n"
	return """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp:  <http://dbpedia.org/property/>
      SELECT DISTINCT
        """ + variables + """

      WHERE {
        ?iri a dbo:Company ;
             rdfs:label ?lbl .
       FILTER (str(?lbl)='Adidas')

        """ + optional + """
      }
          """


response = requests.post("http://localhost:4545/api/get_relation", json={'question': "Gründungsjahr von Adidas?"}, headers={'content-type': "application/json"}).json()

print(create_query2("Adidas", response))

## print(requests.post("http://nlp.api.annotator.demo.qurator.apps.osc.fokus.fraunhofer.de/sent", json={'text':"Gründungsjahr von Adidas?", 'model':'de_core_news_md'}).json())


## Start elasticsearch Docker and relation-api Docker
## Then run this code for testing
'''

import requests
import json


query =  """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp:  <http://dbpedia.org/property/>
      SELECT DISTINCT
        ?0_Gründungsjahr ?1_Gründungsdatum ?2_Gründungsort ?3_Gründungsjahr 

      WHERE {
        ?iri a dbo:Company ;
             rdfs:label ?lbl .
       FILTER (str(?lbl)='Adidas')

        OPTIONAL {?iri <http://dbpedia.org/ontology/formationYear> ?0_Gründungsjahr} 
OPTIONAL {?iri <http://dbpedia.org/ontology/foundingDate> ?1_Gründungsdatum} 
OPTIONAL {?iri <http://dbpedia.org/ontology/foundationPlace> ?2_Gründungsort} 
OPTIONAL {?iri <http://dbpedia.org/ontology/foundingYear> ?3_Gründungsjahr} 

      }
          """


response1 = json.loads(requests.get("http://localhost:8090/cisqa20-api4kb-backend-0.1.0/api/sparql/", params = {'query': query, "entities":['Adidas']}).text)['results']['bindings']
response2 = json.loads(requests.get('http://api4kb.eco-qa.demo.quartor.apps.osc.fokus.fraunhofer.de/cisqa20-api4kb-backend-0.1.0/api/sparql', params = {'query': query, "entities":['Adidas']}).text)['results']['bindings']


print(response1)
#print(response2)

'''
