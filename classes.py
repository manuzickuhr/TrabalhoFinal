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

# Fechar a conexão


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


    def editar_funcionario(): #somente com a funcao gerente
        print('editar funcionario')
    
    def editar_cliente():
        print('editar cliente')

    def excluir_funcionario(): #somente gerente
        print("Excluir funcionario")

    def excluir_cliente():
        print("Excluir cliente")

class Cliente(Usuario):
    def __init__(self, id, usuario, senha, cpf, primeiroNome, sobrenome, emprestimos):
        super().__init__(id, usuario, senha, cpf, primeiroNome, sobrenome)
        self.emprestimos = emprestimos

    def ver_livros():
        print('Ver a lista de todos os livros')
    
    def ver_emprestimos():
        print('Ver os emprestimos linkados aquele cliente')

class Livro():
    def __init__(self, id, isbn, nome, autor, edicao, quantidade):
        self.id = id
        self.isbn = isbn 
        self.nome = nome
        self.autor = autor
        self.edicao = edicao
        self.quantidade = quantidade
        self.emprestado = False

    def adicionar_livro():
        print("Adicionar livro")

    def editar_livro():
        print('Editar livro')

    def excluir_livro():
        print('Excluir livro')

class Emprestimo():
    def __init__(self, data_emprestimo, data_devolucao, id_livro, id_cliente, id_funcionario):
        self.data_emprestimo = datetime
        self.data_devolucao = datetime
        self.id_livro = id_livro
        self.id_cliente = id_cliente
        self.id_funcionario = id_funcionario
        self.status = True

    def realizar_emprestimo(livro, cliente):
        print('emprestimo')

    def realizar_devolucao(livro, cliente):
        print('devolução')

    def calcular_multa():
        print('multa')

    def verificar_limite(cliente):
        print('limite')


# Fechar a conexão
conexao.close()
