from datetime import datetime


def validar_data(data, formato_data='%Y-%m-%d'):
    try:
        data = datetime.strptime(data, formato_data)

        return data
    except Exception as e:
        print('Erro ao fazer validação de data: ', e)
        return None
