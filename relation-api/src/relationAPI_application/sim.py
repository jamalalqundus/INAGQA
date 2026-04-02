#******************************************************************************#
#* Name:     sim.py                                                           *#
#*                                                                            *#
#* Description:                                                               *#
#*  Calculate the similarity between input and target phrases.                *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#
from sentence_transformers import SentenceTransformer, util, models
#from torch import nn
import re
from sklearn.manifold import TSNE

#w_model = models.Transformer("../data/model/GBERT", max_seq_length=512)
#pooling_model = models.Pooling(w_model.get_word_embedding_dimension())
#dense_model = models.Dense(in_features=pooling_model.get_sentence_embedding_dimension(), out_features=512, activation_function=nn.Tanh())
model = SentenceTransformer("../data/model/GBERT")

def generate_sentEmbeddings(text):
  origSent = re.sub(r'\(.*?\)', '', text)
  sentEmbeddings = model.encode(origSent, convert_to_tensor=True)
  return sentEmbeddings, origSent

def high_sim(headphrase, relEmbeddings, rel):
  vec1 = model.encode(headphrase, convert_to_tensor=True)
  rankList = []
  for num, vec2 in enumerate(relEmbeddings):
    if vec1.any() and vec2[0].any():
      cosine_scores = util.pytorch_cos_sim(vec1, vec2)
      rankList.append([cosine_scores, rel[num]])
  rankList.sort(reverse= True, key=lambda tup: tup[0])
  return rankList


"""
import spacy
import gensim
from gensim.models import Word2Vec
from nltk.corpus import stopwords
import re
import numpy as np

import de_core_news_md
nlp = de_core_news_md.load()
print("Start loading model")
#model = gensim.models.KeyedVectors.load_word2vec_format('../data/model/german.model.trained', binary=True)

model = gensim.models.Word2Vec.load('../data/model/deepset.100.bin.trained') #is deepset.100.bin saved so it loads faster
print("Finished loading model")

def sent_vec(sent, model):
  vec = np.zeros(shape=(model.vector_size,))

  for num, word in enumerate(sent):
    if word not in ["STOP"]:
      vec = vec + model[word]
  vec / (num+1)
  return vec


def high_sim(sent, relEmbeddings, origSent): 
  doc = nlp(sent) 
  formattedSent = [token.lemma_ for token in doc]
  vec1 = sent_vec(formattedSent, model)
  #print(formattedSent)
  rankList = []
  for num, vec2 in enumerate(relEmbeddings):
    if vec1.any() and vec2[0].any():
      cos = np.dot(vec1, vec2[0].T)/(np.linalg.norm(vec1)*np.linalg.norm(vec2[0]))
      rankList.append([cos, origSent[num]])
  rankList.sort(reverse= True, key=lambda tup: tup[0])
  return rankList


def generate_sentEmbeddings(text):
  # Convert the Text to the right format
  text = re.sub(r'\(.*?\)', '', text)
  sentEmbeddings = []
  origSent = []
  doc = nlp(text)

  for sent in doc.sents:
    sentList = [token.lemma_ for token in sent]
    sentEmbeddings.append(sent_vec(sentList, model))
    origSent.append(sent.text)
  return sentEmbeddings, origSent

"""