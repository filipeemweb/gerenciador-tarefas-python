import json

from flask import Blueprint, Response, request
from flask_restx import Namespace, Resource, fields

from dtos.ErroDTO import ErroDTO
from dtos.UsuarioDTO import UsuarioBaseDTO, UsuarioCreateDTO
from services.UsuarioService import UsuarioService
from utils import Decorators

usuario_controller = Blueprint('usuario_controller', __name__)

api = Namespace('Usuário')

user_field = api.model('UsuarioBaseDTO',
                       {
                           'name': fields.String,
                           'email': fields.String
                       })


@api.route('', methods=['GET', 'POST'])
class UsuariosController(Resource):

    @api.doc(responses={200: 'Login realizado com sucesso.', 400: 'Token inválido ou expirado.'})
    @api.response(200, 'success', user_field)
    @Decorators.token_required
    def get(usuario):
        try:
            return Response(json.dumps(UsuarioBaseDTO(usuario.nome, usuario.email).__dict__),
                            status=200, mimetype='application/json')
        except Exception as e:
            error = {"status": 500, "erro": e}
            print(error)
            return Response(json.dumps(ErroDTO(500, "Não foi possível processar sua requisição, favor tente novamente").__dict__),
                            status=500, mimetype="application/json")

    def post(self):
        try:
            body = request.get_json()

            erros = []

            if not body:
                return Response(json.dumps(ErroDTO(400, 'Body da requisição não pode ser vazio').__dict__),
                                status=400, mimetype="application/json")

            if 'nome' not in body:
                erros.append("Campo 'nome' é obrigatório.")

            if 'email' not in body:
                erros.append("Campo 'email' é obrigatório.")

            if 'senha' not in body:
                erros.append("Campo 'senha' é obrigatório.")

            if erros:
                return Response(json.dumps(ErroDTO(400, erros).__dict__),
                                status=400, mimetype="application/json")

            usuario_criado = UsuarioService().criar_usuario(body['nome'], body['email'], body['senha'])

            if not usuario_criado:
                return Response(json.dumps(ErroDTO(400, 'E-mail já cadastrado no sistema.').__dict__),
                                status=400, mimetype="application/json")

            return Response(
                json.dumps(UsuarioCreateDTO(usuario_criado.id, usuario_criado.nome, usuario_criado.email, usuario_criado.senha).__dict__),
                status=201, mimetype='application/json'
            )
        except Exception as e:
            error = {"status": 500, "erro": e}
            print(error)
            return Response(
                json.dumps(ErroDTO(500, "Não foi possível processar sua requisição, favor tente novamente").__dict__),
                status=500, mimetype="application/json")
