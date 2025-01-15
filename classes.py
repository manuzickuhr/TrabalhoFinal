from datetime import datetime, timedelta
import mysql.connector

conexao = mysql.connector.connect(
    host = 'localhost' ,
    user = 'root' ,
    password = 'root',
    database = 'trabalhoFinal',
)

if conexao.is_connected():
    print("Conexão realizada com sucesso!")
else:
    print("Erro ao conectar ao banco de dados.")

class Usuario:
    def __init__(self, id, usuario, senha, cpf, primeiroNome, sobrenome):
        self.id = id
        self.usuario = usuario
        self.senha = senha
        self.cpf = cpf
        self.primeiroNome = primeiroNome
        self.sobrenome = sobrenome

    def listar_usuarios():
        try:
            cursor = conexao.cursor()
            query = "SELECT * FROM Usuario"
            cursor.execute(query)
            resultados = cursor.fetchall()
            for row in resultados:
                print(row)
        except mysql.connector.Error as e:
            print(f"Erro ao listar usuários: {e}")
        finally:
            cursor.close()

class Funcionario(Usuario):
    def __init__(self, id, usuario, senha, cpf, primeiroNome, sobrenome, email, funcao):
        super().__init__(id, usuario, senha, cpf, primeiroNome, sobrenome)
        self.email = email
        self.funcao = funcao

    def cadastrar_funcionario(usuario, senha, cpf, primeiro_nome, sobrenome, email, funcao):
        try:
            cursor = conexao.cursor()
            
            query_usuario = """
            INSERT INTO Usuario (usuario, senha, cpf, primeiroNome, sobrenome, tipo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_usuario, (usuario, senha, cpf, primeiro_nome, sobrenome, "Funcionario"))
            usuario_id = cursor.lastrowid

            query_funcionario = "INSERT INTO Funcionario (id, email, funcao) VALUES (%s, %s, %s)"
            cursor.execute(query_funcionario, (usuario_id, email, funcao))

            conexao.commit()
            print("Funcionário cadastrado com sucesso!")
        except mysql.connector.Error as e:
            print(f"Erro ao cadastrar funcionário: {e}")
            conexao.rollback()
        finally:
            cursor.close()

    def excluir_funcionario(id_gerente, id_funcionario):
        try:
            cursor = conexao.cursor()

            query_funcao = "SELECT funcao FROM Funcionario WHERE id = %s"
            cursor.execute(query_funcao, (id_gerente,))
            resultado = cursor.fetchone()

            if not resultado:
                print("Funcionário não encontrado.")
                return
        
            funcao = resultado[0]

            if funcao != "Gerente":
                print("Apenas gerentes podem excluir funcionários.")
                return

            query_verificar = "SELECT id FROM Funcionario WHERE id = %s"
            cursor.execute(query_verificar, (id_funcionario,))
            if not cursor.fetchone():
                print("Funcionário não encontrado.")
                return

            query_funcionario = "DELETE FROM Funcionario WHERE id = %s"
            cursor.execute(query_funcionario, (id_funcionario,))

            query_usuario = "DELETE FROM Usuario WHERE id = %s"
            cursor.execute(query_usuario, (id_funcionario,))

            conexao.commit()
            print(f"Funcionário com ID {id_funcionario} excluído com sucesso!")
        except mysql.connector.Error as e:
            print(f"Erro ao excluir funcionário: {e}")
            conexao.rollback()
        finally:
            cursor.close()

    def editar_funcionario(id, usuario=None, senha=None, cpf=None, primeiroNome=None, sobrenome=None, email=None, funcao=None):
        try:
            cursor = conexao.cursor()

            campos_atualizar = []
            dados = []

            campos_funcionario = []
            dados_funcionario =[]

            if usuario:
                campos_atualizar.append("usuario = %s")
                dados.append(usuario)
            if senha:
                campos_atualizar.append("senha = %s")
                dados.append(senha)
            if cpf:
                campos_atualizar.append("cpf = %s")
                dados.append(cpf)
            if primeiroNome:
                campos_atualizar.append("primeiroNome = %s")
                dados.append(primeiroNome)
            if sobrenome:
                campos_atualizar.append("sobrenome = %s")
                dados.append(sobrenome)
            if email:
                campos_funcionario.append("email = %s")
                dados_funcionario.append(email)
            if funcao:
                campos_funcionario.append("funcao = %s")
                dados_funcionario.append(funcao)

            if not campos_atualizar and not campos_funcionario:
                print("Nenhuma informação fornecida para atualização.")
                return
            
            query_verificar = "SELECT id FROM Funcionario WHERE id = %s"
            cursor.execute(query_verificar, (id,))
            if not cursor.fetchone():
                print("Funcionário não encontrado.")
                return

            query_funcionario = f"UPDATE Funcionario SET {', '.join(campos_funcionario)} WHERE id = %s"
            dados_funcionario.append(id)
            cursor.execute(query_funcionario, dados_funcionario)
            conexao.commit()

            query_usuario = f"UPDATE Usuario SET {', '.join(campos_atualizar)} WHERE id = %s"
            dados.append(id)
            cursor.execute(query_usuario, dados)
            conexao.commit()

            print(f"Funcionário com ID {id} atualizado com sucesso!")
        except mysql.connector.Error as e:
            print(f"Erro ao editar funcionário: {e}")
            conexao.rollback()
        finally:
            cursor.close()

    def listar_funcionarios():
        try:
            cursor = conexao.cursor()
            query = "SELECT u.id, u.usuario, u.cpf, u.primeiroNome, u.sobrenome, u.tipo, f.email, f.funcao FROM Usuario u JOIN Funcionario f ON u.id = f.id"
            cursor.execute(query)
            resultados = cursor.fetchall()
            if resultados:
                for row in resultados:
                    print(row)
            else:
                print("Nenhum funcionário encontrado.")
        except mysql.connector.Error as e:
            print(f"Erro ao listar funcionários: {e}")
        finally:
            cursor.close()

    def cadastrar_cliente(usuario, senha, cpf, primeiro_nome, sobrenome, emprestimos):
        try:
            cursor = conexao.cursor()

            query_usuario = """
            INSERT INTO Usuario (usuario, senha, cpf, primeiroNome, sobrenome, tipo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_usuario, (usuario, senha, cpf, primeiro_nome, sobrenome, "Cliente"))
            usuario_id = cursor.lastrowid

            query_cliente = """
            INSERT INTO Cliente (id, emprestimos)
            VALUES (%s, %s)
            """
            cursor.execute(query_cliente, (usuario_id, emprestimos))
            conexao.commit()
            print("Cliente cadastrado com sucesso!")
        except mysql.connector.Error as e:
            print(f"Erro ao cadastrar cliente: {e}")
            conexao.rollback()
        finally:
            cursor.close()

    def excluir_cliente(id):
        try:
            cursor = conexao.cursor()

            query_verificar = "SELECT id FROM Cliente WHERE id = %s"
            cursor.execute(query_verificar, (id,))
            if not cursor.fetchone():
                print("Cliente não encontrado.")
                return

            query_cliente = "DELETE FROM Cliente WHERE id = %s"
            cursor.execute(query_cliente, (id,))

            query_usuario = "DELETE FROM Usuario WHERE id = %s"
            cursor.execute(query_usuario, (id,))

            conexao.commit()
            print(f"Cliente com ID {id} foi excluído com sucesso!")
        except mysql.connector.Error as e:
            print(f"Erro ao excluir cliente: {e}")
            conexao.rollback()
        finally:
            cursor.close()
    
    def editar_cliente(id, usuario=None, senha=None, cpf=None, primeiroNome=None, sobrenome=None, emprestimos=None):
        try:
            cursor = conexao.cursor()

            campos_atualizar = []
            dados = []

            campos_cliente = []
            dados_cliente = []

            if usuario:
                campos_atualizar.append("usuario = %s")
                dados.append(usuario)
            if senha:
                campos_atualizar.append("senha = %s")
                dados.append(senha)
            if cpf:
                campos_atualizar.append("cpf = %s")
                dados.append(cpf)
            if primeiroNome:
                campos_atualizar.append("primeiroNome = %s")
                dados.append(primeiroNome)
            if sobrenome:
                campos_atualizar.append("sobrenome = %s")
                dados.append(sobrenome)

            if emprestimos is not None:
                campos_cliente.append("emprestimos = %s")
                dados_cliente.append(emprestimos)

            if not campos_atualizar and not campos_cliente:
                print("Nenhuma informação fornecida para atualização.")
                return

            if campos_cliente:
                query_cliente = f"UPDATE Cliente SET {', '.join(campos_cliente)} WHERE id = %s"
                dados_cliente.append(id)
                cursor.execute(query_cliente, dados_cliente)
                conexao.commit()

            if campos_atualizar:
                query_usuario = f"UPDATE Usuario SET {', '.join(campos_atualizar)} WHERE id = %s"
                dados.append(id)
                cursor.execute(query_usuario, dados)
                conexao.commit()

            print(f"Cliente com ID {id} atualizado com sucesso!")
        except mysql.connector.Error as e:
            print(f"Erro ao editar cliente: {e}")
            conexao.rollback()
        finally:
            cursor.close()

    def listar_clientes():
        try:
            cursor = conexao.cursor()
            query = "SELECT u.id, u.usuario, u.cpf, u.primeiroNome, u.sobrenome, u.tipo, c.emprestimos FROM Usuario u JOIN Cliente c ON u.id = c.id"
            cursor.execute(query)
            resultados = cursor.fetchall()
            if resultados:
                for row in resultados:
                    print(row)
            else:
                print("Nenhum cliente encontrado.")
        except mysql.connector.Error as e:
            print(f"Erro ao listar clientes: {e}")
        finally:
            cursor.close()

