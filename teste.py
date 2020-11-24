import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/click_plugin/running', methods=['GET'])
def home():
    return "oi"

@app.route('/response', methods=['POST'])
def home2():
    return "ola"

app.run()