#https://stackoverflow.com/questions/14299006/how-to-access-google-search-right-hand-side-data-programmatically
#https://yago-knowledge.org/sparql/query
#https://rdflib.dev/sparqlwrapper/

import paho.mqtt.client as mqtt #import the client1
import time
import json
import urllib
import requests
from bs4 import BeautifulSoup
from qwikidata.sparql  import return_sparql_query_results
from config import settings

data_set_json=[]

def request_wikidata(params):
    return requests.get(settings['API_ENDPOINT_WIKIDATA'], params=params).json()

def ask_wikidata_ts(entity):
    query = entity.replace('_',' ')
    
    #clear json otherwise suggestions of older quesions will be collected
    data_set_json.clear()
    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'en',
        'search': query
    }

    r = request_wikidata(params = params)
    #print(r)
    data_set={}
    for item in r['search']:        
        try:
            params_company ={
                'action':'wbgetentities',
                'format':'json',
                'sites':'enwiki',
                'props':'claims',
                'titles':item['label']
            }
            company_json = request_wikidata(params=params_company)
            company_url=company_json['entities'][item['id']]['claims']['P856'][0]['mainsnak']['datavalue']['value']
            data_set["query"]=entity
            data_set["properties"]=[
                {"property":"Unternehmensname","type":"literal", "value":item['label']},
                {"property":"Wikidata url","type":"url", "value":item['url']},
                {"property":"Unternemensauftritt","type":"url", "value":company_url}]
            data_set_json.append(data_set)
        except:
            print("no url to official page found")
                    
    print(data_set_json)
    client.publish(settings['ANSWER_MESSAGE'], json.dumps(data_set_json))
############### subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe(settings['NO_DATA_MESSAGE'])

def on_message(client, userdata, msg):
  if msg.payload.decode() !='':
    print("Yes!", str(msg.payload.decode()), ' was received')
    ask_wikidata_ts(str(msg.payload.decode()))

def on_log(client, userdata, level, buf):
    print("subscriber log: ",buf)


############ start client-subscriber
#client = mqtt.Client(transport="websockets") and changing port from ssl tcp to ssl websocket.
client = mqtt.Client()
time.sleep(20)

client.connect(settings['BROKER_ADDRESS'], port=settings['PORT'], keepalive=settings['KEEPALIVE'], bind_address="")

client.on_log=on_log
client.on_connect = on_connect
client.on_message = on_message


client.loop_forever()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        break
print("disconnect client")
