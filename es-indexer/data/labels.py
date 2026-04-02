from heads import *
import requests
import json

import spacy
import de_core_news_lg
nlp = de_core_news_lg.load()

from deep_translator import GoogleTranslator



## This function gets a word and returns a list of synonyms
## \param term string word
def get_synonyms(term):
    try:
        d = json.loads(requests.get("http://www.openthesaurus.de/synonyme/search",
                                params={"q": term, "format": "application/json"}).text)
    except Exception as e:
            return []

    if d["synsets"]:
        return [o["term"] for o in d["synsets"][0]["terms"]]
    else:
        return []



DBQUERY = """
select distinct ?prop ?label where {
  ?company a <http://dbpedia.org/ontology/Company> .
  ?company ?prop ?y.
  ?prop rdfs:label ?label
FILTER(LANG(?label) = "en" || LANGMATCHES(LANG(?label), "en"))
}
        """



def dbPedia(query):

        url = 'https://dbpedia.org/sparql'

        try:
            data = json.loads(requests.post(url, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text)['results']['bindings']
          
        except Exception as e:
            raise RuntimeError('dbPedia Request Error' + requests.post(url, headers = {'User-Agent': '9833ghg376nd824k'}, params = {'format': 'json', 'query': query}).text)
        return data


outF = open("dbo.json", "w")
for x in dbPedia(DBQUERY):
  word = GoogleTranslator(source='auto', target='de').translate(x['label']['value'])
  print(x['label']['value'])
  print(word)
  outF.write('{"_source":{"uri":"' + x['prop']['value'] + '","label":"' + word + '"}}')
  outF.write("\n")
  synonyms = get_synonyms(word)
  if synonyms:
    for syn in synonyms:
      outF.write('{"_source":{"uri":"' + x['prop']['value'] + '","label":"' + syn + '"}}')
      outF.write("\n")
      print('S: ' + syn)
outF.close()