# MQTT set up
docker pull eclipse-mosquitto                                 

docker run -it --name mosquitto -p 1883:1883 eclipse-mosquitto

docker start/stop mosquitto

# start
subscriber (paho_mqtt_client_sub.py) runs for ever!
publisher (paho_mqtt_client_sub.py) run once and publishs events

subscriber takes reaktion on an event (empty-answer) and ask wikidata for further information, which is then transformed into a json as a suggestion.  

