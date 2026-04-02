from nltk.parse import RecursiveDescentParser
from nltk import CFG
from nltk.stem import WordNetLemmatizer
import nltk

from .searchIndex import *
from .sim import *


import spacy
import de_core_news_md
nlp = de_core_news_md.load()

from nltk import Tree
import unittest

def get_head_NP(subtrees):
  heads = []
  for subtree in subtrees:
    #subtree.pretty_print()
    if type(subtree) == tuple:
      if subtree[1] == 'DET':
          if subtree[0] in ['viel', 'wenig', 'mehrer']:
            heads.append(subtree[0])
      if subtree[1] == 'ADJ':
          heads.append(subtree[0])
      if subtree[1] == 'NOUN':
          heads.append(subtree[0])
      if subtree[1] == 'NUM':
        heads.append(subtree[0])
    else:
      if get_head_NP(subtree):
        heads.extend(get_head_NP(subtree))
  return heads


# Covers VP -> ADV PP
# Disregards AP -> ADV ADJ
def get_head_V(subtrees):
  heads = []
  for subtree in subtrees:
    if type(subtree) == tuple:
      if subtree[1] == 'ADV':
        heads.append(subtree[0])
      if subtree[1] == 'VERB':
        verb = subtree[0]
        if subtree[0].endswith("en"):
          verb = verb[:-len("en")]
          verb = verb  + "ung"
        heads.append(verb.capitalize())
    else:
      if get_head_NP(subtree):
        heads.extend(get_head_NP(subtree))
  return heads


def get_heads(sent):
  grammar = """
PP: {<ADP><PROPN>}
PP: {<ADP><DET>?<ADJ>?<NOUN>}
PP: {<ADP><NUM><NOUN>}

AP: {<ADV><ADJ>}
AP: {<ADV><DET><ADJ>?<NOUN>}

NP: {<DET><NOUN><PP>}
NP: {<ADJ><NOUN>}
NP: {<PROPN><PP>}
NP: {<NOUN><PP>}
NP: {<DET><NOUN>}
NP: {<AP>}

VP: {<ADV><PP><VERB>}
VP: {<PP>?<PP><VERB>}
VP: {<VERB>}
"""
  doc = nlp(sent)
  tagged = [(token.lemma_, token.pos_) for token in doc]

  chunkParser = nltk.RegexpParser(grammar)

  heads = []

  for subtree in chunkParser.parse(tagged):
    #print(subtree)
    if type(subtree) == nltk.tree.Tree:
      #print(subtree)
      if subtree.label() == "NP":
        heads.extend(get_head_NP(subtree))
      if subtree.label() == "AP":
        heads.extend(get_head_NP(subtree))
      if subtree.label() == "VP":
        if doc[0].text.lower() in ["wo", "wer", "wann"]:
          heads.extend([doc[0].text.lower()])
        verb = get_head_V(subtree)
        heads = verb + heads
      if subtree.label() == "PP":
        heads.extend(get_head_NP(subtree))
  #print(sent)
  #print(heads)
  return heads


def get_rel(sent):
  heads = get_heads(sent)
  headPhrase = ' '.join(heads)
  print("sent: ", sent)
  print("heads: ", headPhrase)
  headVec, originalHead = generate_sentEmbeddings(headPhrase)

  relations = ontologySearch(headPhrase, headVec)
  #print(headPhrase, relations)

  relEmbeddings = []
  orig = []
  for i, rel in enumerate(relations):
    relEmbed, originalRel = generate_sentEmbeddings(rel[0])
    relEmbeddings.append(relEmbed)
    orig.append(rel)
  
  #candidates = high_sim(headPhrase, relEmbeddings, orig)
  print("CANDIDATES: ", relations)
  #relList = [(c[1][1], c[1][0]) for c in candidates if c[0][0] > 0.8]
  if relations[0][2] >= 9.9:
    relList = [(relations[0][1], relations[0][0].replace(' ', '_'))]
  else:
    relList = [ (c[1], c[0].replace(' ', '_')) for c in relations if c[2] > 0.02]
  print("RELLIST:", relList)
  return set(relList)


