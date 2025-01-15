from datetime import datetime, timedelta
import mysql.connector
from classes import *

conexao = mysql.connector.connect(
    host = 'localhost' ,
    user = 'root' ,
    password = 'root',
    database = 'trabalhoFinal',
)

# if conexao.is_connected():
#     print("Conexão realizada com sucesso!")
# else:
#     print("Erro ao conectar ao banco de dados.")


usuarios = []
livros = []
emprestimos = []



def sistema_login():
    print("Bem-vindo ao sistema de login!")
    cursor = conexao.cursor()

    tentativas = 3
    while tentativas > 0:
        usuario = input("Usuário: ")
        senha = input("Senha: ")
        try:
            cursor = conexao.cursor()
            query = "SELECT senha, tipo, id FROM USUARIO WHERE usuario = %s"
            cursor.execute(query, (usuario,))
            informacoes = cursor.fetchone()  # Use fetchone() para obter apenas um registro.

            if informacoes:
                global id_usuario
                senha_correta, tipo_usuario, id_usuario = informacoes
                if senha == senha_correta:
                    print(f"Bem-vindo, {usuario}!")
                    if tipo_usuario.lower() == "funcionario":
                        menu_funcionario()
                    elif tipo_usuario.lower() == "cliente":
                        menu_cliente()
                    return  # Encerrar o login ao acessar o menu.
                else:
                    print("Senha incorreta. Tente novamente.")
            else:
                print("Usuário não encontrado.")

            tentativas -= 1
            print(f"Você ainda tem {tentativas} tentativa(s).")
        except mysql.connector.Error as e:
            print(f"Erro ao fazer login: {e}")
            conexao.rollback()
        finally:
            if 'cursor' in locals():  # Verifica se o cursor foi inicializado
                cursor.close()  
    print("Número de tentativas excedido. Encerrando o sistema.")
    return False


def menu_funcionario():
    while True:
        print("\nMenu Funcionário: ")
        print("1 - Sair")
        print("2 - Clientes")
        print("3 - Livros")
        print("4 - Empréstimos")
        
        escolha_principal = int(input("Digite o número da opção desejada: "))

        if escolha_principal == 1:
            print("Saindo do sistema.")
            break
        elif escolha_principal == 2:
            menu_clientes()
        elif escolha_principal == 3:
            menu_livros()
        elif escolha_principal == 4:
            menu_emprestimos()
        else:
            print("Opção inválida. Tente novamente.")

