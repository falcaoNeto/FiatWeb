from BD.bd import bd_pool
from BD.bdPinecone import pc
import time
import json

class Carro:
    def cadastrarCarro(modelo):
        connect = None
        cursor = None
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "INSERT INTO carro (modelo) VALUES (%s) RETURNING id"
            cursor.execute(query, (modelo,))
            id_carro = cursor.fetchone()[0]
            connect.commit()
            return id_carro
        except Exception as e:
            if connect:
                connect.rollback() 
            raise RuntimeError(f"Ocorreu um erro: {str(e)}", "cadastrar carro")
        finally:
            if cursor:
                cursor.close()
            if connect:
                bd_pool.putconn(connect)

    def cadastrarCarroDados(dado, id_carro):
        connect = None
        cursor = None
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "INSERT INTO carrodados (titulo, texto, carro_id) VALUES (%s, %s, %s) RETURNING id"
            cursor.execute(query, (dado["titulo"], dado["texto"], id_carro))
            id_carroDado = cursor.fetchone()[0]
            connect.commit()
            return id_carroDado
        except Exception as e:
            if connect:
                connect.rollback() 
            raise RuntimeError(f"Ocorreu um erro: {str(e)}", "cadastrar carro")
        finally:
            if cursor:
                cursor.close()
            if connect:
                bd_pool.putconn(connect)

        


    def cadastrarCarroPinecone(carro, id_carroDado):
        try:
            index_name = "carrosfiat"
            index = pc.Index(index_name)
            dados_for_embeddings = [f"O modelo {carro['modelo']} no quesito {carro['titulo']} possui: {carro['texto']}"]
            embeddings = pc.inference.embed(
                model="multilingual-e5-large",
                inputs=dados_for_embeddings,
                parameters={"input_type": "passage", "truncate": "END"}
            )

            while not pc.describe_index(index_name).status['ready']:
                time.sleep(1)

            valores_embeddings = embeddings.data[0]["values"]
            
            vectors = [{
                "id": str(id_carroDado),
                "values": valores_embeddings,
                "metadata": {
                    "modelo": carro["modelo"],
                    "titulo": carro["titulo"],
                    "dados": carro["texto"]
                }
            }]
            index.upsert(vectors=vectors, namespace="ns1")
        except Exception as e:
            raise RuntimeError(f"Ocorreu um erro: {str(e)}", "cadastrar carro - Pinecone")
            

    

    def Listar():
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "SELECT * FROM carro INNER JOIN carrodados ON carro.id = carrodados.carro_id"
            cursor.execute(query)
            carros = cursor.fetchall()

            return carros
        except Exception as e:
            raise RuntimeError(f"Ocorreu um erro: {str(e)}", "listar carros")
        finally:
            if connect:
                cursor.close()
                bd_pool.putconn(connect)
        
    def DeletarBD(id_carro):
        connect = None
        cursor = None
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "DELETE FROM carro WHERE id = %s"
            cursor.execute(query, (id_carro,))
            connect.commit()
        except Exception as e:
            raise RuntimeError(f"Ocorreu um erro: {str(e)}", "deletar carro")
        finally:
            if connect:
                cursor.close()
                bd_pool.putconn(connect)



    def DeletarDadoBD(id_carro):
        connect = None
        cursor = None
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "DELETE FROM carrodados WHERE id = %s"
            cursor.execute(query, (id_carro,))
            connect.commit()
        except Exception as e:
            raise RuntimeError(f"Ocorreu um erro: {str(e)}", "deletar carro")
        finally:
            if connect:
                cursor.close()
                bd_pool.putconn(connect)    


    def DeletarPinecone(id_carro):
        try:
            index_name = "carrosfiat"
            index = pc.Index(index_name)
            index.delete(ids=[str(id_carro)], namespace="ns1")
        except Exception as e:
            raise RuntimeError(f"Ocorreu um erro: {str(e)}", "deletar carro - Pinecone")
        

    def GetCarro(id_carro):
        connect = None
        cursor = None
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "SELECT * FROM carro WHERE id = %s"
            cursor.execute(query, (id_carro,))
            carro = cursor.fetchall()

            return carro
        except Exception as e:
            raise RuntimeError(f"Ocorreu um erro: {str(e)}", "get carro")
        finally:
            if connect:
                cursor.close()
                bd_pool.putconn(connect)

    def GetCarroDados(id_carro):
            connect = None
            cursor = None
            try:
                connect = bd_pool.getconn()
                cursor = connect.cursor()
                query = "SELECT * FROM carrodados WHERE id = %s"
                cursor.execute(query, (id_carro,))
                carro = cursor.fetchall()

                return carro
            except Exception as e:
                raise RuntimeError(f"Ocorreu um erro: {str(e)}", "get carro")
            finally:
                if connect:
                    cursor.close()
                    bd_pool.putconn(connect)

    def AtualizarDado(data):
        connect = None
        cursor = None
        try:
            connect = bd_pool.getconn()
            cursor = connect.cursor()
            query = "UPDATE carrodados SET titulo = %s, texto = %s WHERE id = %s"
            cursor.execute(query, (data["titulo"], data["texto"], data["id_dado"]))
            connect.commit()
        except Exception as e:
            raise RuntimeError(f"Ocorreu um erro: {str(e)}", "atualizar carro")
        finally:
            if connect:
                cursor.close()
                bd_pool.putconn(connect)



