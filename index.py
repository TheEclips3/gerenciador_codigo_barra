import psycopg

# 1. Configuramos a conexão de forma global ou persistente
conn_info = "dbname=gerenciador_codigos user=postgres password=root host=localhost port=5432"

# Abrimos a conexão (idealmente você faria isso ao iniciar o app)
conn = psycopg.connect(conn_info, autocommit=True)

# 2. Criamos a variável do cursor
cur = conn.cursor()

def criar_categorias(nome: str):
    query = "INSERT INTO categorias (nome) VALUES (%s) RETURNING id;"
    
    try:
        # Usando a variável 'cur' definida lá fora
        cur.execute(query, (nome,))
        
        # Pega o ID retornado
        id_gerado = cur.fetchone()[0]
        return id_gerado
    except Exception as e:
        print(f"Erro ao inserir categoria: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None
def read_categorias():
    try:
        # executa o select
        cur.execute("SELECT * FROM categorias")
        usuarios = cur.fetchall()
        return usuarios
    except Exception as e:
        print(f"Erro ao ler categoria: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None
def update_categorias(nome:str,id:int):
    query = "UPDATE categorias SET nome = %s WHERE id = %s"
    try:
        # executa o update
        cur.execute(query,(nome,id,))
    except Exception as e:
        print(f"Erro ao dar update em categoria: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None    
def delete_categorias(id:int):
    query = "DELETE FROM categorias WHERE id = %s"
    try:
        # executa o delete
        cur.execute(query,(id,))
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None    

def criar_usarios(nome,cnpj: str,id_produto,id_codigo: int):
    query = "INSERT INTO usuarios (nome, cnpj, id_produto, id_codigo) VALUES (%s, %s, %s, %s) RETURNING id;"
    
    try:
        # Usando a variável 'cur' definida lá fora
        cur.execute(query, (nome, cnpj, id_produto, id_codigo))
        
        # Pega o ID retornado
        id_gerado = cur.fetchone()[0]
        return id_gerado
    except Exception as e:
        print(f"Erro ao inserir usuario: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None 
def read_usuarios():
    try:
        # executa o select
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
        return usuarios
    except Exception as e:
        print(f"Erro ao ler usuario: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None  
def update_usuarios(nome,cnpj: str,id_produto,id_codigo,id: int):
    query = """UPDATE usuarios 
    SET nome = %s,
        cnpj = %s,
        id_produto = %s,
        id_codigo = %s 
    WHERE id = %s
    """
    try:
        # executa o update
        cur.execute(query,(nome,cnpj,id_produto,id_codigo,id,))
    except Exception as e:
        print(f"Erro ao dar update em usuarios: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None    
def delete_usuarios(id: int):
    query = "DELETE FROM usuarios WHERE id = %s"
    try:
        # executa o delete
        cur.execute(query,(id,))
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None    

def criar_codigos_barra(cod,tipo_cod: str,id_usuario,id_produto: int):
    query = "INSERT INTO codigos_barra (codigo,tipo_cod_barra,id_usuario,id_produto) VALUES (%s, %s, %s, %s) RETURNING id;"
    
    try:
        # Usando a variável 'cur' definida lá fora
        cur.execute(query, (cod, tipo_cod, id_usuario, id_produto))
        
        # Pega o ID retornado
        id_gerado = cur.fetchone()[0]
        return id_gerado
    except Exception as e:
        print(f"Erro ao inserir usuario: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None   
def read_codigos_barra():
    try:
        # executa o select
        cur.execute("SELECT * FROM codigos_barra")
        usuarios = cur.fetchall()
        return usuarios
    except Exception as e:
        print(f"Erro ao ler categoria: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None  
def update_codigos_barra(cod,tipo_cod: str,id_usuario,id_produto,id: int):
    query = """UPDATE codigos_barra
    SET codigo = %s,
        tipo_cod_barra = %s,
        id_usuario = %s,
        id_produto = %s 
    WHERE id = %s
    """
    try:
        # executa o update
        cur.execute(query,(cod,tipo_cod,id_usuario,id_produto,id,))
    except Exception as e:
        print(f"Erro ao dar update em codigo de barra: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None    
def delete_codigos_barra(id: int):
    query = "DELETE FROM codigos_barra WHERE id = %s"
    try:
        # executa o delete
        cur.execute(query,(id,))
    except Exception as e:
        print(f"Erro ao deletar codigo de barras: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None    

def criar_produtos(nome,desc: str,valor: float,id_usario,id_codigo,id_categoria:int):
    query = "INSERT INTO produtos (nome,valor,descricao,id_usuarios,id_codigo,id_categoria) VALUES (%s, %s, %s, %s, %s,%s) RETURNING id;"
    
    try:
        # Usando a variável 'cur' definida lá fora
        cur.execute(query, (nome, valor, desc,id_usario,id_codigo,id_categoria,))
        
        # Pega o ID retornado
        id_gerado = cur.fetchone()[0]
        return id_gerado
    except Exception as e:
        print(f"Erro ao inserir usuario: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None   