class Cliente:
    def __init__(self, id_cliente):
        self.id_cliente = id_cliente

    def ver_livros():

        try:
            cursor = conexao.cursor()

            query = "SELECT id, nome, autor, quantidade, emprestado FROM livro WHERE quantidade > 0"
            cursor.execute(query)
            livros = cursor.fetchall()

            if livros:
                print("Livros disponíveis:")
                for livro in livros:
                    print(f"ID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]} | Quantidade: {livro[3]} | Cópias Emprestadas: {livro[4]}")
            else:
                print("Não há livros disponíveis no momento.")

        except mysql.connector.Error as erro:
            print(f"Erro ao listar os livros: {erro}")

        finally:
            cursor.close()

    def ver_emprestimos(id_cliente):

        try:
            cursor = conexao.cursor()

            query = "SELECT id, id_livro, data_emprestimo, data_devolucao, status FROM emprestimo WHERE id_cliente = %s"
            cursor.execute(query, (id_cliente,))
            emprestimos = cursor.fetchall()

            if emprestimos:
                print(f"Empréstimos de Cliente ID {id_cliente}:")
                for emprestimo in emprestimos:
                    status = "Ativo" if emprestimo[4] else "Devolvido"
                    print(f"ID: {emprestimo[0]} | Livro ID: {emprestimo[1]} | Data Empréstimo: {emprestimo[2]} | Data Devolução: {emprestimo[3]} | Status: {status}")
            else:
                print("Não há empréstimos registrados para este cliente.")

        except mysql.connector.Error as erro:
            print(f"Erro ao listar os empréstimos: {erro}")

        finally:
            cursor.close()

    def ver_multas(id_cliente):
        try:
            cursor = conexao.cursor()

            query = "SELECT id, dias_atraso, valor FROM multa WHERE cliente_id = %s AND status = 'pendente'"
            cursor.execute(query, (id_cliente,))
            multas = cursor.fetchall()

            if multas:
                print(f"Multas pendentes para Cliente ID {id_cliente}:")
                for multa in multas:
                    print(f"ID: {multa[0]} | Dias de Atraso: {multa[1]} | Valor da Multa: R${multa[2]:.2f}")
            else:
                print("Não há multas pendentes para este cliente.")

        except mysql.connector.Error as erro:
            print(f"Erro ao listar as multas: {erro}")

        finally:
            cursor.close()
    
    def pagar_multa(id_multa):
        try:
            cursor = conexao.cursor()

            query_verificar_multa = "SELECT id, status FROM multa WHERE id = %s AND status = 'pendente'"
            cursor.execute(query_verificar_multa, (id_multa,))
            multa = cursor.fetchone()

            if not multa:
                print("Multa não encontrada ou já foi paga.")
                return

            query_atualizar_multa = "UPDATE multa SET status = 'paga' WHERE id = %s"
            cursor.execute(query_atualizar_multa, (id_multa,))

            conexao.commit()
            print(f"Multa com ID {id_multa} paga com sucesso!")

        except mysql.connector.Error as erro:
            print(f"Erro ao pagar multa: {erro}")
            conexao.rollback()

        finally:
            cursor.close()


