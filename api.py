from flask import Flask
from flask_cors import CORS
from resources.globalDefs import GlobalDefs

app = Flask(__name__)
GlobalDefs(app, None)
CORS(app)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.76', port=5000)