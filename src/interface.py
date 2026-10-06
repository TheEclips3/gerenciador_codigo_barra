from src.index import (
    calcular_valor_catalogo, cadastrar_produto_com_codigo,
    criar_categorias, criar_codigos_barra, criar_produtos, criar_usuarios,
    delete_categorias, delete_codigos_barra, delete_produtos, delete_usuarios,
    read_categorias, read_codigos_barra, read_produtos, read_usuarios,
    update_categorias, update_codigos_barra, update_produtos, update_usuarios,
    ver_categoria_sem_produto, ver_produtos_cod_bar,
)


def executar_acao(acao, mensagem_sucesso=None):
    try:
        resultado = acao()
        if mensagem_sucesso:
            print(mensagem_sucesso)
        return resultado
    except Exception as erro:
        print(f"Erro na operacao: {erro}")
        return None


def exibir_categorias():
    categorias = executar_acao(read_categorias) or []
    if not categorias:
        print("Nenhuma categoria encontrada.")
    for cat in categorias:
        print(f"ID: {cat['id']} | Nome: {cat['nome']}")


def exibir_usuarios():
    usuarios = executar_acao(read_usuarios) or []
    if not usuarios:
        print("Nenhum usuario encontrado.")
    for user in usuarios:
        print(f"ID: {user['id']} | Nome: {user['nome']} | CNPJ: {user['cnpj']}")


def exibir_produtos(usuario_id=None):
    produtos = executar_acao(lambda: read_produtos(usuario_id)) or []
    if not produtos:
        print("Nenhum produto encontrado.")
    for prod in produtos:
        print(
            f"ID: {prod['id']} | Nome: {prod['nome']} | "
            f"Valor: R${float(prod['valor']):.2f} | Descricao: {prod['descricao']} | "
            f"Usuario ID: {prod['id_usuario']} | Categoria ID: {prod['id_categoria']}"
        )


def exibir_codigos_barra(usuario_id=None):
    codigos = executar_acao(lambda: read_codigos_barra(usuario_id)) or []
    if not codigos:
        print("Nenhum codigo de barra encontrado.")
    for cod in codigos:
        print(
            f"ID: {cod['id']} | Codigo: {cod['codigo']} | "
            f"Tipo: {cod['tipo_cod_barra']} | Produto ID: {cod['id_produto']}"
        )


def exibir_produtos_com_codigos():
    """Funcionalidade 1: consulta a View criada no Supabase."""
    produtos = executar_acao(ver_produtos_cod_bar) or []
    print("\n=== RELATORIO DA VIEW: PRODUTOS COM CODIGOS ===")
    if not produtos:
        print("Nenhum produto com codigo de barra encontrado.")
    for prod in produtos:
        print(
            f"Produto: {prod['produto']} | Categoria: {prod['categoria']} | "
            f"Usuario: {prod['usuario']} | Valor: R${float(prod['valor']):.2f} | "
            f"Codigo: {prod['codigo']} ({prod['tipo_codigo']})"
        )


def exibir_categorias_sem_produtos():
    categorias = executar_acao(ver_categoria_sem_produto) or []
    if not categorias:
        print("Todas as categorias possuem produtos associados.")
    for cat in categorias:
        print(f"Categoria: {cat['nome']}")


def exibir_valor_catalogo():
    """Funcionalidade 2: chama a Function de calculo no Supabase."""
    exibir_usuarios()
    id_usuario = int(input("ID do usuario: "))
    total = executar_acao(lambda: calcular_valor_catalogo(id_usuario))
    if total is not None:
        print(f"Valor total do catalogo: R${total:.2f}")


def cadastro_integrado():
    """Funcionalidade 3: cadastra produto e codigo por meio da Procedure."""
    nome = input("Nome do produto: ")
    desc = input("Descricao do produto: ")
    valor = float(input("Valor do produto: "))
    exibir_usuarios()
    id_usuario = int(input("ID do usuario: "))
    exibir_categorias()
    entrada = input("ID da categoria (Enter para pular): ")
    id_categoria = int(entrada) if entrada else None
    codigo = input("Codigo de barra: ")
    tipo = input("Tipo do codigo (ex: EAN-13, UPC): ")
    produto_id = executar_acao(
        lambda: cadastrar_produto_com_codigo(
            nome, desc, valor, id_usuario, id_categoria, codigo, tipo
        )
    )
    if produto_id:
        print(f"Produto e codigo cadastrados pela Procedure! Produto ID: {produto_id}")


def menu_categorias():
    while True:
        print("\n1. Criar categoria\n2. Listar categorias\n3. Atualizar categoria")
        print("4. Deletar categoria\n5. Categorias sem produtos\n0. Voltar")
        opcao = input("Opcao: ")
        if opcao == "1":
            nome = input("Nome: ")
            resultado = executar_acao(lambda: criar_categorias(nome))
            if resultado:
                print(f"Categoria criada! ID: {resultado}")
        elif opcao == "2":
            exibir_categorias()
        elif opcao == "3":
            exibir_categorias()
            id_cat = int(input("ID: "))
            nome = input("Novo nome: ")
            executar_acao(lambda: update_categorias(nome, id_cat), "Atualizada!")
        elif opcao == "4":
            exibir_categorias()
            id_cat = int(input("ID: "))
            executar_acao(lambda: delete_categorias(id_cat), "Deletada!")
        elif opcao == "5":
            exibir_categorias_sem_produtos()
        elif opcao == "0":
            break
        else:
            print("Opcao invalida!")