class Livro:
    def __init__(self, id, isbn, nome, autor, edicao, quantidade, emprestado):
        self.id = id
        self.isbn = isbn
        self.nome = nome
        self.autor = autor
        self.edicao = edicao
        self.quantidade = quantidade
        self.emprestado = emprestado

    def adicionar_livro(isbn, nome, autor, edicao, quantidade):
        try:
            cursor = conexao.cursor()
            query = "INSERT INTO Livro (isbn, nome, autor, edicao, quantidade) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (isbn, nome, autor, edicao, quantidade))
            conexao.commit()
            print("Livro adicionado com sucesso!")
        except mysql.connector.Error as e:
            print(f"Erro ao adicionar livro: {e}")
            conexao.rollback()
        finally:
            cursor.close()

    def excluir_livro(id):
        try:
            cursor = conexao.cursor()

            query_verificar = "SELECT id FROM Livro WHERE id = %s"
            cursor.execute(query_verificar, (id,))
            if not cursor.fetchone():
                print("Livro não encontrado.")
                return

            query = "DELETE FROM Livro WHERE id = %s"
            cursor.execute(query, (id,))
            conexao.commit()
            print(f"Livro com ID {id} excluído com sucesso!")
        except mysql.connector.Error as e:
            print(f"Erro ao excluir livro: {e}")
            conexao.rollback()
        finally:
            cursor.close()

    def editar_livro(id, isbn=None, nome=None, autor=None, edicao=None, quantidade=None):
        try:
            cursor = conexao.cursor()

            campos_atualizar = []
            dados = []

            if isbn:
                campos_atualizar.append("isbn = %s")
                dados.append(isbn)
            if nome:
                campos_atualizar.append("nome = %s")
                dados.append(nome)
            if autor:
                campos_atualizar.append("autor = %s")
                dados.append(autor)
            if edicao:
                campos_atualizar.append("edicao = %s")
                dados.append(edicao)
            if quantidade:
                campos_atualizar.append("quantidade = %s")
                dados.append(quantidade)

            if not campos_atualizar:
                print("Nenhuma informação fornecida para atualização.")
                return

            query = f"UPDATE Livro SET {', '.join(campos_atualizar)} WHERE id = %s"
            dados.append(id)
            cursor.execute(query, dados)
            conexao.commit()

            print(f"Livro com ID {id} atualizado com sucesso!")
        except mysql.connector.Error as e:
            print(f"Erro ao editar livro: {e}")
            conexao.rollback()
        finally:
            cursor.close()

