import json

from flask import Blueprint, Response
from flask_restx import Namespace, Resource, fields

import config
from dtos.ErroDTO import ErroDTO
from dtos.UsuarioDTO import UsuarioBaseDTO
from utils import Decorators

usuario_controller = Blueprint('usuario_controller', __name__)

api = Namespace('Usuário')

user_field = api.model('UsuarioBaseDTO',
                       {
                           'name': fields.String,
                           'email': fields.String
                       })


@api.route('/', methods=['GET'])
class UsuariosController(Resource):

    @api.doc(responses={200: 'Login realizado com sucesso.', 400: 'Token inválido ou expirado.'})
    @api.response(200, 'success', user_field)
    @Decorators.token_required
    def get(self, usuario_atual):
        try:
            return Response(json.dumps(UsuarioBaseDTO('Admin', config.LOGIN_TEST).__dict__),
                            status=200, mimetype='application/json')
        except Exception as e:
            error = {"status": 500, "erro": e}
            print(error)
            return Response(json.dumps(ErroDTO("Não foi possível processar sua requisição, favor tente novamente", 500).__dict__),
                            status=500, mimetype="application/json")
