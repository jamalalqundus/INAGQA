import connexion

app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yaml')
app.run(port=4545)