from database.database import SessionLocal
from models.Tarefa import Tarefa

db = SessionLocal()


class TarefaService:
    def __init__(self):
        pass

    def filter(self, idUsuario, periodo_de, periodo_ate, status):
        tarefas = db.query(Tarefa).filter(Tarefa.idUsuario == idUsuario)

        if status == '1':
            tarefas = tarefas.filter(Tarefa.dataConclusao is None)

        if status == '2':
            tarefas = tarefas.filter(Tarefa.dataConclusao.isnot(None))

        if periodo_de:
            tarefas = tarefas.filter(Tarefa.dataPrevisaoConclusao >= periodo_de)

        if periodo_ate:
            tarefas = tarefas.filter(Tarefa.dataPrevisaoConclusao <= periodo_ate)

        return tarefas.all()

    def filter_by_id(self, id):
        return db.query(Tarefa).filter(Tarefa.id == id).first()

    def criar_tarefa(self, nome, data_previsao_conclusao, data_conclusao, id_usuario):

        nova_tarefa = Tarefa(
            nome=nome,
            dataPrevisaoConclusao=data_previsao_conclusao,
            dataConclusao=data_conclusao,
            idUsuario=id_usuario
        )

        db.add(nova_tarefa)
        db.commit()

        return nova_tarefa

    def deletar_tarefa(self, id_usuario, id):
        tarefa_encontrada = self.filter_by_id(id)

        if not tarefa_encontrada.idUsuario == id_usuario:
            return None

        db.query(Tarefa).filter(Tarefa.id == id).delete()
        db.commit()

        return True

    def atualizar_tarefa(self, id_usuario, tarefa):
        tarefa_encontrada = self.filter_by_id(tarefa.id)

        if not tarefa_encontrada.idUsuario == id_usuario:
            return None

        db.commit()

        return True