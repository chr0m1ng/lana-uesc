
from flask import Flask, request
from flask_restful import Resource, Api
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))
from bot_uesc import Bot

app = Flask(__name__)
api = Api(app)

class UESC(Resource):
    def post(self):
        bot_uesc = Bot()
        return bot_uesc.UESC()

class UESC_Listar_Cursos(Resource):
    def post(self):
        bot_sagres = Bot()
        return bot_sagres.UESC_Listar_Cursos()

class UESC_Listar_Departamentos(Resource):
    def post(self):
        bot_sagres = Bot()
        return bot_sagres.UESC_Listar_Departamentos()

class UESC_Listar_Editais(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'date' in params:    
                bot_sagres = Bot()
                return bot_sagres.UESC_Listar_Editais(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class UESC_Listar_Editais_Recentes(Resource):
    def post(self):
        bot_sagres = Bot()
        return bot_sagres.UESC_Listar_Editais_Recentes()

class UESC_Listar_Editaisbens(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'date' in params:    
                bot_sagres = Bot()
                return bot_sagres.UESC_Listar_Editaisbens(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class UESC_Listar_Editaisbens_Recentes(Resource):
    def post(self):
        bot_sagres = Bot()
        return bot_sagres.UESC_Listar_Editaisbens_Recentes()

class UESC_Listar_Noticias(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'date' in params:    
                bot_sagres = Bot()
                return bot_sagres.UESC_Listar_Noticias(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class UESC_Listar_Noticias_Recentes(Resource):
    def post(self):
        bot_sagres = Bot()
        return bot_sagres.UESC_Listar_Noticias_Recentes()

class UESC_Listar_Resultados(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'date' in params:    
                bot_sagres = Bot()
                return bot_sagres.UESC_Listar_Resultados(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class UESC_Listar_Resultados_Recentes(Resource):
    def post(self):
        bot_sagres = Bot()
        return bot_sagres.UESC_Listar_Resultados_Recentes()
        
api.add_resource(UESC, '/uesc')
api.add_resource(UESC_Listar_Cursos, '/uesc_listar_cursos')
api.add_resource(UESC_Listar_Departamentos, '/uesc_listar_departamentos')
api.add_resource(UESC_Listar_Editais, '/uesc_listar_editais')
api.add_resource(UESC_Listar_Editais_Recentes, '/uesc_listar_editais_recentes')
api.add_resource(UESC_Listar_Editaisbens, '/uesc_listar_editaisbens')
api.add_resource(UESC_Listar_Editaisbens_Recentes, '/uesc_listar_editaisbens_recentes')
api.add_resource(UESC_Listar_Noticias, '/uesc_listar_noticias')
api.add_resource(UESC_Listar_Noticias_Recentes, '/uesc_listar_noticias_recentes')
api.add_resource(UESC_Listar_Resultados, '/uesc_listar_resultados')
api.add_resource(UESC_Listar_Resultados_Recentes, '/uesc_listar_resultados_recentes')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5060))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
