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
def delete_categorias(id):
    query = "DELETE FROM categorias WHERE id = %s"
    try:
        # executa o delete
        cur.execute(query,(id,))
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        conn.rollback() # Desfaz em caso de erro se não estiver em autocommit
        return None    
