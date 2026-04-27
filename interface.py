import psycopg
from index import (
    criar_tabelas,
    criar_categorias, read_categorias, update_categorias, delete_categorias,
    criar_usuarios, read_usuarios, update_usuarios, delete_usuarios,
    criar_produtos, read_produtos, update_produtos, delete_produtos,
    criar_codigos_barra, read_codigos_barra, update_codigos_barra, delete_codigos_barra,
    ver_produtos_cod_bar, ver_categoria_sem_produto
)

conn_info = "dbname=gerenciador_codigos user=postgres password=root host=localhost port=5432"
conn = psycopg.connect(conn_info, autocommit=True)
cur = conn.cursor()

def exibir_categorias():
    """Exibe todas as categorias cadastradas"""
    categorias = read_categorias()
    if categorias:
        print("\n=== CATEGORIAS CADASTRADAS ===")
        for cat in categorias:
            print(f"ID: {cat[0]} | Nome: {cat[1]}")
        print("===============================\n")
    else:
        print("Nenhuma categoria encontrada.\n")

def exibir_usuarios():
    """Exibe todos os usuários cadastrados"""
    usuarios = read_usuarios()
    if usuarios:
        print("\n=== USUÁRIOS CADASTRADOS ===")
        for user in usuarios:
            print(f"ID: {user[0]} | Nome: {user[1]} | CNPJ: {user[2]}")
        print("============================\n")
    else:
        print("Nenhum usuário encontrado.\n")

def exibir_produtos(usuario_id=None):
    """Exibe todos os produtos cadastrados"""
    produtos = read_produtos(usuario_id)
    if produtos:
        print("\n=== PRODUTOS CADASTRADOS ===")
        for prod in produtos:
            print(f"ID: {prod[0]} | Nome: {prod[1]} | Valor: R${prod[2]:.2f} | Descrição: {prod[3]} | Usuário ID: {prod[4]} | Categoria ID: {prod[5]}")
        print("============================\n")
    else:
        print("Nenhum produto encontrado.\n")

def exibir_codigos_barra(usuario_id=None):
    """Exibe todos os códigos de barra cadastrados"""
    codigos = read_codigos_barra(usuario_id)
    if codigos:
        print("\n=== CÓDIGOS DE BARRA CADASTRADOS ===")
        for cod in codigos:
            print(f"ID: {cod[0]} | Código: {cod[1]} | Tipo: {cod[2]} | Produto ID: {cod[3]}")
        print("=====================================\n")
    else:
        print("Nenhum código de barra encontrado.\n")

def exibir_produtos_com_codigos():
    """Exibe produtos com seus códigos de barra"""
    produtos_cod = ver_produtos_cod_bar()
    if produtos_cod:
        print("\n=== PRODUTOS COM CÓDIGOS DE BARRA ===")
        for prod in produtos_cod:
            print(f"Produto: {prod[0]} | Descrição: {prod[1]} | Valor: R${prod[2]:.2f} | Código: {prod[3]}")
        print("======================================\n")
    else:
        print("Nenhum produto com código de barra encontrado.\n")

def exibir_categorias_sem_produtos():
    """Exibe categorias sem produtos associados"""
    categorias = ver_categoria_sem_produto()
    if categorias:
        print("\n=== CATEGORIAS SEM PRODUTOS ===")
        for cat in categorias:
            print(f"Categoria: {cat[0]}")
        print("================================\n")
    else:
        print("Todas as categorias possuem produtos associados.\n")

