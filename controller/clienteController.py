from entity.cliente import Cliente
from controller.filhoController import FilhoController
from utils import format_telefone
from flask import session
from datetime import datetime


class ClienteController:
    def Cadastrar(self, response_form, id_funcionario):
        data = {
            'cpf': response_form.get('cpf'),
            'nome': response_form.get('nome'),
            'data_nascimento': response_form.get('dataN'),
            'data_compra': response_form.get('dataC'),
            'id_funcionario': id_funcionario,
            'revisoes_pendentes': response_form.get('revisoes'),
            'telefone': format_telefone(response_form.get('telefone')),
            'data_ultima_revisao': response_form.get('date_ultima_rev') or None,
            'nome_conjuge': response_form.get('nome_conjuge') if response_form.get('casado') == 'Sim' else None,
            'data_casamento': response_form.get('data_casamento') if response_form.get('casado') == 'Sim' else None,
            'data_aniver_conjuge': response_form.get('data_aniver_conjuge') if response_form.get('casado') == 'Sim' else None
        }
        
        try:

            id_cliente = Cliente.cadastrar(data)

            if response_form.get('filho') == 'Sim':
                self._processar_filhos(response_form, id_cliente)

            return "Cadastro realizado com sucesso!"
        except ValueError as e:
            return str(e)
        except Exception as e:
            return f"Erro no cadastro: {str(e)}"
        

    def _processar_filhos(self, form_data, id_cliente):
        try:
            controllerFilho = FilhoController()

            num_filhos = int(form_data.get('num_filhos'))

            for i in range(num_filhos):
                nome_filho = form_data.getlist(f"nome_filho_{i}")
                data_nasc_filho = form_data.getlist(f"data_nasc_filho_{i}")

                # Pegando apenas o primeiro valor, caso seja uma lista
                dado = {
                    'nome': nome_filho[0] if nome_filho else None,
                    'data_nascimento': data_nasc_filho[0] if data_nasc_filho else None
                }

                controllerFilho.Cadastrar(dado, id_cliente)
                    
        except Exception as e:
            print(e)

        


    def ListarClientes(self):
        id_func = session.get("id")

        try:
            clientes, filhos = Cliente.GetClientes(id_func)
            return True, "", clientes, filhos, id_func
        except Exception as e:
            return False, f"Erro ao listar clientes: {str(e)}", None, None, id_func
        

    def ListarTodosClientes(self):
        try:
            clientes, filhos = Cliente.GetTodosClientes()
            return True, "", clientes, filhos
        except Exception as e:
            return False, f"Erro ao listar clientes: {str(e)}", None, None
        


    def DeletarCliente(self, id_cliente):
        try:
            Cliente.Deletar(id_cliente)
            return "Cliente deletado com sucesso!"
        except Exception as e:
            return f"Erro ao deletar o cliente: {str(e)}"
        


    def AtualizarClienteForm(self, id_cliente):
        try:
            clientes, filhos, casado, TemFilho, nfilhos = Cliente.GetClienteAtualizar(id_cliente)
            return True, "", clientes, filhos, casado, TemFilho, nfilhos
        except Exception as e:
            return False, f"Erro ao listar clientes: {str(e)}", None, None, None, None, None
        

    def AtualizarClientee(self,response_form, id_cliente):

        cpf = response_form.get("cpf")
        nome = response_form.get("nome")
        nomeConjuge = response_form.get("nome_conjuge")
        dCompra = response_form.get("dataC")
        dCompra = datetime.strptime(dCompra, '%Y-%m-%d').date() if dCompra else None
        dNasc = response_form.get("dataN")
        dNasc = datetime.strptime(dNasc, '%Y-%m-%d').date() if dNasc else None
        dCasam = response_form.get("data_casamento")
        dCasam = datetime.strptime(dCasam, '%Y-%m-%d').date() if dCasam else None
        revPend = response_form.get("revisoes")
        dataNc = response_form.get("data_aniver_conjuge")
        dataNc = datetime.strptime(dataNc, '%Y-%m-%d').date() if dataNc else None
        telefone = format_telefone(response_form.get("telefone"))
        dataUR = response_form.get("date_ultima_rev")
        dataUR = datetime.strptime(dataUR, '%Y-%m-%d').date() if dataUR else None

        data = {
            'cpf': cpf,
            'nome': nome,
            'nome_conjuge': nomeConjuge,
            'data_aniver_conjuge': dataNc,
            'data_compra': dCompra,
            'data_nascimento': dNasc,
            'data_casamento': dCasam,
            'revisoes_pendentes': revPend,
            'telefone': telefone,
            'data_ultima_revisao': dataUR
        }
        print(data)
        print("---------------------")
        print(id_cliente)
        print("---------------------")

        id_client = Cliente.AtualizarClient(data, id_cliente)
        print(id_client)

        try:
            # id_client = Cliente.AtualizarClient(data, id_cliente)
            # print(id_client)
            self._processar_filhos(response_form, id_client)
            return "Atualização realizada com sucesso!"
        except ValueError as e:
            return str(e)
        except Exception as e:
            return f"Erro no cadastro: {str(e)}"