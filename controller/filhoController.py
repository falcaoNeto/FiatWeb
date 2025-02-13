from entity.filho import Filho

class FilhoController:
    def Cadastrar(self, dado, id_cliente):
        
        try:
            Filho.Insert(dado, id_cliente)
        except Exception as e:
            print(e)


    def DeletarFilho(self, id_filho):
        try:
            Filho.Delete(id_filho)
        except Exception as e:
            print(e)

    def GetFilho(self, id_filho):
        try:
            filho = Filho.Select_for_update(id_filho)
            filho_dic = {}
            
            filho_dic["id_filho"] = filho[0]
            filho_dic["nome_filho"] = filho[1]
            filho_dic["dNasc"] = filho[2]

                

            print(filho_dic)
            print("=-=-=-=-=-=-=-=-=-==-=-=")


            return filho_dic
        except Exception as e:
            print(e)

    def AtualizarFilho(self, id_filho, dado):
        try:
            filho_dic = {"id_filho": id_filho, "nome": dado["nome"], "data_nascimento": dado["dataN"]}
            Filho.Update(filho_dic)
        except Exception as e:
            print(e)