def menu_usuarios():
    while True:
        print("\n1. Criar usuario\n2. Listar usuarios\n3. Atualizar usuario")
        print("4. Deletar usuario\n0. Voltar")
        opcao = input("Opcao: ")
        if opcao == "1":
            nome, cnpj = input("Nome: "), input("CNPJ: ")
            resultado = executar_acao(lambda: criar_usuarios(nome, cnpj))
            if resultado:
                print(f"Usuario criado! ID: {resultado}")
        elif opcao == "2":
            exibir_usuarios()
        elif opcao == "3":
            exibir_usuarios()
            id_user = int(input("ID: "))
            nome, cnpj = input("Novo nome: "), input("Novo CNPJ: ")
            executar_acao(lambda: update_usuarios(nome, cnpj, id_user), "Atualizado!")
        elif opcao == "4":
            exibir_usuarios()
            id_user = int(input("ID: "))
            executar_acao(lambda: delete_usuarios(id_user), "Deletado!")
        elif opcao == "0":
            break
        else:
            print("Opcao invalida!")


def ler_dados_produto():
    nome, desc = input("Nome: "), input("Descricao: ")
    valor = float(input("Valor: "))
    exibir_usuarios()
    id_usuario = int(input("ID do usuario: "))
    exibir_categorias()
    entrada = input("ID da categoria (Enter para pular): ")
    return nome, desc, valor, id_usuario, int(entrada) if entrada else None


def menu_produtos():
    while True:
        print("\n1. Criar produto\n2. Cadastro produto + codigo (PROCEDURE)")
        print("3. Listar produtos\n4. Listar por usuario\n5. Atualizar\n6. Deletar")
        print("7. Relatorio produtos/codigos (VIEW)\n8. Total do catalogo (FUNCTION)\n0. Voltar")
        opcao = input("Opcao: ")
        if opcao == "1":
            dados = ler_dados_produto()
            resultado = executar_acao(lambda: criar_produtos(*dados))
            if resultado:
                print(f"Produto criado! ID: {resultado}")
        elif opcao == "2":
            cadastro_integrado()
        elif opcao == "3":
            exibir_produtos()
        elif opcao == "4":
            exibir_usuarios()
            exibir_produtos(int(input("ID do usuario: ")))
        elif opcao == "5":
            exibir_produtos()
            id_prod = int(input("ID: "))
            dados = ler_dados_produto()
            executar_acao(lambda: update_produtos(*dados, id_prod), "Atualizado!")
        elif opcao == "6":
            exibir_produtos()
            id_prod = int(input("ID: "))
            executar_acao(lambda: delete_produtos(id_prod), "Deletado!")
        elif opcao == "7":
            exibir_produtos_com_codigos()
        elif opcao == "8":
            exibir_valor_catalogo()
        elif opcao == "0":
            break
        else:
            print("Opcao invalida!")


def menu_codigos_barra():
    while True:
        print("\n1. Criar codigo\n2. Listar codigos\n3. Listar por usuario")
        print("4. Atualizar codigo\n5. Deletar codigo\n0. Voltar")
        opcao = input("Opcao: ")
        if opcao == "1":
            codigo, tipo = input("Codigo: "), input("Tipo: ")
            exibir_produtos()
            id_produto = int(input("ID do produto: "))
            resultado = executar_acao(lambda: criar_codigos_barra(codigo, tipo, id_produto))
            if resultado:
                print(f"Codigo criado! ID: {resultado}")
        elif opcao == "2":
            exibir_codigos_barra()
        elif opcao == "3":
            exibir_usuarios()
            exibir_codigos_barra(int(input("ID do usuario: ")))
        elif opcao == "4":
            exibir_codigos_barra()
            id_cod = int(input("ID: "))
            codigo, tipo = input("Novo codigo: "), input("Novo tipo: ")
            exibir_produtos()
            id_produto = int(input("Novo ID do produto: "))
            executar_acao(
                lambda: update_codigos_barra(codigo, tipo, id_produto, id_cod),
                "Atualizado!",
            )
        elif opcao == "5":
            exibir_codigos_barra()
            id_cod = int(input("ID: "))
            executar_acao(lambda: delete_codigos_barra(id_cod), "Deletado!")
        elif opcao == "0":
            break
        else:
            print("Opcao invalida!")


def menu_principal():
    print("\n=== GERENCIADOR DE CODIGOS DE BARRA - SUPABASE ===")
    while True:
        print("\n1. Categorias\n2. Usuarios\n3. Produtos e recursos SQL")
        print("4. Codigos de barra\n0. Sair")
        opcao = input("Opcao: ")
        if opcao == "1":
            menu_categorias()
        elif opcao == "2":
            menu_usuarios()
        elif opcao == "3":
            menu_produtos()
        elif opcao == "4":
            menu_codigos_barra()
        elif opcao == "0":
            break
        else:
            print("Opcao invalida!")


if __name__ == "__main__":
    menu_principal()

