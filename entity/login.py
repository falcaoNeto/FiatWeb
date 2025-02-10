from BD.bd import bd_pool
import psycopg2
class Login:
    @staticmethod

    def Verificar(cpf, senha):
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()

            cursor.execute("SELECT * FROM funcionario WHERE cpf = %s AND senha = %s", (cpf, senha))
            login = cursor.fetchone()

            if login:
                return login

            raise ValueError("CPF ou senha incorretos.")
            
        except psycopg2.DatabaseError as e:
            raise RuntimeError("Erro no banco de dados: " + str(e)) 
        except Exception as e:
            raise RuntimeError("Ocorreu um erro inesperado: " + str(e))
        finally:
            if connect:
                cursor.close()
                bd_pool.putconn(connect)


            