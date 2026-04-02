# INAGQA

INAGQA is a semantic question-answering system for German financial queries. It combines syntactic chunking with knowledge graph embeddings to handle linguistic variability, achieving:

0.91 F1 on 2,100 expert-annotated German financial questions
35% fewer relation-linking errors for compound nouns (e.g., "Eigenkapitalrendite")
2.1s average response time in real-world analyst use
98% accuracy on temporal vs. quantitative variants (e.g., "When" vs. "Where")
Outperforms BERT-KGQA (0.83 F1) and template-based systems (0.79 F1). Designed for SMEs and aligned with Corporate Smart Insights frameworks.

### Workflow Diagram:
![](cisqa-workflow2.svg " Workflow Diagram")


# Get started

<details>
  <summary markdown="span">if working locally with vs-code IDE (click me)</summary>

1. Install [vs-code](https://code.visualstudio.com/)
1. Click on Extension symbol on the left side
1. Search "Remote-SSH" and install version v0.49.0
1. Click on the green bottom left corner "Open a Remote Window"
1. Choose "Connect to Host" in drop down menu, which pops up.
</details>


#### Pulling
```
git clone https://github.com/jamalalqundus/INAGQA.git
git submodule update --init --recursive
```

#### Building

sample dataset are availabe in th project.placed in 
```
es-indexer/data
```
and checked in
```
elasticsearch/data
```
however, extended dataset can be requested by the authors.

##### to use: 
docker deamon running

to start (build images and start container):
```
docker compose up --build
```
to stop running container
```
docker compose down
```

# Currently used Ports:

frontend
- Port from outside http://localhost:2003/
- Port for docker inside communication [frontend:8080](frontend:8080)

![](documentation/container-flow.png)

# ocumentation
Code Documentation\
doc > vXXXXXXXX > index.html

Graph\
doc > Graph.pdf

Component Map\
doc > Modul.pdf

# Version History

##### V3
- semantic-api and nlp merge 

###### V2Embed
- New: relation-api
- Uses word embeddings to find relation URI (label will be compared with head word using elasticsearch)
- Builds SPARQL query with returned URIs

###### GITHUB
- SPARQL template with #HEAD-WORD comment
- if head-word then #HEAD-WORD comment will be removed
- Example: "#CEOS ?keyPerson" turns to "?keyPerson"

- Stock Business Data Q&A
- Triple Store Backend
- http://localhost:5001/api/query?query=aktuelle%20Nachrichten%20zu%20Adidas


# cite the paper
tbd