import json
from datetime import datetime

from flask import Blueprint, Response, request
from flask_restx import Namespace, Resource

from dtos.ErroDTO import ErroDTO
from dtos.SucessoDTO import SucessoDTO
from services.TarefaService import TarefaService
from utils import Decorators
from utils.Validacao import validar_data

tarefa_controller = Blueprint('tarefa_controller', __name__)

api = Namespace('Tarefa')


@api.route('', methods=['POST', 'GET'])
@api.route('/<idTarefa>', methods=['DELETE', 'PUT'])
class TarefaController(Resource):

    @Decorators.token_required
    def post(usuario, controller):
        try:
            body = request.get_json()

            erros = []

            if not body:
                return Response(json.dumps(ErroDTO(400, 'Body da requisição não pode ser vazio').__dict__),
                                status=400, mimetype="application/json")

            if 'nome' not in body:
                erros.append("Campo 'nome' é obrigatório.")

            if 'dataPrevisaoConclusao' not in body:
                erros.append("Campo 'dataPrevisaoConclusao' é obrigatório.")
            elif not validar_data(body['dataPrevisaoConclusao']):
                erros.append("Campo 'dataPrevisaoConclusao' inválido, formato deve ser 'yyyy-mm-dd'.")
            elif validar_data(body['dataPrevisaoConclusao']) < datetime.now():
                erros.append('Data de previsão não pode ser menor que hoje.')

            if erros:
                return Response(json.dumps(ErroDTO(400, erros).__dict__),
                                status=400, mimetype="application/json")

            tarefa_criada = TarefaService().criar_tarefa(body['nome'], body['dataPrevisaoConclusao'], None, usuario.id)

            return Response(json.dumps(tarefa_criada.to_dict()),
                            status=201, mimetype='application/json')

        except Exception as e:
            error = {"status": 500, "erro": e}
            print(error)
            return Response(
                json.dumps(ErroDTO(500, "Não foi possível criar a tarefa, favor tente novamente").__dict__),
                status=500, mimetype="application/json")

    @Decorators.token_required
    def delete(usuario, controller, idTarefa):
        try:
            if not TarefaService().filter_by_id(idTarefa):
                return Response(
                    json.dumps(ErroDTO(400, "Tarefa não encontrada").__dict__),
                    status=400, mimetype="application/json")

            tarefa_deletada = TarefaService().deletar_tarefa(usuario.id, idTarefa)

            if not tarefa_deletada:
                return Response(
                    json.dumps(ErroDTO(401, "Não foi possível deletar a tarefa, favor tente novamente").__dict__),
                    status=401, mimetype="application/json")

            return Response(
                json.dumps(SucessoDTO(200, "Tarefa deletada com sucesso").__dict__),
                status=200, mimetype="application/json")

        except Exception as e:
            error = {"status": 500, "erro": e}
            print(error)
            return Response(
                json.dumps(ErroDTO(500, "Não foi possível excluir a tarefa, favor tente novamente").__dict__),
                status=500, mimetype="application/json")

    @Decorators.token_required
    def put(usuario, controller, idTarefa):
        try:
            if not TarefaService().filter_by_id(idTarefa):
                return Response(
                    json.dumps(ErroDTO(400, "Tarefa não encontrada").__dict__),
                    status=400, mimetype="application/json")

            body = request.get_json()

            erros = []

            if not body:
                return Response(json.dumps(ErroDTO(400, 'Body da requisição não pode ser vazio').__dict__),
                                status=400, mimetype="application/json")

            if 'nome' not in body and 'dataPrevisaoConclusao' not in body and 'dataConclusao' not in body:
                erros.append('Favor enviar os dados que deseja atualizar.')

            if 'dataConclusao' in body and not validar_data(body['dataConclusao']):
                erros.append("Campo 'dataConclusao' inválido, formato deve ser 'yyyy-mm-dd'.")

            if 'dataPrevisaoConclusao' in body and not validar_data(body['dataPrevisaoConclusao']):
                erros.append("Campo 'dataPrevisaoConclusao' inválido, formato deve ser 'yyyy-mm-dd'.")

            if erros:
                return Response(json.dumps(ErroDTO(400, erros).__dict__),
                                status=400, mimetype='application/json')

            tarefa_encontrada = TarefaService().filter_by_id(idTarefa)

            if 'nome' in body:
                tarefa_encontrada.nome = body['nome']

            if 'dataConclusao' in body:
                tarefa_encontrada.dataConclusao = body['dataConclusao']

            if 'dataPrevisaoConclusao' in body:
                tarefa_encontrada.dataPrevisaoConclusao = body['dataPrevisaoConclusao']

            tarefa_atualizada = TarefaService().atualizar_tarefa(usuario.id, tarefa_encontrada)

            if not tarefa_atualizada:
                return Response(
                    json.dumps(ErroDTO(401, "Não foi possível atualizar a tarefa, favor tente novamente").__dict__),
                    status=401, mimetype="application/json")

            return Response(
                json.dumps(SucessoDTO(200, "Tarefa atualizada com sucesso").__dict__),
                status=200, mimetype="application/json")

        except Exception as e:
            error = {"status": 500, "erro": e}
            print(error)
            return Response(
                json.dumps(ErroDTO(500, "Não foi possível atualizar a tarefa, favor tente novamente").__dict__),
                status=500, mimetype="application/json")

    @Decorators.token_required
    def get(usuario, controller):
        try:
            erros = []

            allowed_status = ['0', '1', '2']

            if 'periodoDe' in request.args and not validar_data(request.args.get('periodoDe')):
                erros.append("Campo 'periodoDe' inválido, formato deve ser 'yyyy-mm-dd'.")

            if 'periodoAte' in request.args and not validar_data(request.args.get('periodoAte')):
                erros.append("Campo 'periodoAte' inválido, formato deve ser 'yyyy-mm-dd'.")

            if 'status' in request.args and request.args.get('status') not in allowed_status:
                erros.append("Campo 'status' com opção inválida. Favor informar um status 0, 1 ou 2")

            if erros:
                return Response(json.dumps(ErroDTO(400, erros).__dict__),
                                status=400, mimetype='application/json')

            periodoDe = request.args.get('periodoDe')
            periodoAte = request.args.get('periodoAte')
            status = request.args.get('status') if request.args.get('status') else '0'

            tarefas = TarefaService().filter(usuario.id, periodoDe, periodoAte, status)

            return Response(
                json.dumps([ob.to_dict() for ob in tarefas]),
                status=200, mimetype="application/json")

        except Exception as e:
            error = {"status": 500, "erro": e}
            print(error)
            return Response(
                json.dumps(ErroDTO(500, "Não foi possível listar as tarefas, favor tente novamente").__dict__),
                status=500, mimetype="application/json")

