from elasticsearch import Elasticsearch
import json
from multiprocessing.pool import ThreadPool
from elasticsearch import helpers


import pickle


from sentence_transformers import SentenceTransformer, util, models
#from torch import nn
import re

#w_model = models.Transformer("../../relation-api/data/model/GBERT", max_seq_length=512)
#pooling_model = models.Pooling(w_model.get_word_embedding_dimension())
#dense_model = models.Dense(in_features=pooling_model.get_sentence_embedding_dimension(), out_features=512, activation_function=nn.Tanh())
model = SentenceTransformer("../../relation-api/data/model/GBERT")

def generate_sentEmbeddings(text):
  origSent = re.sub(r'\(.*?\)', '', text)
  sentEmbeddings = model.encode(origSent, convert_to_tensor=True)
  return sentEmbeddings, origSent


### SAVE TO FILE
with open('dbo.json',encoding="utf8") as f:
    requests = []
    for line in f:
        lineObject=json.loads(line, strict=False)
        labelEmbed, originalLabel = generate_sentEmbeddings(lineObject["_source"]["label"])
        #print(labelEmbed.shape)
        requests.append({'_index':"dbontologyindex", "uri":lineObject["_source"]["uri"], "label":lineObject["_source"]["label"], "vec":labelEmbed.tolist()})
    #print(requests)
    pickle.dump(requests, open( "dbo.p", "wb" ) )


### LOAD TO ES
# by default we connect to localhost:9200
es = Elasticsearch(['http://localhost:9201'])

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


requests = pickle.load( open( "dbo.p", "rb" ))
helpers.bulk(es, requests)
print("ok")