def menu_clientes():
    while True:
        print("\nEdição de Clientes:")
        print("1 - Voltar")
        print("2 - Cadastrar cliente")
        print("3 - Editar cliente")
        print("4 - Deletar cliente")
        print("5 - Listar cliente")
        escolha_usuarios = int(input("Digite o número da opção desejada: "))

        if escolha_usuarios == 1:
            print("Voltando ao menu inicial.")
            menu_funcionario()
        elif escolha_usuarios == 2:
            print("Preencha as informações abaixo para realizar o cadastro: ")
            usuario = input("Informe o nome de usuário para ser utilizado: ")
            senha = input("Infomre a senha que será utilizada: ")
            while True:
                    try:
                        cpf = input('Digite o CPF: ')
                        verificar_cpf(cpf)  # Verifica se o CPF é válido
                        print("CPF válido!")  # Se o CPF for válido, sai do laço
                        break  # Encerra o laço e segue para o restante do cadastro
                    except ValueError as e:
                        print(f"Erro: {e}. Tente novamente.")

            primeiro_nome = input("Informe o primeiro nome do cliente: ")
            sobrenome = input("Informe o sobrenome do cliente: ")
            Funcionario.cadastrar_cliente(usuario, senha, cpf, primeiro_nome, sobrenome,0)
        elif escolha_usuarios == 3:
            cursor = conexao.cursor()
            cpf = input("Informe o cpf do cliente que deseja alterar suas informações: ")
            try: 
                query = "SELECT u.id FROM USUARIO u WHERE cpf = %s"
                cursor.execute(query, (cpf,))
                id = cursor.fetchone()
                print("Cliente encontrado! ")
                print("Preencha as informações abaixo que deseja alterar (caso não seja alterada aperte a tecla ENTER, pulando aquele dado): ")
                usuario = input("Informe o novo nome de usuário para ser utilizado: ")
                vazio(usuario)
                senha = input("Infomre a nova senha que será utilizada: ")
                vazio(senha)
                cpf = input("Informe o novo cpf do cliente: ")
                vazio(cpf)
                # if cpf != None:
                #     while True:
                #         try:
                #             cpf = input('Digite o CPF: ')
                #             verificar_cpf(cpf)  # Verifica se o CPF é válido
                #             print("CPF válido!")  # Se o CPF for válido, sai do laço
                #             break  # Encerra o laço e segue para o restante do cadastro
                #         except ValueError as e:
                #             print(f"Erro: {e}. Tente novamente.")
                primeiro_nome = input("Informe o novo primeiro nome do cliente: ")
                vazio(primeiro_nome)
                sobrenome = input("Informe o novo sobrenome do cliente: ")
                vazio(sobrenome)
                Funcionario.editar_cliente(id, usuario, senha, cpf, primeiro_nome, sobrenome)
            except mysql.connector.Error as e:
                print(f"Erro ao fazer login: {e}")
                conexao.rollback()
            finally:
                cursor.close()
        elif escolha_usuarios == 4:
            cursor = conexao.cursor()
            cpf = input("Informe o cpf do cliente que deseja alterar suas informações: ")
            try: 
                query = "SELECT u.id FROM USUARIO u WHERE cpf = %s"
                cursor.execute(query, (cpf,))
                id = cursor.fetchone()
                verificar = input("Você tem certeza que deseja excluir esse cliente?(sim/nao): ")
                if verificar.lower() == ("sim"):
                    Funcionario.excluir_cliente(id)
                elif verificar.lower() == "nao":
                    menu_clientes()
            except mysql.connector.Error as e:
                print(f"Erro ao fazer login: {e}")
                conexao.rollback()
            finally:
                cursor.close()
        elif escolha_usuarios == 5:
            Funcionario.listar_clientes()
        else:
            print("Opção inválida. Tente novamente.")

def menu_livros():
    while True:
        print("\nMenu Livros:")
        print("1 - Voltar")
        print("2 - Cadastrar Livro")
        print("3 - Editar Livro")
        print("4 - Deletar Livro")
        print("5 - Listar Livros")
        escolha_livros = int(input("Digite o número da opção desejada: "))

        if escolha_livros == 1:
            menu_funcionario()
        elif escolha_livros == 2:
            print("Preencha as informações abaixo para adicionar o livro: ")
            isbn = input("Informe o ISBN do livro: ")
            nome = input("Informe o nome do livro: ")
            autor = input("Informe o autor do livro: ")
            edicao = input("Informe a edicao do livro: ")
            quantidade = input("Informe a quantidade de livros: ")
            Livro.adicionar_livro(isbn, nome, autor, edicao, quantidade)
        elif escolha_livros == 3:
            cursor = conexao.cursor()

            id = input("Informe o ID cadastrado do livro que deseja editar: ")
            try: 
                query = "SELECT id FROM LIVRO WHERE id = %s"
                cursor.execute(query, (id,))
                id = cursor.fetchone()

                if id:
                    print("Livro encontrado! ")
                    print("Preencha as informações abaixo que deseja alterar (caso não seja alterada aperte a tecla ENTER, pulando aquele dado): ")
                    isbn = input("Informe o novo ISBN do livro: ")
                    vazio(isbn)
                    nome = input("Infomre o novo nome que será utilizada: ")
                    vazio(nome)
                    autor = input("Informe o novo autor do livro: ")
                    vazio(autor)
                    edicao = input("Informe o nova edicao do livro: ")
                    vazio(edicao)
                    quantidade = input("Informe a nova quantidade de livros: ")
                    vazio(quantidade)
                    Livro.editar_livro(id,isbn, nome, autor, edicao, quantidade)
            except mysql.connector.Error as e:
                print(f"Erro ao fazer login: {e}")
                conexao.rollback()
            finally:
                cursor.close()
        elif escolha_livros == 4:
            input("Informe o ID do livro que deseja deletar: ")
            Livro.excluir_livro()
        elif escolha_livros == 5:
            Cliente.ver_livros()
        else:
            print("Opção inválida. Tente novamente.")