def menu_categorias():
    """Menu de operações com categorias"""
    while True:
        print("\n=== MENU CATEGORIAS ===")
        print("1. Criar categoria")
        print("2. Listar categorias")
        print("3. Atualizar categoria")
        print("4. Deletar categoria")
        print("5. Listar categorias sem produtos")
        print("0. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome da categoria: ")
            resultado = criar_categorias(nome)
            if resultado:
                print(f"Categoria criada com sucesso! ID: {resultado}")
        elif opcao == "2":
            exibir_categorias()
        elif opcao == "3":
            exibir_categorias()
            id_cat = int(input("ID da categoria a atualizar: "))
            nome = input("Novo nome da categoria: ")
            update_categorias(nome, id_cat)
            print("Categoria atualizada com sucesso!")
        elif opcao == "4":
            exibir_categorias()
            id_cat = int(input("ID da categoria a deletar: "))
            delete_categorias(id_cat)
            print("Categoria deletada com sucesso!")
        elif opcao == "5":
            exibir_categorias_sem_produtos()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_usuarios():
    """Menu de operações com usuários"""
    while True:
        print("\n=== MENU USUÁRIOS ===")
        print("1. Criar usuário")
        print("2. Listar usuários")
        print("3. Atualizar usuário")
        print("4. Deletar usuário")
        print("0. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do usuário: ")
            cnpj = input("CNPJ do usuário: ")
            resultado = criar_usuarios(nome, cnpj)
            if resultado:
                print(f"Usuário criado com sucesso! ID: {resultado}")
        elif opcao == "2":
            exibir_usuarios()
        elif opcao == "3":
            exibir_usuarios()
            id_user = int(input("ID do usuário a atualizar: "))
            nome = input("Novo nome do usuário: ")
            cnpj = input("Novo CNPJ do usuário: ")
            update_usuarios(nome, cnpj, id_user)
            print("Usuário atualizado com sucesso!")
        elif opcao == "4":
            exibir_usuarios()
            id_user = int(input("ID do usuário a deletar: "))
            delete_usuarios(id_user)
            print("Usuário deletado com sucesso!")
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_produtos():
    """Menu de operações com produtos"""
    while True:
        print("\n=== MENU PRODUTOS ===")
        print("1. Criar produto")
        print("2. Listar produtos (todos)")
        print("3. Listar produtos por usuário")
        print("4. Atualizar produto")
        print("5. Deletar produto")
        print("6. Listar produtos com códigos de barra")
        print("0. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do produto: ")
            desc = input("Descrição do produto: ")
            valor = float(input("Valor do produto: "))
            exibir_usuarios()
            id_usuario = int(input("ID do usuário: "))
            exibir_categorias()
            id_categoria_input = input("ID da categoria (opcional, Enter para pular): ")
            id_categoria = int(id_categoria_input) if id_categoria_input else None
            resultado = criar_produtos(nome, desc, valor, id_usuario, id_categoria)
            if resultado:
                print(f"Produto criado com sucesso! ID: {resultado}")
        elif opcao == "2":
            exibir_produtos()
        elif opcao == "3":
            exibir_usuarios()
            id_user = int(input("ID do usuário para filtrar: "))
            exibir_produtos(id_user)
        elif opcao == "4":
            exibir_produtos()
            id_prod = int(input("ID do produto a atualizar: "))
            nome = input("Novo nome do produto: ")
            desc = input("Nova descrição do produto: ")
            valor = float(input("Novo valor do produto: "))
            exibir_usuarios()
            id_usuario = int(input("Novo ID do usuário: "))
            exibir_categorias()
            id_categoria_input = input("Novo ID da categoria (opcional, Enter para pular): ")
            id_categoria = int(id_categoria_input) if id_categoria_input else None
            update_produtos(nome, desc, valor, id_usuario, id_categoria, id_prod)
            print("Produto atualizado com sucesso!")
        elif opcao == "5":
            exibir_produtos()
            id_prod = int(input("ID do produto a deletar: "))
            delete_produtos(id_prod)
            print("Produto deletado com sucesso!")
        elif opcao == "6":
            exibir_produtos_com_codigos()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_codigos_barra():
    """Menu de operações com códigos de barra"""
    while True:
        print("\n=== MENU CÓDIGOS DE BARRA ===")
        print("1. Criar código de barra")
        print("2. Listar códigos de barra (todos)")
        print("3. Listar códigos de barra por usuário")
        print("4. Atualizar código de barra")
        print("5. Deletar código de barra")
        print("0. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            codigo = input("Código de barra: ")
            tipo_cod = input("Tipo do código (ex: EAN-13, UPC): ")
            exibir_produtos()
            id_produto = int(input("ID do produto: "))
            resultado = criar_codigos_barra(codigo, tipo_cod, id_produto)
            if resultado:
                print(f"Código de barra criado com sucesso! ID: {resultado}")
        elif opcao == "2":
            exibir_codigos_barra()
        elif opcao == "3":
            exibir_usuarios()
            id_user = int(input("ID do usuário para filtrar: "))
            exibir_codigos_barra(id_user)
        elif opcao == "4":
            exibir_codigos_barra()
            id_cod = int(input("ID do código de barra a atualizar: "))
            codigo = input("Novo código de barra: ")
            tipo_cod = input("Novo tipo do código: ")
            exibir_produtos()
            id_produto = int(input("Novo ID do produto: "))
            update_codigos_barra(codigo, tipo_cod, id_produto, id_cod)
            print("Código de barra atualizado com sucesso!")
        elif opcao == "5":
            exibir_codigos_barra()
            id_cod = int(input("ID do código de barra a deletar: "))
            delete_codigos_barra(id_cod)
            print("Código de barra deletado com sucesso!")
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_principal():
    """Menu principal do sistema"""
    print("\n" + "="*40)
    print("   GERENCIADOR DE CÓDIGOS DE BARRA")
    print("="*40)

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Gerenciar Categorias")
        print("2. Gerenciar Usuários")
        print("3. Gerenciar Produtos")
        print("4. Gerenciar Códigos de Barra")
        print("5. Criar tabelas no banco")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_categorias()
        elif opcao == "2":
            menu_usuarios()
        elif opcao == "3":
            menu_produtos()
        elif opcao == "4":
            menu_codigos_barra()
        elif opcao == "5":
            print("Criando tabelas no banco de dados...")
            criar_tabelas()
            print("Tabelas criadas com sucesso!")
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()