class Emprestimo:
    def __init__(self, id_livro, id_cliente, id_funcionario):
        self.data_emprestimo = datetime.now()
        self.data_devolucao = self.data_emprestimo + timedelta(days=15)
        self.id_livro = id_livro
        self.id_cliente = id_cliente
        self.id_funcionario = id_funcionario
        self.status = True

    def verificar_limite(id_cliente):
        try:
            cursor = conexao.cursor()

            query_verificar_cliente = "SELECT id FROM cliente WHERE id = %s"
            cursor.execute(query_verificar_cliente, (id_cliente,))
            cliente_existe = cursor.fetchone()

            if not cliente_existe:
                print("Cliente não encontrado.")
                return False 

            query_verificar_emprestimos = "SELECT COUNT(*) FROM emprestimo WHERE id_cliente = %s AND status = TRUE"
            cursor.execute(query_verificar_emprestimos, (id_cliente,))
            numero_emprestimos = cursor.fetchone()[0]  

            numero_maximo = 3

            if numero_emprestimos >= numero_maximo:
                print("Limite de empréstimos atingido! Não é possível realizar o empréstimo.")
                return False  
            else:
                return True 

        except mysql.connector.Error as erro:
            print(f"Erro ao verificar limite: {erro}")
            return False
        finally:
            cursor.close()

    def calcular_multa(id_cliente):
        try:
            cursor = conexao.cursor()

            query_verificar_emprestimos = "SELECT id, data_devolucao FROM emprestimo WHERE id_cliente = %s AND status = TRUE"
            cursor.execute(query_verificar_emprestimos, (id_cliente,))
            emprestimos = cursor.fetchall()

            if not emprestimos:
                print("Não há empréstimos pendentes para este cliente.")
                return

            for emprestimo in emprestimos:
                id_emprestimo = emprestimo[0]  
                data_devolucao = emprestimo[1]  
                data_atual = datetime.now().date()

                if data_atual > data_devolucao:
                    dias_atraso = (data_atual - data_devolucao).days
                    if dias_atraso > 0:
                        valor = dias_atraso * 0.50

                        query_verificar_multa = "SELECT id FROM multa WHERE cliente_id = %s AND status = 'pendente'"
                        cursor.execute(query_verificar_multa, (id_cliente,))
                        multa_existente = cursor.fetchone()

                        if multa_existente:
 
                            query_atualizar = "UPDATE multa SET dias_atraso = %s, valor = %s WHERE id = %s"
                            cursor.execute(query_atualizar, (dias_atraso, valor, multa_existente[0]))
                            print(f"Multa atualizada: {dias_atraso} dias de atraso, valor: R${valor}")
                        else:
                            query_inserir = "INSERT INTO multa (dias_atraso, valor, cliente_id, status, emprestimo_id) VALUES (%s, %s, %s, 'pendente', %s)"
                            cursor.execute(query_inserir, (dias_atraso, valor, id_cliente, id_emprestimo))
                            print(f"Nova multa gerada: {dias_atraso} dias de atraso, valor: R${valor}")

                        conexao.commit()

            print("Verificação de multas concluída.")

        except mysql.connector.Error as erro:
            print(f"Erro ao calcular multa: {erro}")

        finally:
            cursor.close()


    def realizar_emprestimo(self):
        try:
            cursor = conexao.cursor()

            if not Emprestimo.verificar_limite(self.id_cliente):
                print("Limite de empréstimos atingido! Não é possível realizar o empréstimo.")
                return

            query_verificar_quantidade = "SELECT quantidade, emprestado FROM livro WHERE id = %s"
            cursor.execute(query_verificar_quantidade, (self.id_livro,))
            resultado = cursor.fetchone()

            if resultado is None:
                print("Livro não encontrado.")
                return

            quantidade = resultado[0]
            emprestado = resultado[1] if resultado[1] is not None else 0  

            quantidade_disponivel = quantidade - emprestado
            if quantidade_disponivel < 1:
                print("Este livro está indisponível no momento.")
                return

            query_multa = "SELECT id FROM multa WHERE cliente_id = %s AND status = 'pendente'"
            cursor.execute(query_multa, (self.id_cliente,))
            multa_existente = cursor.fetchone()
            if multa_existente:
                print("Você tem uma multa em aberto e não pode realizar um empréstimo.")
                return

            data_emprestimo = datetime.now()
            data_devolucao = data_emprestimo + timedelta(days=15)

            query_inserir_emprestimo = (
                "INSERT INTO emprestimo (data_emprestimo, data_devolucao, id_livro, id_cliente, id_funcionario) VALUES (%s, %s, %s, %s, %s)"
            )
            cursor.execute(query_inserir_emprestimo, (data_emprestimo, data_devolucao, self.id_livro, self.id_cliente, self.id_funcionario))

            query_atualizar_quantidade = "UPDATE livro SET emprestado = emprestado + 1 WHERE id = %s"
            cursor.execute(query_atualizar_quantidade, (self.id_livro,))

            conexao.commit()
            print("Empréstimo realizado com sucesso!")

        except mysql.connector.Error as erro:
            print(f"Erro ao realizar empréstimo: {erro}")
        finally:
            cursor.close()

    def realizar_devolucao(id_emprestimo):
        try:
            cursor = conexao.cursor()

            query_verificar_emprestimo = "SELECT id_cliente, data_devolucao, status FROM emprestimo WHERE id = %s AND status = TRUE"
            cursor.execute(query_verificar_emprestimo, (id_emprestimo,))
            emprestimo = cursor.fetchone()

            if not emprestimo:
                print("Empréstimo não encontrado ou já foi devolvido.")
                return

            id_cliente = emprestimo[0]
            data_devolucao = emprestimo[1]
            status = emprestimo[2]

            query_verificar_multa = "SELECT id FROM multa WHERE cliente_id = %s AND status = 'pendente'"
            cursor.execute(query_verificar_multa, (id_cliente,))
            multa_existente = cursor.fetchone()

            if multa_existente:
                print("O cliente tem uma multa pendente e não pode devolver o livro ainda.")
                return

            data_atual = datetime.now().date()

            if data_atual > data_devolucao:
                Emprestimo.calcular_multa(id_cliente)
                print("Devolução após data de devolução.")

            else:
                print("Devolução dentro do prazo. Nenhuma multa será aplicada.")

            query_atualizar_emprestimo = "UPDATE emprestimo SET status = FALSE WHERE id = %s"
            cursor.execute(query_atualizar_emprestimo, (id_emprestimo,))

            query_atualizar_quantidade = "UPDATE livro SET emprestado = emprestado - 1 WHERE id = (SELECT id_livro FROM emprestimo WHERE id = %s)"
            cursor.execute(query_atualizar_quantidade, (id_emprestimo,))

            conexao.commit()

            print("Devolução realizada com sucesso!")

        except mysql.connector.Error as erro:
            print(f"Erro ao realizar devolução: {erro}")

        finally:
            cursor.close()


conexao.close()