from entity.carro import Carro
import json

class CarroController:

    def cadastrar(self, respnse_form):
        try:
            modelo = respnse_form.get("modelo")
            contadorCampos = 1
            id_carro = Carro.cadastrarCarro(modelo)
            while True:
                titulo = respnse_form.get(f"titulo{contadorCampos}")
                campo = respnse_form.get(f"campo{contadorCampos}")
                if not campo:
                    break
                id_carroDado = Carro.cadastrarCarroDados({"titulo": titulo, "texto": campo}, id_carro)
                Carro.cadastrarCarroPinecone({"modelo": modelo, "titulo": titulo, "texto": campo}, id_carroDado)
                print(id_carroDado)
                contadorCampos += 1
            
            return "Carro cadastrado com sucesso!"
        except Exception as e:
            return f"Erro ao cadastrar o carro: {str(e)}"
        
    def CadastrarDado(self, id, modelo,  respnse_form):
        try:
            titulo = respnse_form.get("titulo")
            texto = respnse_form.get("texto")

            carro = {
                "titulo": titulo,
                "texto": texto
            }

            Carro.cadastrarCarroDados(carro, id)
            Carro.cadastrarCarroPinecone({"modelo": modelo, "titulo": titulo, "texto": texto}, id)
            return "Carro cadastrado com sucesso!"
        except Exception as e:
            return f"Erro ao cadastrar o carro unico Controller: {str(e)}"


        

    def ListarCarros(self):
        try:
            # No seu código Python, agrupe os detalhes por carro:
            carros = Carro.Listar()
            carros_agrupados = {}
            for row in carros:
                id_carro = row[0]
                if id_carro not in carros_agrupados:
                    carros_agrupados[id_carro] = {
                        "id_carro": row[0],
                        "modelo": row[1],
                        "dados": []
                    }
                carros_agrupados[id_carro]["dados"].append({
                    "id_carroDados": row[2],
                    "titulo": row[4],
                    "texto": row[5]
                })

            # Converta para lista para o template
            Carros = list(carros_agrupados.values())
            return True, "", Carros
        except Exception as e:
            return False, f"Erro ao listar carros: {str(e)}", None
        

    def DeletarCarro(self, id_carro):
        try:
            Carro.Deletar(id_carro)
            # Carro.DeletarPinecone(id_carro)
            return "Carro deletado com sucesso!"
        except Exception as e:
            return f"Erro ao deletar o carro: {str(e)}"
        

    def DeletarDado(self, id_carro):
        try:
            Carro.DeletarDados(id_carro)
            # Carro.DeletarPinecone(id_carro)
            return "Carro deletado com sucesso!"
        except Exception as e:
            return f"Erro ao deletar o carro: {str(e)}"
        
    def VisualizarCarroDados(self, id_carroDados):
        try:
            carroDados = Carro.GetCarroDados(id_carroDados)
            
            dado = {"id_carroDados" : carroDados[0][0], "titulo" : carroDados[0][2], "texto" : carroDados[0][3]}
            return dado
        except Exception as e:
            return f"Erro ao encontrar o carro: {str(e)}"
        
    def AtualizarCarros(self, id, respnse_form):
        try:
            titulo = respnse_form.get("titulo")
            texto = respnse_form.get("texto")

            carro = {
                "id_dado": id,
                "titulo": titulo,
                "texto": texto
            }
            Carro.Atualizar(carro)

            return "Carro atualizado com sucesso!"
        except Exception as e:
            return f"Erro ao atualizar o carro: {str(e)}"


if __name__ == "__main__":
    carro = CarroController()
    carroD = carro.VisualizarCarroDados(10)

    print(carroD)