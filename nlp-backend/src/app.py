import connexion
from flask_cors import CORS

app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yaml')

### for debugging - see Dockerfile -u CMD
CORS(app.app, supports_credentials=True)
app.run(port=8070)