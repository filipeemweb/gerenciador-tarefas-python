import random
import string
import db_config as db

API_HOST = '127.0.0.1'
API_PORT = 5000
API_BASE_URL = '/api'

LOGIN_TEST = 'admin@admin.com'
SENHA_TEST = 'Admin1234@'

# Gera uma chave aleatória para geração do JWT
gen = string.ascii_letters + string.digits + string.ascii_uppercase
SECRET_KEY = ''.join(random.choice(gen) for i in range(32))

# Configuração MySQL
MYSQL_HOST = db.LOCAL_MYSQL_HOST
MYSQL_PORT = db.LOCAL_MYSQL_PORT
MYSQL_USER = db.LOCAL_MYSQL_USER
MYSQL_PASSWORD = db.LOCAL_MYSQL_PASSWORD

MYSQL_DATABASE = 'gerenciador_tarefas'

DEBUG = True