def sparql(sent):
  relURIs = get_rel(sent)

  variables = ""
  optional = ""
  for i, rel in enumerate(relURIs):
    variables = variables + "?" + str(i) + " "
    optional = optional + "OPTIONAL {?iri " + rel + " ?" + str(i) + "} " + "\n"

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

"""
print("Aktiva von Adidas?", sparql("Aktiva von Adidas?"))
print("Einkommen von Adidas?", sparql("Einkommen von Adidas?"))
print("Wann wurde Adidas gegründet?", sparql("Wann wurde Adidas gegründet?"))
print("In welchem Jahr wurde Adidas gegründet?", sparql("In welchem Jahr wurde Adidas gegründet?"))
print("Gründungsjahr von Adidas?", sparql("Gründungsjahr von Adidas?"))
print("Gründungsort von Adidas?", sparql("Gründungsort von Adidas?"))
print("Slogan von Adidas?", sparql("Slogan von Adidas?"))
print("Gründer von Adidas?", sparql("Gründer von Adidas?"))
print("Produkte von Adidas?", sparql("Produkte von Adidas?"))
print("Wie viele Mitarbeiter hat Adidas?", sparql("Wie viele Mitarbeiter hat Adidas?"))
print("Wo wurde Adidas gegründet?", sparql("Wo wurde Adidas gegründet?"))
print("Welche Kategorie gehört die Nachricht an?", sparql("Welche Kategorie gehört die Nachricht an?"))
"""


