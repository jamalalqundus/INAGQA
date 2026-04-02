#******************************************************************************#
#* Name:     performQuery.py                                                  *#
#* Author:   lvu                                                              *#
#*                                                                            *#
#* Description:                                                               *#
#*  Transforms the query results of nlp-backend into the proper frontend      *#
#*  format and sets the data flag (map, card, table).                         *#
#*                                                                            *#
#*                                                                            *#
#******************************************************************************#

import json
import requests
import connexion

def value(news, key):
    if key in news:
        return news[key]["value"]
    else:
        return "N/A"

def performQuery(query):
    ### Forwarding Error Message
    if type(query)!=list:
        return query, 500

    if query[0] == "C-card":
        if "propertyCount" in query[1]:
            del query[1]["propertyCount"]

    jsonFile = {}
    ############## MAP ##############
    if query[0] == "C-map":
        jsonFile = {"flag": "map", "query": query[4],"content": [{"lat": query[1],"locationlabel": query[2],"long": query[3]}]}
        print(jsonFile)
    ############## TABLE ##############
    ### NVR Nachrichten zu Adidas
    elif query[0] == "NVR-table":
        jsonFile = {"flag": "table", "query": query[2], "content":{"headers": [{"label": "Datum", "type": "date"}, {"label": "Nachricht", "type": "literal"}, {"label": "Kapitalmaßnahme", "type": "literal"}, {"label": "Gesamtstimmrechte", "type": "literal"}, {"label": "Gültigkeitsdatum", "type": "literal"},  {"label": "iri", "type": "url"}, {"label": "Autor", "type": "literal"}, {"label": "Sprache", "type": "literal"}], "rows": []}}
        for news in query[1]:
            jsonFile["content"].get('rows').append([value(news,"date"), value(news,"title"), value(news,"capitalMeasure"), value(news,"votingRights"), value(news,"effDate"), {"label": "Link zur iri", "href":news["iri"]["value"]}, value(news,"author"), value(news,"language") ])
            print("json: ", jsonFile)
    elif query[0] == "C-table":
        rows = []
        ### Nachrichten zu Adidas
        if type(query[1]) == list:
            jsonFile = {"flag": "table", "query": query[2], "content": {"headers": [{"label": "Datum", "type": "date"}, {"label": "Nachricht", "type": "literal"}, {"label": "Weblink", "type": "url"}], "rows": []}}
            for news in query[1]:
                news[2] = { "label": "Link zur Nachricht", "href": news[2]}
                jsonFile["content"].get('rows').append(news)
        ### Wie viele Nachrichten gibt es zu Adidas?
        else:
            jsonFile = {"flag": "table", "query": query[2], "content": {"headers": [{"label": "Nachrichten Anzahl","type": "literal"}], "rows": [[query[1]]]}}
    ############## CARD ##############
    elif query[0] == "C-card":
        for prop in query:
            jsonFile = {"flag": "card", "query": query[2], "properties": []}

            for key in query[1]:
                if key in ["thumbnail", "entity", "title"]:
                    json = {key: query[1][key]['value']}
                    jsonFile.update(json)
                elif query[1][key]['value']:
                    jsonHead = {"property": str(key.encode('latin-1').decode('utf-8'))}
                    # Convert Numbers and Currency to the right format
                    if key in ["assets","equity","revenue","netIncome"]:
                        query[1][key]['value'] = float(query[1][key]['value'])
                    jsonProp = query[1][key]
                    merged = {**jsonHead, **jsonProp}
                    jsonFile["properties"].append(merged)
    #elif query[0] == "C-graph":
        #jsonFile = {"flag": "graph", "content": {"roots": [{"type": "literal","value": "Johnny Depp"}], "knots": [{"type": "literal","value": "Autobiografie"}]}}
    elif query[0] == "Bar-chart":
        data = []
        categories = []
        for element in query[1]:
            #print(value(element,"date"))
            #value(element,"umsatz_currency")
            #value(element,"Metrik")
            #value(element,"Jahr")
            categories.append(value(element,"lbl"))
            data.append({"y":value(element,"umsatz_amount")})
        jsonFile = {"flag": "chart", "query": query[2], "properties": [{"datatype":"barchart", "categories":categories, "series":[{"title":"Umsatz Vergleich","data":data}] }]}
    elif query[0] == "Stock-chart":
        data = []
        title = ""
        for element in query[1]:
            if "umsatz_amount" in element:
                title = "Umsatz Vergleich"
                data.append([value(element,"date"),value(element,"umsatz_amount")])
            if "news_count" in element:
                title = "Nachrichten Anzahl"
                data.append([value(element,"news_date"),value(element,"news_count")])
        jsonFile = {"flag": "chart", "query": query[2], "properties": [{"datatype":"stock", "series":[{"title":title,"data":data}] }]}
    print(jsonFile)
    return jsonFile