def menu_emprestimos():
    while True:
        print("\nMenu Empréstimos:")
        print("1 - Voltar")
        print("2 - Realizar Empréstimo")
        print("3 - Devolver Livro")
        escolha_emprestimos = int(input("Digite o número da opção desejada: "))

        if escolha_emprestimos == 1:
            print("Voltando ao menu anterior: ")
            menu_funcionario()
        elif escolha_emprestimos == 2:
            livro = input("Informe o ID do livro que será emprestado: ")
            cliente = input("Informe o ID do cliente que irá pegar o livro: ")
            funcionario = input("Informe o ID do funcionário que auxiliou no empréstimo: ")
            emprestimo1 = Emprestimo(livro,cliente,funcionario)
            emprestimo1.realizar_emprestimo()
        elif escolha_emprestimos == 3:
            try:
                cursor = conexao.cursor()
                cpf = input("Digite o cpf do cliente que está devolvendo o livro: ")
                id_livro = input("Digite o ID do livro que será devolvido: ")

                query_id_cliente = "SELECT id FROM cliente WHERE cpf = %s"
                cursor.execute(query_id_cliente, (cpf,))
                id_cliente = cursor.fetchone()

                query_id_emprestimo = "SELECT id FROM cliente WHERE id_livro = %s and id_cliente = %s"
                cursor.execute(query_id_emprestimo, (id_livro,id_cliente,))
                id_emprestimo = cursor.fetchone()

                conexao.commit()

                Emprestimo.realizar_devolucao(id_emprestimo)
            except mysql.connector.Error as erro:
                print(f"Erro ao realizar devolução: {erro}")

            finally:
                cursor.close()
        else:
            print("Opção inválida. Tente novamente.")

def menu_cliente():
    while True:
        print("\nMenu Cliente:")
        print("1 - Sair")
        print("2 - Ver livros")
        print("3 - Ver emprestimos")
        print("4 - Calcular multas")
        print("5 - Pagar multa")
        escolha_cliente = int(input("Digite o número da opção desejada: "))

        if escolha_cliente == 1:
            print("Saindo do sistema. ")
            break
        elif escolha_cliente == 2:
            Cliente.ver_livros()
        elif escolha_cliente == 3:
            Cliente.ver_emprestimos(id_usuario)
        elif escolha_cliente == 4:
            Emprestimo.calcular_multa(id_usuario)
            Cliente.ver_multas(id_usuario)
        elif escolha_cliente == 4:
            id_multa = input("Informe o ID da multa que deseja pagar: ")
            Cliente.pagar_multa(id_multa)
        else:
            print("Opção inválida. Tente novamente.")


def vazio(dado):
    if dado == "":
        dado = None

def verificar_cpf(cpf):

    if len(cpf) == 11 and cpf.isdigit():  

        if cpf == cpf[0] * 11:
            return False
        else:
            soma = 0
            mult = 10

            for digito in cpf[:9]: 
                soma += int(digito) * mult
                mult -= 1

            if soma % 11 >= 2:
                d1 = 11 - (soma % 11)
            else:
                d1 = 0

            soma = 0
            mult = 11

            for digito in cpf[:10]:  
                soma += int(digito) * mult
                mult -= 1

            if soma % 11 >= 2:
                d2 = 11 - (soma % 11)
            else:
                d2 = 0

            # Verifica se os dígitos calculados correspondem aos fornecidos
            if int(cpf[9]) == d1 and int(cpf[10]) == d2:
                return True
            else:
                raise ValueError("CPF inválido.")
    else:
        raise ValueError("CPF deve ter 11 dígitos numéricos.")

sistema_login()
