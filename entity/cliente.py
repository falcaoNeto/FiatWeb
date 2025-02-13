# entity/cliente.py

from BD.bd import bd_pool


class Cliente:
    @staticmethod
    def Insert(data):
        conn = None
        cursor = None
        try:
            conn = bd_pool.getconn()
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO cliente (
                    cpf, nome, nome_conjuge, data_compra, data_casamento,
                    data_nascimento, id_funcionario, revisoes_pendentes,
                    data_aniver_conjuge, telefone, data_ultima_revisao
                )
                VALUES (
                    %(cpf)s, %(nome)s, %(nome_conjuge)s, %(data_compra)s, %(data_casamento)s,
                    %(data_nascimento)s, %(id_funcionario)s, %(revisoes_pendentes)s,
                    %(data_aniver_conjuge)s, %(telefone)s, %(data_ultima_revisao)s
                )
                RETURNING id_clien;
            """
            cursor.execute(insert_query, data)
            id_cliente = cursor.fetchone()[0]
            conn.commit()
            return id_cliente
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                bd_pool.putconn(conn)

    @staticmethod
    def Select_with_idFunc(id_funcionario):
        conn = None
        cursor = None
        try:
            conn = bd_pool.getconn()
            cursor = conn.cursor()
            query = """
            SELECT 
                c.id_clien,
                c.cpf,
                c.nome AS nome_cliente,
                c.nome_conjuge,
                c.data_compra,
                c.data_nascimento,
                c.data_casamento,
                c.id_funcionario,
                c.revisoes_pendentes,
                c.data_aniver_conjuge,
                c.telefone,
                c.data_ultima_revisao,
                f.id_filho,
                f.nome AS nome_filho,
                f.data_nascimento AS data_nascimento_filho,
                f.id_cliente AS id_cliente
            FROM cliente c
            LEFT JOIN filho f ON c.id_clien = f.id_cliente
            WHERE c.id_funcionario = %s;

        """
            cursor.execute(query, (id_funcionario,))
            rows = cursor.fetchall()
            nomes_colunas = [desc[0] for desc in cursor.description]
            dados = [dict(zip(nomes_colunas, rows)) for rows in rows]
            

            return dados
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                bd_pool.putconn(conn)

    @staticmethod
    def SelectAll():
        """
        Retorna todos os clientes e, para cada um, os filhos associados.
        Cada registro é convertido para dicionário.
        """
        conn = None
        cursor = None
        try:
            conn = bd_pool.getconn()
            cursor = conn.cursor()
            # Buscar todos os clientes
            query_clientes = "SELECT * FROM cliente;"
            cursor.execute(query_clientes)
            col_names = [desc[0] for desc in cursor.description]
            clientes = [dict(zip(col_names, row)) for row in cursor.fetchall()]

            # Buscar os filhos de todos os clientes
            client_ids = [cliente["id_clien"] for cliente in clientes]
            filhos = []
            if client_ids:
                query_filhos = "SELECT * FROM filho WHERE id_cliente IN %s;"
                cursor.execute(query_filhos, (tuple(client_ids),))
                col_names_filhos = [desc[0] for desc in cursor.description]
                filhos = [dict(zip(col_names_filhos, row)) for row in cursor.fetchall()]

            return clientes, filhos
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                bd_pool.putconn(conn)

    @staticmethod
    def Delete(id_cliente):
        """
        Deleta o cliente cujo id é passado como parâmetro.
        Considera que as restrições (por exemplo, ON DELETE CASCADE)
        estão definidas no banco para a tabela filho.
        """
        conn = None
        cursor = None
        try:
            conn = bd_pool.getconn()
            cursor = conn.cursor()
            delete_query = "DELETE FROM cliente WHERE id_clien = %s;"
            cursor.execute(delete_query, (id_cliente,))
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                bd_pool.putconn(conn)

    @staticmethod
    def Select_for_update(id_cliente):
        conn = None
        cursor = None
        try:
            conn = bd_pool.getconn()
            cursor = conn.cursor()
            # Buscar dados do cliente
            query_cliente = "SELECT * FROM cliente WHERE id_clien = %s;"
            cursor.execute(query_cliente, (id_cliente,))
            col_names = [desc[0] for desc in cursor.description]
            cliente_row = cursor.fetchone()
            if not cliente_row:
                raise ValueError("Cliente não encontrado")
            cliente = dict(zip(col_names, cliente_row))

            # Definir se o cliente é casado (se possui nome_conjuge cadastrado)
            casado = True if cliente.get("nome_conjuge") else False

            # Buscar os filhos do cliente
            query_filhos = "SELECT * FROM filho WHERE id_cliente = %s;"
            cursor.execute(query_filhos, (id_cliente,))
            col_names_filhos = [desc[0] for desc in cursor.description]
            filhos = [dict(zip(col_names_filhos, row)) for row in cursor.fetchall()]

            TemFilho = True if filhos else False
            nfilhos = len(filhos)

            return cliente, filhos, casado, TemFilho, nfilhos
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                bd_pool.putconn(conn)

    @staticmethod
    def Update(data, id_cliente):
        """
        Atualiza os dados do cliente na tabela 'cliente' com os valores
        passados no dicionário data e retorna o id atualizado.
        Espera que data contenha as chaves:
          cpf, nome, nome_conjuge, data_aniver_conjuge, data_compra,
          data_nascimento, data_casamento, revisoes_pendentes, telefone,
          data_ultima_revisao
        """
        conn = None
        cursor = None
        try:
            conn = bd_pool.getconn()
            cursor = conn.cursor()
            update_query = """
                UPDATE cliente
                SET
                    cpf = %(cpf)s,
                    nome = %(nome)s,
                    nome_conjuge = %(nome_conjuge)s,
                    data_aniver_conjuge = %(data_aniver_conjuge)s,
                    data_compra = %(data_compra)s,
                    data_nascimento = %(data_nascimento)s,
                    data_casamento = %(data_casamento)s,
                    revisoes_pendentes = %(revisoes_pendentes)s,
                    telefone = %(telefone)s,
                    data_ultima_revisao = %(data_ultima_revisao)s
                WHERE id_clien = %(id_cliente)s
                RETURNING id_clien;
            """
            # Adiciona o id_cliente ao dicionário de dados
            data['id_cliente'] = id_cliente
            cursor.execute(update_query, data)
            updated_id = cursor.fetchone()[0]
            conn.commit()
            return updated_id
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                bd_pool.putconn(conn)

if __name__ == "__main__":
    ...