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
        self.__usuario = usuario 
        self.__senha = senha
        self.cpf = cpf
        self.primeiroNome = primeiroNome
        self.sobrenome = sobrenome
    
    @property
    def usuario(self):
        return self.__usuario
    
    @usuario.setter
    def usuario(self, novo_usuario):
        self.__usuario = novo_usuario
    
    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, novo_senha):
        self.__senha = novo_senha

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
        super().__init__(id, usuario, senha,cpf, primeiroNome, sobrenome)
        self.email = email
        self.funcao = funcao

    def cadastrar_funcionario(conexao, usuario, senha, cpf, primeiro_nome, sobrenome, tipo, email, funcao):
        try:
            cursor = conexao.cursor()

            query_usuario = """
            INSERT INTO Usuario (usuario, senha, cpf, primeiroNome, sobrenome, tipo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores_usuario = (usuario, senha, cpf, primeiro_nome, sobrenome, tipo)
            cursor.execute(query_usuario, valores_usuario)
            conexao.commit()

            usuario_id = cursor.lastrowid

            query_funcionario = """
            INSERT INTO Funcionario (id, email, funcao)
            VALUES (%s, %s, %s)
            """
            valores_funcionario = (usuario_id, email, funcao)
            cursor.execute(query_funcionario, valores_funcionario)
            conexao.commit()

            print("Funcionário cadastrado com sucesso!")

        except mysql.connector.Error as e:
            print(f"Erro ao cadastrar funcionário: {e}")
            conexao.rollback()  

        finally:
            cursor.close()

    def cadastrar_cliente(conexao, usuario, senha, cpf, primeiro_nome, sobrenome, tipo, emprestimos):
        try:
            cursor = conexao.cursor()
            
            # Inserir na tabela Usuario
            query_usuario = """
            INSERT INTO Usuario (usuario, senha, cpf, primeiroNome, sobrenome, tipo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores_usuario = (usuario, senha, cpf, primeiro_nome, sobrenome, tipo)
            cursor.execute(query_usuario, valores_usuario)
            conexao.commit()
            
            usuario_id = cursor.lastrowid

            # Inserir na tabela Cliente
            query_cliente = """
            INSERT INTO Cliente (id, emprestimos)
            VALUES (%s, %s)
            """
            valores_cliente = (usuario_id, emprestimos)
            cursor.execute(query_cliente, valores_cliente)
            conexao.commit()

            print("Cliente cadastrado com sucesso!")

        except mysql.connector.Error as e:
            print(f"Erro ao cadastrar cliente: {e}")
            conexao.rollback()

        finally: 
            cursor.close()

    def editar_funcionario(id, funcionario, usuario=None, senha=None, cpf=None, primeiroNome=None, sobrenome=None, email=None, funcao=None):
        if funcionario.funcao == "Gerente":
            try: 
                cursor = conexao.cursor()

                campos_atualizar = []
                dados = []

                campos_funcionario = []
                dados_funcionario = []

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
                
                # Atualizando dados do usuário
                if campos_atualizar:
                    query_usuario = f"""UPDATE usuario
                        SET {', '.join(campos_atualizar)}
                        WHERE id = %s""" 
                    dados.append(id)
                    cursor.execute(query_usuario, dados)
                    conexao.commit()

                # Atualizando dados do funcionário
                if campos_funcionario:
                    query_funcionario = f"""UPDATE funcionario
                        SET {', '.join(campos_funcionario)}
                        WHERE id = %s"""
                    dados_funcionario.append(id)
                    cursor.execute(query_funcionario, dados_funcionario)
                    conexao.commit()

                print("Informações do funcionário atualizadas com sucesso!")

            except mysql.connector.Error as erro:
                print(f"Erro ao atualizar o funcionário: {erro}")

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
            if emprestimos:
                campos_cliente.append('emprestimos = %s')
                dados_cliente.append(emprestimos)

            if not campos_atualizar and not campos_cliente:
                    print("Nenhuma informação fornecida para atualização.")
                    return

            if campos_atualizar:
                    query_usuario = f"""UPDATE usuario
                        SET {', '.join(campos_atualizar)}
                        WHERE id = %s""" 
                    dados.append(id)
                    cursor.execute(query_usuario, dados)
                    conexao.commit()

            if campos_cliente:
                query_cliente = f"""UPDATE cliente
                    SET {','.join(campos_cliente)}
                    WHERE id = %s"""
                dados_cliente.append(id)
                cursor.execute(query_cliente, dados_cliente)
                conexao.commit()

            print("Informações do cliente atualizadas com sucesso!")

        except mysql.connector.Error as erro:
                print(f"Erro ao atualizar o cliente: {erro}")

        finally:
                cursor.close()
            
    def excluir_funcionario(valor, funcionario): #somente gerente
        if funcionario.funcao == "Gerente":
            try:
                cursor = conexao.cursor()
                query_funcionario = f"DELETE FROM funcionario WHERE id =%s"
                cursor.execute(query_funcionario, (valor,))
                conexao.commit()

                query_usuario = f"DELETE FROM usuario WHERE id = %s"
                cursor.execute(query_usuario, (valor,))
                conexao.commit()

                print(f'Registro da tabela funcionários onde id é igual a {valor} foi deletado. ')
            
            except mysql.connector.Error as e:
                print(f"Erro ao cadastrar funcionário: {e}")
                conexao.rollback()

            finally:
                cursor.close()

    def excluir_cliente(valor):
        try:
            cursor = conexao.cursor()
            query_cliente = f"DELETE FROM cliente WHERE id = %s" 
            cursor.execute(query_cliente, (valor,))
            conexao.commit()

            query_usuario = f"DELETE FROM usuario WHERE id = %s"
            cursor.execute(query_usuario, (valor,))
            conexao.commit()

            print(f'Registro da tabela clientes onde id é igual a {valor} foi deletado. ')

        except mysql.connector.Error as e:
            print(f"Erro ao cadastrar cliente: {e}")
            conexao.rollback()

        finally:
            cursor.close()

    def listar_funcionarios():
        try:
            cursor = conexao.cursor()
            query = "SELECT * FROM usuario u, funcionario f WHERE u.id = f.id and u.tipo = 'Funcionario'"
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            for row in resultados:
                print(row)
        except mysql.connector.Error as e:
            print(f"Erro ao listar funcionarios: {e}")
        finally:
            cursor.close()

    def listar_clientes():
        try:
            cursor = conexao.cursor()
            query = "SELECT * FROM usuario u, cliente c WHERE u.id = c.id and u.tipo = 'Cliente'"
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            for row in resultados:
                print(row)
        except mysql.connector.Error as e:
            print(f"Erro ao listar funcionarios: {e}")
        finally:
            cursor.close()

class Cliente(Usuario):
    def __init__(self, id, usuario, senha, cpf, primeiroNome, sobrenome, emprestimos):
        super().__init__(id, usuario, senha, cpf, primeiroNome, sobrenome)
        self.emprestimos = emprestimos

    def ver_livros():
        try:
            cursor = conexao.cursor()
            query = "SELECT * FROM livro"
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            for row in resultados:
                print(row)
        except mysql.connector.Error as e:
            print(f"Erro ao listar livros: {e}")
        finally:
            cursor.close()
    
    def ver_emprestimos():
        print('Ver os emprestimos linkados aquele cliente')

class Livro():
    def __init__(self, id, isbn, nome, autor, edicao, quantidade, emprestado):
        self.id = id
        self.isbn = isbn 
        self.nome = nome
        self.autor = autor
        self.edicao = edicao
        self.quantidade = quantidade
        self.emprestado = emprestado

    def adicionar_livro(conexao, isbn, nome, autor, edicao, quantidade):
        try:
            cursor = conexao.cursor()
            query = """INSERT INTO livro (isbn, nome, autor, edicao, quantidade)
            VALUES(%s, %s, %s, %s, %s)"""

            valores = (isbn, nome, autor, edicao, quantidade)
            cursor.execute(query, valores)
            conexao.commit()

            print("Livro adicionado")
        
        except mysql.connector.Error as e:
            print(f"Erro ao cadastrar livro: {e}")
            conexao.rollback()  

        finally:
            cursor.close()

    def editar_livro(id, isbn = None, nome=None, autor=None, edicao=None, quantidade=None, emprestado=None):
        try:
            cursor = conexao.cursor()
            campos_atualizar = []
            dados= []

            if isbn:
                campos_atualizar.append('isbn = %s')
                dados.append(isbn)
            if nome:
                campos_atualizar.append('nome = %s')
                dados.append(nome)
            if autor:
                campos_atualizar.append('autor = %s')
                dados.append(autor)
            if edicao:
                campos_atualizar.append('edicao = %s ')
                dados.append(edicao)
            if quantidade:
                campos_atualizar.append('quantidade = %s')
                dados.append(quantidade)
            if emprestado:
                campos_atualizar.append('emprestado = %s')
                dados.append(emprestado)

            if not campos_atualizar:
                    print("Nenhuma informação fornecida para atualização.")
                    return

            if campos_atualizar:
                    query = f"""UPDATE livro
                        SET {', '.join(campos_atualizar)}
                        WHERE id = %s""" 
                    dados.append(id)
                    cursor.execute(query, dados)
                    conexao.commit()
            
            print("Informações do livro atualizadas com sucesso!")

        except mysql.connector.Error as erro:
                print(f"Erro ao atualizar o livro: {erro}")

        finally:
                cursor.close()

    def excluir_livro(conexao, valor):
        try:
            cursor = conexao.cursor()
            query = f"DELETE FROM livro where id=%s"
            cursor.execute(query, (valor,))
            conexao.commit()

            print(f"Livro com id {valor} foi deletado.")

        except mysql.connector.Error as e:
            print(f"Erro ao deletar livro: {e}")
            conexao.rollback()

        finally:
            cursor.close()

class Emprestimo():
    def __init__(self, data_emprestimo, data_devolucao, id_livro, id_cliente, id_funcionario):
        self.data_emprestimo = datetime
        self.data_devolucao = datetime
        self.id_livro = id_livro
        self.id_cliente = id_cliente
        self.id_funcionario = id_funcionario
        self.status = True

    def realizar_emprestimo(livro, id_cliente, id_funcionario):
        print('emprestimo')

    def realizar_devolucao(livro, id_cliente, id_funcionario):
        print('devolução')

    def calcular_multa():
        print('multa')

    def verificar_limite(cliente):
        print('limite')



#Testes de implementação
cliente1 = Cliente(
    id=1,
    usuario="joao123",
    senha="senha123",
    cpf="12345678901",
    primeiroNome="João",
    sobrenome="Silva",
    emprestimos=0
)

'''Funcionario.cadastrar_cliente(
    conexao=conexao,
    usuario=cliente1.usuario,
    senha=cliente1.senha,
    cpf=cliente1.cpf,
    primeiro_nome=cliente1.primeiroNome,
    sobrenome=cliente1.sobrenome,
    tipo="cliente",
    emprestimos=cliente1.emprestimos
)'''

funcionario1 = Funcionario(
    id=1,
    usuario="ana456",
    senha="senha456",
    cpf="98765432100",
    primeiroNome="Ana",
    sobrenome="Pereira",
    email="ana.pereira@email.com",
    funcao="Gerente"
)

Funcionario.editar_funcionario(id=3, funcionario=funcionario1, email="anapereira@hotmail.com")
Funcionario.editar_cliente(id=6, emprestimos=2)

'''Funcionario.cadastrar_funcionario(
    conexao=conexao,
    usuario=funcionario1.usuario,
    senha=funcionario1.senha,
    cpf=funcionario1.cpf,
    primeiro_nome=funcionario1.primeiroNome,
    sobrenome=funcionario1.sobrenome,
    tipo="funcionario",
    email=funcionario1.email,
    funcao=funcionario1.funcao
)'''

#Funcionario.excluir_cliente(1)

#Livro.adicionar_livro(conexao, "123", "Exemplo de Livro", "Autor X", "1ª Edição", 10)

#Livro.editar_livro(1, emprestado=2 )

#Usuario.listar_usuarios()
#Cliente.ver_livros()

Funcionario.listar_clientes()

conexao.close()
