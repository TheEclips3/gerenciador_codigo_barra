import psycopg

conn_info = "dbname=gerenciador_codigos user=postgres password=root host=localhost port=5432"
conn = psycopg.connect(conn_info, autocommit=True)
cur = conn.cursor()

def criar_tabelas():
    query = """
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(14) NOT NULL
);

CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor FLOAT NOT NULL,
    descricao VARCHAR(400),
    id_usuario INT NOT NULL REFERENCES usuarios(id),
    id_categoria INT REFERENCES categorias(id)
);

CREATE TABLE codigos_barra (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(128) NOT NULL,
    tipo_cod_barra VARCHAR(50),
    id_produto INT NOT NULL UNIQUE REFERENCES produtos(id)
);
"""
    try:
        cur.execute(query)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
#categorias
def criar_categorias(nome: str):
    query = "INSERT INTO categorias (nome) VALUES (%s) RETURNING id;"
    try:
        cur.execute(query, (nome,))
        return cur.fetchone()[0]
    except Exception as e:
        print(f"Erro ao inserir categoria: {e}")
        return None
def read_categorias():
    try:
        cur.execute("SELECT * FROM categorias")
        return cur.fetchall()
    except Exception as e:
        print(f"Erro ao ler categoria: {e}")
        return None
def update_categorias(nome: str, id: int):
    query = "UPDATE categorias SET nome = %s WHERE id = %s"
    try:
        cur.execute(query, (nome, id))
    except Exception as e:
        print(f"Erro ao dar update em categoria: {e}")
def delete_categorias(id: int):
    query = "DELETE FROM categorias WHERE id = %s"
    try:
        cur.execute(query, (id,))
    except Exception as e:
        print(f"Erro ao deletar categoria: {e}")
#usuario
def criar_usuarios(nome: str, cnpj: str):
    query = "INSERT INTO usuarios (nome, cnpj) VALUES (%s, %s) RETURNING id;"
    try:
        cur.execute(query, (nome, cnpj))
        return cur.fetchone()[0]
    except Exception as e:
        print(f"Erro ao inserir usuario: {e}")
        return None
def read_usuarios():
    try:
        cur.execute("SELECT * FROM usuarios")
        return cur.fetchall()
    except Exception as e:
        print(f"Erro ao ler usuario: {e}")
        return None
def update_usuarios(nome: str, cnpj: str, id: int):
    query = """UPDATE usuarios 
    SET nome = %s,
        cnpj = %s
    WHERE id = %s
    """
    try:
        cur.execute(query, (nome, cnpj, id))
    except Exception as e:
        print(f"Erro ao dar update em usuario: {e}")
def delete_usuarios(id: int):
    query = "DELETE FROM usuarios WHERE id = %s"
    try:
        cur.execute(query, (id,))
    except Exception as e:
        print(f"Erro ao deletar usuario: {e}")
#codigos de barra
def criar_codigos_barra(cod: str, tipo_cod: str, id_produto: int):
    query = "INSERT INTO codigos_barra (codigo, tipo_cod_barra, id_produto) VALUES (%s, %s, %s) RETURNING id;"
    try:
        cur.execute(query, (cod, tipo_cod, id_produto))
        return cur.fetchone()[0]
    except Exception as e:
        print(f"Erro ao inserir codigo de barras: {e}")
        return None
def read_codigos_barra(usuario_id=None):
    try:
        if usuario_id:
            query = """
                SELECT cb.* FROM codigos_barra cb
                INNER JOIN produtos p ON cb.id_produto = p.id
                WHERE p.id_usuario = %s
            """
            cur.execute(query, (usuario_id,))
        else:
            cur.execute("SELECT * FROM codigos_barra")
        return cur.fetchall()
    except Exception as e:
        print(f"Erro ao ler codigos de barra: {e}")
        return None
def update_codigos_barra(cod: str, tipo_cod: str, id_produto: int, id: int):
    query = """UPDATE codigos_barra
    SET codigo = %s,
        tipo_cod_barra = %s,
        id_produto = %s
    WHERE id = %s
    """
    try:
        cur.execute(query, (cod, tipo_cod, id_produto, id))
    except Exception as e:
        print(f"Erro ao dar update em codigo de barra: {e}")
def delete_codigos_barra(id: int):
    query = "DELETE FROM codigos_barra WHERE id = %s"
    try:
        cur.execute(query, (id,))
    except Exception as e:
        print(f"Erro ao deletar codigo de barras: {e}")
#produtos
def criar_produtos(nome: str, desc: str, valor: float, id_usuario: int, id_categoria: int):
    query = "INSERT INTO produtos (nome, valor, descricao, id_usuario, id_categoria) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
    try:
        cur.execute(query, (nome, valor, desc, id_usuario, id_categoria))
        return cur.fetchone()[0]
    except Exception as e:
        print(f"Erro ao inserir produto: {e}")
        return None
def read_produtos(usuario_id=None):
    try:
        if usuario_id:
            query = "SELECT * FROM produtos WHERE id_usuario = %s"
            cur.execute(query, (usuario_id,))
        else:
            cur.execute("SELECT * FROM produtos")
        return cur.fetchall()
    except Exception as e:
        print(f"Erro ao ler produto: {e}")
        return None
def update_produtos(nome: str, desc: str, valor: float, id_usuario: int, id_categoria: int, id: int):
    query = """UPDATE produtos
    SET nome = %s,
        descricao = %s,
        valor = %s,
        id_usuario = %s,
        id_categoria = %s
    WHERE id = %s
    """
    try:
        cur.execute(query, (nome, desc, valor, id_usuario, id_categoria, id))
    except Exception as e:
        print(f"Erro ao dar update em produto: {e}")
def delete_produtos(id: int):
    query = "DELETE FROM produtos WHERE id = %s"
    try:
        cur.execute(query, (id,))
    except Exception as e:
        print(f"Erro ao deletar produto: {e}")

def ver_produtos_cod_bar():
    query = """
        SELECT p.nome, p.descricao, p.valor, cb.codigo
        FROM produtos p
        INNER JOIN codigos_barra cb ON cb.id_produto = p.id
    """
    try:
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        print(f"Erro ao ler produto: {e}")
        return None
def ver_categoria_sem_produto():
    query = """
        SELECT categorias.nome
        FROM categorias
        LEFT JOIN produtos ON categorias.id = produtos.id_categoria
        WHERE produtos.id_categoria IS NULL
    """
    try:
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        print(f"Erro ao ler categoria: {e}")
        return None