"""
class TestStringMethods(unittest.TestCase):
  def test_head(self):
        #s = 'Wer ist CEO von Adidas?'
        #self.assertEqual(get_heads(s), ['CEO'])
        s = 'Adidas'
        self.assertEqual(get_heads(s), [])
        s = 'Informationen zu Adidas'
        self.assertEqual(get_heads(s), ['Information'])
        s = 'Wo befindet sich Adidas?'
        self.assertEqual(get_heads(s), ['wo', 'befinden'])
        s = 'Wer sind die CEOs von Adidas?'
        self.assertEqual(get_heads(s), ['CEOs'])
        s = 'Wer war der Gründer von Adidas?'
        self.assertEqual(get_heads(s), ['Gründer'])
        s = 'Gründer von Adidas?'
        self.assertEqual(get_heads(s), ['Gründer'])
        s = 'CEOs von Adidas?'
        self.assertEqual(get_heads(s), ['CEOs'])
        s = 'In welchem Jahr wurde Adidas gegründet?'
        self.assertEqual(get_heads(s), ['Jahr', 'gründen'])
        s = 'Wie hoch ist das Eigenkapital von Adidas'
        self.assertEqual(get_heads(s), ['hoch', 'Eigenkapital'])
        s = 'Wie hoch sind die Einnahmen von Adidas'
        self.assertEqual(get_heads(s), ['hoch', 'Einnahme'])
        s = 'Wie hoch sind die Vermögenswerte von Adidas'
        self.assertEqual(get_heads(s), ['hoch', 'Vermögenswerte'])
        s = 'Wie hoch ist das Aktiva von Adidas'
        self.assertEqual(get_heads(s), ['hoch', 'Aktiva'])
        s = 'Wie niedrig ist das Eigenkapital von Adidas'
        self.assertEqual(get_heads(s), ['niedrig', 'Eigenkapital'])
        s = 'Wie niedrig sind die Einnahmen von Adidas'
        self.assertEqual(get_heads(s), ['niedrig', 'Einnahme'])
        s = 'Wie niedrig sind die Vermögenswerte von Adidas'
        self.assertEqual(get_heads(s), ['niedrig', 'Vermögenswerte'])
        s = 'Wie niedrig ist das Aktiva von Adidas'
        self.assertEqual(get_heads(s), ['niedrig', 'Aktiva'])
        s = 'Wie viele Mitarbeiter hat Adidas?'
        self.assertEqual(get_heads(s), ['viel', 'Mitarbeiter'])
        s = 'Was ist der Slogan von Adidas?'
        self.assertEqual(get_heads(s), ['Slogan'])
        s = 'Wie viele CEOs hat Adidas?'
        self.assertEqual(get_heads(s), ['viel', 'CEOs'])
        s = 'Welche Aktien sind im letzten Monat um 10% gestiegen?'
        self.assertEqual(get_heads(s), ['Aktie', 'letzt', 'Monat', '10', '%', 'steigen'])
        s = 'Welche Aktien sind in der letzten Woche um 10% gesunken?'
        self.assertEqual(get_heads(s), ['Aktie', 'letzt', 'Woche', '10', '%', 'sinken'])
        s = 'Welche Aktien sind gestern um 10% gesunken?'
        self.assertEqual(get_heads(s), ['Aktie', 'gestern', '10', '%', 'sinken',])
        s = 'Welche Aktien sind am 10.10.2020 um 10% gesunken?'
        self.assertEqual(get_heads(s), ['Aktie', '10.10.2020', '10', '%', 'sinken'])
        s = 'In welchen Unternehmen werden in letzter Zeit viele Stimmanteile gekauft?'
        self.assertEqual(get_heads(s), ['Unternehmen', 'letzt', 'Zeit', 'viel', 'Stimmanteile', 'kaufen'])
        s = 'In welcher Branche werden in letzter Zeit wenige Stimmanteile veräußert?'
        self.assertEqual(get_heads(s), ['Branche', 'letzt', 'Zeit', 'wenig', 'Stimmanteile', 'veräußern'])
        s = 'Welches Unternehmen erwirbt in letzter Zeit viele Stimmanteile?'
        self.assertEqual(get_heads(s), ['Unternehmen', 'erwerben', 'letzt', 'Zeit', 'viel', 'Stimmanteile']) 
        s = 'Wie verhält sich der Aktienkurs um die Bewegungen der Stimmanteile herum?'
        self.assertEqual(get_heads(s), ['verhalten', 'Aktienkurs', 'Bewegung', 'Stimmanteile'])
        s = 'Wie verhält sich der Aktienkurs um die DDs herum?'
        self.assertEqual(get_heads(s), ['verhalten', 'Aktienkurs', 'DDs'])
        s = 'Welche Personen haben viele DDs?'
        self.assertEqual(get_heads(s), ['Person', 'viel', 'DDs'])
        s = 'Welche Personen haben DDs in mehreren Unternehmen?'
        self.assertEqual(get_heads(s), ['Person', 'DDs', 'mehrer', 'Unternehmen'])
        s = 'Wie haben sich die DDs von Personen entwickelt?'
        self.assertEqual(get_heads(s), ['DDs', 'Person', 'entwickeln'])
        s = 'In welchen Unternehmen gibt es viele DDs?'
        self.assertEqual(get_heads(s), ['Unternehmen', 'geben', 'viel', 'DDs'])
        s = 'In welchen Branchen gibt es hohe DDs?'
        self.assertEqual(get_heads(s), ['Branche', 'geben', 'hoch', 'DDs'])
        s = 'In welchen Regionen gibt es niedrige DDs?'
        self.assertEqual(get_heads(s), ['Region', 'geben', 'niedrige', 'DDs'])
        s = 'In welchen Branchen gibt es viel DDs?'
        self.assertEqual(get_heads(s), ['Branche', 'geben', 'viel', 'DDs'])
        s = 'In welchen Regionen gibt es wenig DDs?'
        self.assertEqual(get_heads(s), ['Region', 'geben', 'wenig', 'DDs'])
        s = 'Wie viele CEOs hat Adidas?'
        self.assertEqual(get_heads(s), ['viel', 'CEOs'])
        s = 'Wann wurde Adidas gegründet?'
        self.assertEqual(get_heads(s), ['wann', 'gründen'])
        s = 'Wer gründete Adidas?'
        self.assertEqual(get_heads(s), ['wer', 'gründen'])

if __name__ == '__main__':
    unittest.main()
  
"""

