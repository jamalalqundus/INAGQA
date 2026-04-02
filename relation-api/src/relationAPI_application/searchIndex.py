from elasticsearch import Elasticsearch


import os

# by default we connect to localhost:9200
ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')

es = Elasticsearch([ELASTICSEARCH_URL])

docType = "doc"

        
def ontologySearch(query, query_vec):
    indexName = "dbontologyindex"
    results=[]
    
    ###################################################
    search_query = {
        "size": 10,
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "1 / (1 + l1norm(params.query_vec, 'vec'))",
                    "params": {
                        "query_vec": query_vec.tolist()
                    }
                }
            }
        }
    }

    elasticResults=es.search(index=indexName, body=search_query)
    for result in elasticResults['hits']['hits']:
        if result["_source"]["uri"].lower()=="http://dbpedia.org/ontology/"+query.replace(" ", "_").lower():
            results.append([result["_source"]["label"],result["_source"]["uri"],result["_score"]*10,40])
        else:
            results.append([result["_source"]["label"],result["_source"]["uri"],result["_score"]*10,0])
    return results

def ontologySearch3(query, query_vec):
    indexName = "dbontologyindex"
    results=[]
    
    ###################################################
    search_query = {
        "size": 10,
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "1 / (1 + l2norm(params.query_vec, 'vec'))",
                    "params": {
                        "query_vec": query_vec.tolist()
                    }
                }
            }
        }
    }

    elasticResults=es.search(index=indexName, body=search_query)
    for result in elasticResults['hits']['hits']:
        if result["_source"]["uri"].lower()=="http://dbpedia.org/ontology/"+query.replace(" ", "_").lower():
            results.append([result["_source"]["label"],result["_source"]["uri"],result["_score"]])
        else:
            results.append([result["_source"]["label"],result["_source"]["uri"],result["_score"]])
    return results


def ontologySearch4(query, query_vec):
    indexName = "dbontologyindex"
    results=[]
    
    ###################################################
    search_query = {
        "size": 10,
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "doc['vec'].size() == 0 ? 0 : cosineSimilarity(params.query_vec, 'vec') + 1.0",
                    "params": {
                        "query_vec": query_vec.tolist()
                    }
                }
            }
        }
    }

    elasticResults=es.search(index=indexName, body=search_query)
    for result in elasticResults['hits']['hits']:
        if result["_source"]["uri"].lower()=="http://dbpedia.org/ontology/"+query.replace(" ", "_").lower():
            results.append([result["_source"]["label"],result["_source"]["uri"],result["_score"]*10,40])
        else:
            results.append([result["_source"]["label"],result["_source"]["uri"],result["_score"]*10,0])
    return results
    #for result in results['hits']['hits']:
        #print (result["_score"])
        #print (result["_source"])
        #print("-----------")
     
