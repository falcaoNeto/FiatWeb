from BD.bd import bd_pool

class Filho:
    @staticmethod
    def cadastrar(filho, id_cliente):
        try:
            print(filho)
            print("--------------------------------------------------------")
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "INSERT INTO filho (nome, data_nascimento, id_cliente) VALUES (%s, %s, %s)"
            cursor.execute(query, (filho["nome"], filho["data_nascimento"], id_cliente))
            connect.commit()
        except Exception as e: 
            print(e)
        finally:
            cursor.close()
            connect.close()


    def Deletar(id_filho):
        connect = None
        cursor = None
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "DELETE FROM filho WHERE id_filho = %s"
            cursor.execute(query, (id_filho,))
            connect.commit()

        except Exception as e:
            if connect:
                connect.rollback()
            raise RuntimeError(f"Erro ao deletar filho: {e}")
        finally:
            if cursor:
                cursor.close()
            if connect:
                bd_pool.putconn(connect)