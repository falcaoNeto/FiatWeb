from entity.login import Login
from flask import session

class LoginController:

    def Verificar_Login(self, response_form):
        try:
            cpf = response_form.get("cpf")
            senha = response_form.get("senha")
        
            login = Login.Verificar(cpf, senha)
            session["id"] = login[0]
            session["nome"] = login[2]
            
            return True, "Login realizado com sucesso"
        except Exception as e:
                return False , e
