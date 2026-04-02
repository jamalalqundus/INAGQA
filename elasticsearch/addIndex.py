"""


@author: Sakor
"""
from elasticsearch import Elasticsearch
import json
from multiprocessing.pool import ThreadPool
###from sim import *
from elasticsearch import helpers

import pickle

import os, sys
print(os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0])

# by default we connect to localhost:9200
es = Elasticsearch(['http://localhost:9200'])


create_query = {
    "mappings": {
        "properties": {
            "uri": {
                "type": "text"
            },
            "label": {
                "type": "text"
            },
            "vec": {
                "type": "dense_vector",
                "dims": 1024
            }
        }
    }
}

es.indices.create(index="dbontologyindex", body=create_query)


"""
### SAVE TO FILE
with open('./data/dbo2.json',encoding="utf8") as f:
    requests = []
    for line in f:
        lineObject=json.loads(line, strict=False)
        labelEmbed, originalLabel = generate_sentEmbeddings(lineObject["_source"]["label"])
        requests.append({'_index':"dbontologyindex", "uri":lineObject["_source"]["uri"], "label":lineObject["_source"]["label"], "vec":labelEmbed[0].tolist()})
    print(requests)
    pickle.dump(requests, open( "dbo.p", "wb" ) )
"""


requests = pickle.load( open( "/usr/elasticsearch/data/dbo.p", "rb" ))
helpers.bulk(es, requests)

