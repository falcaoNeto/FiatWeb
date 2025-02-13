from BD.bd import bd_pool

class Filho:
    @staticmethod
    def Insert(filho, id_cliente):
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


    def Delete(id_filho):
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

    def Select_for_update(id_filho):
        connect = None
        cursor = None
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "SELECT * FROM filho WHERE id_filho = %s"
            cursor.execute(query, (id_filho,))
            filho = cursor.fetchone()

            return filho
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar filho: {e}")
        finally:
            if connect:
                cursor.close()
                bd_pool.putconn(connect)


    def Update(filho):
        connect = None
        cursor = None
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "UPDATE filho SET nome = %s, data_nascimento = %s WHERE id_filho = %s"
            cursor.execute(query, (filho["nome"], filho["data_nascimento"], filho["id_filho"]))
            connect.commit()
        except Exception as e:
            if connect:
                connect.rollback()
            raise RuntimeError(f"Erro ao atualizar filho: {e}")
        finally:
            if connect:
                cursor.close()
                bd_pool.putconn(connect)