
from flask import Flask, request
from flask_restful import Resource, Api
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers/config'))
from bot_sagres import Bot

app = Flask(__name__)
api = Api(app)

class Sagres(Resource):
    def post(self):
        bot_sagres = Bot()
        return bot_sagres.Sagres()

class Sagres_Calcular_CRAA(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'sagres_username' in params and 'sagres_password' in params:
                bot_sagres = Bot()
                return bot_sagres.Sagres_Calcular_CRAA(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class Sagres_Horarios_Corrente(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'sagres_username' in params and 'sagres_password' in params:
                bot_sagres = Bot()
                return bot_sagres.Sagres_Horarios_Corrente(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class Sagres_Listar_Disciplinas(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'sagres_username' in params and 'sagres_password' in params:
                bot_sagres = Bot()
                return bot_sagres.Sagres_Listar_Disciplinas(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class Sagres_Listar_Disciplinas_Corrente(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'sagres_username' in params and 'sagres_password' in params:
                bot_sagres = Bot()
                return bot_sagres.Sagres_Listar_Disciplinas_Corrente(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class Sagres_Listar_Faltas(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'sagres_username' in params and 'sagres_password' in params:
                bot_sagres = Bot()
                return bot_sagres.Sagres_Listar_Faltas(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class Sagres_Listar_Faltas_Disciplina(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'sagres_username' in params and 'sagres_password' in params and 'codigo_disciplina' in params:
                bot_sagres = Bot()
                return bot_sagres.Sagres_Listar_Faltas_Disciplina(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class Sagres_Listar_Notas(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'sagres_username' in params and 'sagres_password' in params:
                bot_sagres = Bot()
                return bot_sagres.Sagres_Listar_Notas(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class Sagres_Listar_Notas_Disciplina(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'sagres_username' in params and 'sagres_password' in params and 'codigo_disciplina' in params:
                bot_sagres = Bot()
                return bot_sagres.Sagres_Listar_Notas_Disciplina(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

class Sagres_Listar_Turmas_Corrente(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'sagres_username' in params and 'sagres_password' in params:
                bot_sagres = Bot()
                return bot_sagres.Sagres_Listar_Turmas_Corrente(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400
        
class Sagres_Listar_Alunos_Turma(Resource):
    def post(self):
        if 'params' in request.json:
            params = request.json['params']
            if 'sagres_username' in params and 'sagres_password' in params and 'codigo_disciplina' in params:
                bot_sagres = Bot()
                return bot_sagres.Sagres_Listar_Alunos_Turma(params)
            else:
                return 'request fora do padrao', 400
        else:
            return 'request fora do padrao', 400

# class Sagres_Listar_Quantidade_Turmas(Resource):
#     def post(self):
#         if 'params' in request.json:
#             params = request.json['params']
#             if 'sagres_username' in params and 'sagres_password' in params:
#                 bot_sagres = Bot()
#                 return bot_sagres.Sagres_Listar_Turmas_Corrente(params)
#             else:
#                 return 'request fora do padrao', 400
#         else:
#             return 'request fora do padrao', 400

api.add_resource(Sagres, '/sagres')
api.add_resource(Sagres_Calcular_CRAA, '/sagres_calcular_craa')
api.add_resource(Sagres_Horarios_Corrente, '/sagres_horarios_corrente')
api.add_resource(Sagres_Listar_Disciplinas, '/sagres_listar_disciplinas')
api.add_resource(Sagres_Listar_Disciplinas_Corrente, '/sagres_listar_disciplinas_corrente')
api.add_resource(Sagres_Listar_Faltas, '/sagres_listar_faltas')
api.add_resource(Sagres_Listar_Faltas_Disciplina, '/sagres_listar_faltas_disciplina')
api.add_resource(Sagres_Listar_Notas, '/sagres_listar_notas')
api.add_resource(Sagres_Listar_Notas_Disciplina, '/sagres_listar_notas_disciplina')
api.add_resource(Sagres_Listar_Turmas_Corrente, '/sagres_listar_turmas_corrente')
api.add_resource(Sagres_Listar_Alunos_Turma, '/sagres_listar_alunos_turma')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
