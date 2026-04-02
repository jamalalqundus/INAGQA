import requests


def check_get_endpoint(url):
    assert requests.get(url).status_code == 200

def check_post_endpoint(url):
    assert requests.post(url, json={'question': "Gründungsjahr von Adidas?"}, headers={'content-type': "application/json"}).status_code == 200
    return requests.post(url, json={'question': "Gründungsjahr von Adidas?"}, headers={'content-type': "application/json"}).json()


def test_api4kb_available():
    check_get_endpoint('http://api4kb.eco-qa.demo.quartor.apps.osc.fokus.fraunhofer.de/cisqa20-api4kb-backend-0.1.0/swagger-ui.html')

def test_elasticsearch_available():
    check_get_endpoint('http://eco-qa-elasticsearch:9200/')

def test_frontend_available():
    check_get_endpoint('http://eco-qa-frontend:8080/')




def test_nlp_available():
    check_get_endpoint('http://eco-qa-nlp-api:8070/api/query?query=Adidas?&generatorMode=false')
    json = requests.get('http://eco-qa-nlp-api:8070/api/query?query=Adidas?&generatorMode=false').json()
    assert json["entity"] == "http://dbpedia.org/resource/Adidas"

def test_relation_api_available():
    json = check_post_endpoint('http://eco-qa-relation-api:4545/api/get_relation')
    assert json["URIs"][0] == ['http://dbpedia.org/ontology/foundingYear', 'Gründungsjahr']

"""

def test_api4kb_available():
    check_get_endpoint('http://api4kb.eco-qa.demo.quartor.apps.osc.fokus.fraunhofer.de/cisqa20-api4kb-backend-0.1.0/swagger-ui.html')

def test_elasticsearch_available():
    check_get_endpoint('http://172.17.0.1:9201/')

def test_frontend_available():
    check_get_endpoint('http://172.17.0.1:2003/')




def test_nlp_available():
    check_get_endpoint('http://172.17.0.1:8070/api/query?query=Adidas?&generatorMode=false')
    json = requests.get('http://172.17.0.1:8070/api/query?query=Adidas?&generatorMode=false').json()
    assert json["entity"] == "http://dbpedia.org/resource/Adidas"

def test_relation_api_available():
    json = check_post_endpoint('http://172.17.0.1:4545/api/get_relation')
    assert json["URIs"][0] == ['http://dbpedia.org/ontology/foundingYear', 'Gründungsjahr']

"""
"""

def test_api4kb_available():
    check_get_endpoint('http://api4kb.eco-qa.demo.quartor.apps.osc.fokus.fraunhofer.de/cisqa20-api4kb-backend-0.1.0/swagger-ui.html')
                        
def test_frontend_available():
    check_get_endpoint('http://eco-qa.demo.quartor.apps.osc.fokus.fraunhofer.de')


def test_nlp_available():
    check_get_endpoint('http://eco-qa.demo.quartor.apps.osc.fokus.fraunhofer.de/api/query?query=Adidas?&generatorMode=false')
    json = requests.get('http://eco-qa.demo.quartor.apps.osc.fokus.fraunhofer.de/api/query?query=Adidas?&generatorMode=false').json()
    assert json["entity"] == "http://dbpedia.org/resource/Adidas"
"""