from flask import Flask, request, Response
from flask_restful import Resource, Api
from config.api_keys import KEYS
from config.essential import BOTS, SERVICES
from thread_with_return import ThreadWithReturnValue
import requests
import time
import json
import os

app = Flask(__name__)
api = Api(app)

def DoTheRequest(bot_url, service, params):
    response = requests.post('%s/%s' % (bot_url, service), json = {'params' : params}, timeout=120)
    return response.json()

class StartService(Resource):
    def get(self):
        return 'Para usar e autenticar fazer post request em / e passar x-api-key na header'
    def post(self):
        if 'x-api-key' in request.headers and request.headers['x-api-key'] in KEYS:
            if 'service' in request.json:
                try:
                    service = str(request.json['service']).lower()
                    bot_name = SERVICES[service]
                    bot_url = BOTS[bot_name]
                    if 'params' in request.json:
                        params = request.json['params']
                    else:
                        params = {}
                    def generate():
                        response = ThreadWithReturnValue(target=DoTheRequest, args=tuple([bot_url, service, params]))
                        response.start()
                        while response.is_alive():
                            time.sleep(2)
                            yield '' # ?? works ??
                        yield json.dumps(response.join())
                    return Response(generate(), content_type='application/json')
                except KeyError as exc:
                    print (exc)
                    return 'servico nao encontrado no bothub', 404
            else:
                return 'request fora do padrao', 400
        else:
            return 'x-api-key nao liberada para uso ou nao localizada nas headers', 401

api.add_resource(StartService, '/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5555))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
