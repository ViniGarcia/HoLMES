import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/click_plugin/running', methods=['GET'])
def running():
    return "/click_plugin/running - OK"

@app.route('/click_plugin/metrics', methods=['GET'])
def metrics():
	return "/click_plugin/metrics - OK"

@app.route('/response', methods=['POST'])
def response():
    return "/response - OK"

app.run()