from datetime import datetime, timedelta
import mysql.connector

conexao = mysql.connector.connect(
    host = 'localhost' ,
    user = 'root' ,
    password = 'root',
    database = 'trabalhoFinal',
)

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

#No bd fazer 1 tabela usuario com o atributo tipo

class Funcionario(Usuario):
    def __init__(self, id, usuario, senha, cpf, primeiroNome, sobrenome, email, funcao):
        super().__init__(id, usuario, senha,cpf, primeiroNome, sobrenome)
        self.email = email
        self.funcao = funcao

    def cadastrar_funcionario():
        print('cadastro funcionario')

    
    def cadastar_cliente():
        print('cadastro clientes')

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
        self.emprestimos = []

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
