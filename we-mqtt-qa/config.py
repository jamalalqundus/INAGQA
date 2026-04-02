import os

settings = dict(
    BROKER_ADDRESS = os.getenv('BROKER_ADDRESS', "mosquitto"),
    PORT = int(os.getenv('PORT', "1883")),
    KEEPALIVE = int(os.getenv('KEEPALIVE', "60")),
    NO_DATA_MESSAGE = os.getenv('NO_DATA_MESSAGE', "topic/entityNotFound"),
    ANSWER_MESSAGE = os.getenv('ANSWER_MESSAGE', "topic/suggestAnswer"),
    API_ENDPOINT_WIKIDATA = os.getenv('API_ENDPOINT_WIKIDATA', "https://www.wikidata.org/w/api.php"),
)