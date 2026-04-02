#******************************************************************************#
#* Name:     fromCSV.py                                                       *#
#*                                                                            *#
#* Description:                                                               *#
#* 	A question is analyzed. It is either answered from the local CSV or       *#
#*	API4KB is queried.                                                        *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#

import pandas as pd
import paho.mqtt.client as mqtt
import os
import re

import spacy
import de_core_news_lg
nlp = de_core_news_lg.load()

import uuid
import pickle

from .virtuoso import *
from .heads import *

from spacy.pipeline import EntityRuler
from  geopy.geocoders import Nominatim
from datetime import datetime

DATE = datetime.today().strftime('%Y-%m-%d')

import logging
logging.basicConfig(filename='../log/logger.log', level=logging.INFO, format='%(asctime)s; %(message)s')

SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT', "http://virtuoso:8890/sparql/")
RELATION_ENDPOINT = os.getenv('RELATION_ENDPOINT')


### Adding Companies to Spacy Entity Ruler
comp = pickle.load( open( "../data/comps_de.p", "rb" ) )

 
comp.remove('Nachrichten')
patterns = []
for company in comp:
  words = company.split()
  p = []
  for ii, word in enumerate(words):
    #if ii == 0:
      p.append({"LOWER": word.lower()})
    #else:
      #{"LOWER": word.lower(), "OP": "?"}
      #p.append({"LOWER": word.lower(), "OP": "?"})
  patterns.append({"label": "ORG", "pattern": p, "id": company})


ruler = EntityRuler(nlp)
ruler.add_patterns(patterns)
nlp.add_pipe(ruler, before='ner')

def create_query(function, company = "", day = ""):
	filepath = "../data/queries/" + function
	with open(filepath, "r") as f:
		sparql = f.read()
	# Replace the placeholders in the SPARQL template
	sparql = sparql % {'comp':company, 'date':day}
	return sparql



def create_query2(entity, relation):
	print(relation["URIs"])
	variables = ""
	optional = ""
	for i, rel in enumerate(relation["URIs"]):
		variables = variables + "?" + str(i) + "_" + rel[1] + "\n"
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
			  ?lbl bif:contains " """ + "'" + entity + "'" +  """ "@en  .
			  FILTER( langMatches(lang(?lbl),"de") )

        """ + optional + """
      }
          """


def on_log(client, userdata, level, buf):
	print("publisher log: ",buf)

def api4kb(query, entity=None):
        try:
            data = json.loads(requests.get(SPARQL_ENDPOINT, params = {'query': query, "entities":[entity]}).text)['results']['bindings']
        except Exception as e:
            raise RuntimeError('API4KB Request Error' + requests.get(SPARQL_ENDPOINT, params = {'query': query}).text + str(e))
        return data

def get_rel(question):
	response = requests.post(RELATION_ENDPOINT, json={'question': question}, headers={'content-type': "application/json"}).json()

	return response


