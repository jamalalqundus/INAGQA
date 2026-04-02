Aktuell mögliche Klassen: map, table, card

## map: 
mehrere Orte möglich, mehrere Marker auf einer card

```
{
    "flag": "map", 
    "content": [
        {
            "locationlabel": "ExampleLocation",
            "lat": "456",
            "long": "123"
        }
    ]
}
```

## table:

```
{
    "flag": "table", 
    "content": {
        "headers": [ {"label": "Datum", "type": "date"}, {"label": "Nachricht", "type": "literal"}, {"label": "Weblink", "type": "url"} ], 
        "rows": rows
    }
}
```

rows: 
```
[
    [
        1596647687,
        "adidas AG: Release according to Article 40, Section 1 of the WpHG [the German Securities Trading Act] with the objective of Europe-wide distribution - dgap.de",
        {
            "label": "Link zur Nachricht",
            "href": "https://www.dgap.de/dgap/News/pvr/adidas-release-according-article-section-the-wphg-the-german-securities-trading-act-with-the-objective-europewide-distribution/?newsID=1356885"
        }
    ]
]
```

## card:

```
{
    "flag": "card", 
    "title": "ExampleTitle", 
    "entity": "Entity_UUID",
    "image": "url/to/image",
    "properties": properties
}
```

properties:
```
[
    {
        "property": "Bezeichnung", 
        "type": "literal", 
        "value": "Adidas", 
    }
]
```

### Todo:
Graph, Heatmap, Line-plot, Histogramm



# Modify result

## Specification:

```PUT /api/query?query=X```

Modify or add the result for a specific query.
Payload equals the classes defined in ./InterfaceDocs.md


## Example:

```GET /api/query?query=Daimler```

```
{
  "entity": "http://dbpedia.org/resource/Daimler-Benz",
  "flag": "card",
  "image": "http://commons.wikimedia.org/wiki/Special:FilePath/Znaczek_Mercedesa.jpg",
  "properties": [
    {
      "property": "Beschreibung",
      "type": "literal",
      "value": "Die Daimler-Benz Aktiengesellschaft war ein Vorg\u00e4ngerunternehmen der heutigen Daimler AG. Daimler-Benz entstand 1926 durch die Fusion der Daimler-Motoren-Gesellschaft mit der Benz & Cie. Im Jahr 1998 fusionierten die Daimler-Benz AG und die amerikanische Chrysler Corporation zur neu gegr\u00fcndeten DaimlerChrysler AG, die seit 2007, nach dem mehrheitlichen Verkauf von Chrysler, nunmehr als Daimler AG firmiert. Die Vorl\u00e4ufer der Daimler-Benz AG, die Daimler-Motoren-Gesellschaft sowie Benz und Cie., gelten als \u00e4lteste Kraftfahrzeug-Unternehmen der Welt."
    },
    {
      "property": "Branche",
      "type": "literal",
      "value": "Automobilindustrie,Milit\u00e4r"
    },
    {
      "property": "CEO",
      "type": "literal",
      "value": "Carl Benz,Gottlieb Daimler,Karl Benz"
    },
    {
      "property": "Ort",
      "type": "literal",
      "value": "Stuttgart"
    },
    {
      "property": "Produkt",
      "type": "literal",
      "value": "Kraftfahrzeug,Verbrennungsmotor"
    }
  ],
  "title": "Daimler-Benz"
}
```

```PUT /api/query?query=Daimler```

Modified "Beschreibung", removed "CEO", added "Jahresumsatz".
```
{
  "entity": "http://dbpedia.org/resource/Daimler-Benz",
  "flag": "card",
  "image": "http://commons.wikimedia.org/wiki/Special:FilePath/Znaczek_Mercedesa.jpg",
  "properties": [
    {
      "property": "Beschreibung",
      "type": "literal",
      "value": "This is a modified text."
    },
    {
      "property": "Branche",
      "type": "literal",
      "value": "Automobilindustrie,Milit\u00e4r"
    },
    {
      "property": "Jahresumsatz",
      "type": "literal",
      "value": "11590000000.0"
    },
    {
      "property": "Ort",
      "type": "literal",
      "value": "Stuttgart"
    },
    {
      "property": "Produkt",
      "type": "literal",
      "value": "Kraftfahrzeug,Verbrennungsmotor"
    }
  ],
  "title": "Daimler-Benz"
}
```

## TODO
Create validation Agent in order to validate user input and annotate properties in api4kb way:

User input:
```
{
    "property": "Jahresumsatz",
    "type": "literal",
    "value": "11590000000.0"
}
```
Validation output:
```
{
    "datatype": "http://dbpedia.org/datatype/euro",
    "property": "Jahresumsatz",
    "type": "typed-literal",
    "value": 11590000000.0
}
```

# 3rd. party suggestions (mainly wikidata)

## Specification:

```/suggestAnswer```

Server-sent events (https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
for keeping a message stream between frontend and backend. 
Backend will notify frontend when there are new suggestions available.
Renaming the question suggestions endpoint (```/suggest```) (inspiring the user which questions to ask) into ```/suggestQuestion```.

## Example:

mandatory fields:

```["query"]```
```
[
    {
        "query":"Informationen über INAGQA",
        "properties":[
            {
                "property": "Unternehmensname", 
                "type": "literal", 
                "value": "Fraunhofer Institute for Open Communication Systems", 
            },
            {
                "property": "Wikidata url", 
                "type": "url", 
                "value": "https://www.wikidata.org/wiki/Q1452018", 
            },
            {
                "property": "Unternehmensauftritt", 
                "type": "url", 
                "value": "https://www.fokus.fraunhofer.de/en", 
            }
        ]
    },
    {
        "query":"Informationen über Siemens",
        "properties":[
            {
                "property": "Name der Ressource", 
                "type": "literal", 
                "value": "Siemens AG Annual Report 2016", 
            },
            {
                "property": "Wikidata url", 
                "type": "url", 
                "value": "https://www.wikidata.org/wiki/Q29533487", 
            },
            {
                "property": "Beschreibung", 
                "type": "literal", 
                "value": "annual report of Siemens AG", 
            }
        ]
    }
]
```

# still to come
- Validation agent
- Specification for rating properties and query results.
- question classifications should offer insights which result class (table, card, map) should be presented to the user when the user wants to add information to an empty response.
