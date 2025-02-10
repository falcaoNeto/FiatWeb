from entity.filho import Filho

class FilhoController:
    def Cadastrar(self, dado, id_cliente):
        
        try:
            Filho.cadastrar(dado, id_cliente)
        except Exception as e:
            print(e)


    def DeletarFilho(self, id_filho):
        try:
            Filho.Deletar(id_filho)
        except Exception as e:
            print(e)