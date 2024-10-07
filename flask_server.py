from datetime import datetime
import json
from os import getenv

from flask import Flask, request

app = Flask(__name__)
CALLBACK_URL_PORT = getenv("CALLBACK_URL_PORT", 8000)


@app.route('/', methods=['GET'])
def callback():
    code = request.args.get('code')
    today_date = datetime.now().strftime("%Y-%m-%d")

    if code is None:
        return 'Codice non trovato!'

    with open(f'{today_date}.json', 'a') as f:
        json_string = json.dumps({'code': code})
        f.write(json_string)

    return 'Codice memorizzato! Attendi la chiusura del browser...'


def run_server():
    app.run(host='0.0.0.0', port=CALLBACK_URL_PORT)