def answerFromAPI4KB(question, clientID, questionID, questionOrig, correctedQuery):
	logging.info(questionID + ' --------------------------------------------')
	logStr = questionID + "; request:" + questionOrig + "; spellcheck:" + correctedQuery + "; response:{}; entity:{}; cookie_clientID:" + clientID

	doc = nlp(question)

	# Umsatz Prognose all companies -> entity not relevant in query "Umsatz Prognose für das Jahr 2020"
	# das Jahr as entity in spacy
	if 'umsatz prognose' in question.lower():
		try:
			year = str(re.findall(r'[0-9]+',question)[0])
			query = create_query("prognose-year", day = year)
			print(query)
			s = api4kb(query, None)
			logging.info(logStr.format('api4kb(csv): C-chart ' + str(s), "No Entity"))
			return ['Bar-chart', s, correctedQuery]
		except Exception as e:
			logging.info(logStr.format('CSV: C-chart []', "No Entity"))
			raise IndexError('Entity not found in api4kb(csv)'  + str(e))


	entity = doc.ents[0].text
	entityLabel = doc.ents[0].label_

	# Check for too many entities
	if len(doc.ents) > 1:
		logging.error(logStr.format(' ERROR: More than one Entity found - ' +  str(doc.ents), entityLabel))
		raise IndexError('More than one Entity found: ' +  str(doc.ents))

	
	if len(doc.ents) > 0:
		# Address of the company
		if 'wo befindet' in question.lower() or 'adresse' in question.lower():
			try:
				# Check virtuoso
				query = selectTriple('CompanyKB', entity, 'address')
				if query:
					s = query[0]['search']['value']
				else:
				# Check Api4kb
					query = create_query("location", company = entity)
					result = api4kb(query, entity)[0]
					s = result['Strasse']['value'] +  ", " + result['Land']['value']
				geolocator = Nominatim(user_agent='9833ghg376nd824k')
				loc = geolocator.geocode(s, timeout=60)
				logging.info(logStr.format('api4kb(csv): C-map ' + str(loc.latitude) + str(loc) + str(loc.longitude), entityLabel))
				return ['C-map', loc.latitude, str(loc), loc.longitude, correctedQuery]
			except Exception as e:
				logging.info(logStr.format('api4kb(csv): C-table []', entityLabel))
				raise IndexError('Entity not found in api4kb(csv)'  + str(e))
		# Umsatz from company
		elif 'umsatz' in question.lower():
			try:
				query = create_query("umsatz", company = entity)
				s = api4kb(query, entity)
				logging.info(logStr.format('api4kb(csv): C-chart ' + str(s), entityLabel))
				return ['Stock-chart', s, correctedQuery]
			except Exception as e:
				logging.info(logStr.format('CSV: C-chart []', entityLabel))
				raise IndexError('Entity not found in api4kb(csv)'  + str(e))

		# How many current news about the company (day)
		elif 'wie viele aktuelle nachrichten' in question.lower():
			try:
				query = create_query("news-count-today", company = entity, day = DATE)
				s = api4kb(query, entity)[0]['news_count']['value']
				logging.info(logStr.format('api4kb(csv): C-table ' + str(s), entityLabel))
				return ['C-table', str(s), correctedQuery]
			except Exception as e:
				logging.info(logStr.format('CSV: C-table []', entityLabel))
				raise IndexError('Entity not found in api4kb(csv)'  + str(e))

		# How many news about the company all in all
		elif 'wie viele nachrichten' in question.lower():
			try:
				query = create_query("news-count", company = entity)
				s = api4kb(query, entity)
				logging.info(logStr.format('api4kb(csv): C-table ' + str(s), entityLabel))
				return ['Stock-chart', s, correctedQuery]
			except Exception as e:
				logging.info(logStr.format('api4kb(csv): C-table []', entityLabel))
				raise IndexError('Entity not found in api4kb(csv)'  + str(e))

		# Current news about the company
		elif 'aktuelle nachrichten' in question.lower():
			try:
				query = create_query("news-today", company = entity, day = DATE)
				result = api4kb(query, entity)
				s = []
				for news in result:
					s.append([news['Datum_News']['value'], news['News_Header']['value'], news['URL']['value']])
				logging.info(logStr.format('api4kb(csv): C-table' + str(s), entityLabel))
				return ['C-table', s, correctedQuery]
			except Exception as e:
				logging.info(logStr.format('api4kb(csv): C-table []', entityLabel))
				raise IndexError('Entity not found in api4kb(csv)'  + str(e))
		# All NVR news about the company
		elif 'nvr-nachrichten' in question.lower():
			try:
				query = create_query("news-NVR", company = entity)
				s = api4kb(query, entity)
				print(s)
				#s = []
				#for news in result:
					#s.append([news['title']['value'], news['lastModified']['value'], news['author']['value'], news['capitalMeasure']['value'], news['votingRights']['value']])
				logging.info(logStr.format('api4kb(csv): NVR-table ' + str(s), entityLabel))
				return ['NVR-table', s, correctedQuery]
			except Exception as e:
				logging.info(logStr.format('api4kb(csv): NVR-table []' + query, entityLabel))
				raise IndexError('Entity not found in api4kb(csv)'  + str(e))
		# All news about the company
		elif 'nachrichten' in question.lower():
			try:
				query = create_query("news", company = entity)
				result = api4kb(query, entity)
				s = []
				for news in result:
					s.append([news['Datum_News']['value'], news['News_Header']['value'], news['URL']['value']])
				logging.info(logStr.format('api4kb(csv): C-table ' + str(s), entityLabel))
				return ['C-table', s, correctedQuery]
			except Exception as e:
				logging.info(logStr.format('api4kb(csv): C-table []' + query, entityLabel))
				raise IndexError('Entity not found in api4kb(csv)'  + str(e))
		elif get_heads(question):
			try:
				relation = get_rel(question)
				query = create_query2(entity, relation)
				print(query)
				result = api4kb(query, entity)[0]
				print(result, entity, api4kb(query, entity))
				logging.info(logStr.format('api4kb(dbpedia): C-card ' + str(result), entityLabel))
				return ['C-card', result, correctedQuery]
			except Exception as e:
				logging.info(logStr.format('api4kb(dbpedia): C-Card []', entityLabel))
				raise IndexError('Entity not found in api4kb(dbpedia)'  + str(e))
					

	# Info about the company
		############################
		# Example mqtt entity not found message
		############################
		client = mqtt.Client()
		client.connect(os.environ["MQTT_BROKER"], port=int(os.environ["MQTT_PORT"]), keepalive=int(os.environ["MQTT_KEEPALIVE"]), bind_address="")
		client.on_log=on_log
		client.publish(os.environ["MQTT_NO_DATA"], entity)
		client.disconnect()
		############################
		# Check API4KB
		############################
		try:
			query = create_query("card", company = entity)
			result = api4kb(query, entity)[0]
			logging.info(logStr.format('api4kb(dbpedia): C-card' + str(result), entityLabel))
			return ['C-card', result, correctedQuery]
		except Exception as e:
			logging.info(logStr.format('CSV: C-Card []', entityLabel))
			raise IndexError('Entity not found in api4kb(dbpedia)' + str(e))
