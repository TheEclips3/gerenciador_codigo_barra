import os

from dotenv import load_dotenv
from supabase import Client, create_client


load_dotenv()


def conectar_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    chave = os.getenv("SUPABASE_KEY")
    if not url or not chave:
        raise RuntimeError(
            "Configure SUPABASE_URL e SUPABASE_KEY no arquivo .env. "
            "Use .env.example como modelo."
        )
    return create_client(url, chave)


supabase = conectar_supabase()


def _dados(resposta):
    return resposta.data or []


# categorias
def criar_categorias(nome: str):
    dados = _dados(supabase.table("categorias").insert({"nome": nome}).execute())
    return dados[0]["id"] if dados else None


def read_categorias():
    return _dados(supabase.table("categorias").select("*").order("id").execute())


def update_categorias(nome: str, id: int):
    supabase.table("categorias").update({"nome": nome}).eq("id", id).execute()


def delete_categorias(id: int):
    supabase.table("categorias").delete().eq("id", id).execute()


# usuarios
def criar_usuarios(nome: str, cnpj: str):
    dados = _dados(
        supabase.table("usuarios").insert({"nome": nome, "cnpj": cnpj}).execute()
    )
    return dados[0]["id"] if dados else None


def read_usuarios():
    return _dados(supabase.table("usuarios").select("*").order("id").execute())


def update_usuarios(nome: str, cnpj: str, id: int):
    supabase.table("usuarios").update({"nome": nome, "cnpj": cnpj}).eq(
        "id", id
    ).execute()


def delete_usuarios(id: int):
    supabase.table("usuarios").delete().eq("id", id).execute()


# codigos de barra
def criar_codigos_barra(cod: str, tipo_cod: str, id_produto: int):
    dados = _dados(
        supabase.table("codigos_barra")
        .insert(
            {"codigo": cod, "tipo_cod_barra": tipo_cod, "id_produto": id_produto}
        )
        .execute()
    )
    return dados[0]["id"] if dados else None


def read_codigos_barra(usuario_id=None):
    if usuario_id:
        produtos = supabase.table("produtos").select("id").eq(
            "id_usuario", usuario_id
        ).execute()
        ids_produtos = [produto["id"] for produto in _dados(produtos)]
        if not ids_produtos:
            return []
        resposta = (
            supabase.table("codigos_barra")
            .select("*")
            .in_("id_produto", ids_produtos)
            .order("id")
            .execute()
        )
    else:
        resposta = supabase.table("codigos_barra").select("*").order("id").execute()
    return _dados(resposta)


def update_codigos_barra(cod: str, tipo_cod: str, id_produto: int, id: int):
    supabase.table("codigos_barra").update(
        {"codigo": cod, "tipo_cod_barra": tipo_cod, "id_produto": id_produto}
    ).eq("id", id).execute()


def delete_codigos_barra(id: int):
    supabase.table("codigos_barra").delete().eq("id", id).execute()


# produtos
def criar_produtos(nome: str, desc: str, valor: float, id_usuario: int, id_categoria):
    dados = _dados(
        supabase.table("produtos")
        .insert(
            {
                "nome": nome,
                "valor": valor,
                "descricao": desc,
                "id_usuario": id_usuario,
                "id_categoria": id_categoria,
            }
        )
        .execute()
    )
    return dados[0]["id"] if dados else None


def read_produtos(usuario_id=None):
    consulta = supabase.table("produtos").select("*")
    if usuario_id:
        consulta = consulta.eq("id_usuario", usuario_id)
    return _dados(consulta.order("id").execute())


def update_produtos(nome: str, desc: str, valor: float, id_usuario: int, id_categoria, id: int):
    supabase.table("produtos").update(
        {
            "nome": nome,
            "descricao": desc,
            "valor": valor,
            "id_usuario": id_usuario,
            "id_categoria": id_categoria,
        }
    ).eq("id", id).execute()


def delete_produtos(id: int):
    supabase.table("produtos").delete().eq("id", id).execute()


# VIEW: relatorio pronto com dados de quatro tabelas
def ver_produtos_cod_bar():
    resposta = (
        supabase.table("vw_produtos_codigos")
        .select("*")
        .order("produto_id")
        .execute()
    )
    return _dados(resposta)


def ver_categoria_sem_produto():
    produtos = supabase.table("produtos").select("id_categoria").execute()
    categorias_usadas = {
        produto["id_categoria"]
        for produto in _dados(produtos)
        if produto["id_categoria"] is not None
    }
    categorias = supabase.table("categorias").select("*").order("nome").execute()
    return [
        categoria
        for categoria in _dados(categorias)
        if categoria["id"] not in categorias_usadas
    ]


# FUNCTION: calcula no banco o valor total do catalogo de um usuario
def calcular_valor_catalogo(id_usuario: int):
    resposta = supabase.rpc(
        "calcular_valor_catalogo", {"p_id_usuario": id_usuario}
    ).execute()
    return float(resposta.data or 0)


# PROCEDURE: este RPC adaptador executa a Procedure no banco
def cadastrar_produto_com_codigo(
    nome: str,
    desc: str,
    valor: float,
    id_usuario: int,
    id_categoria,
    codigo: str,
    tipo_cod: str,
):
    resposta = supabase.rpc(
        "cadastrar_produto_com_codigo",
        {
            "p_nome": nome,
            "p_descricao": desc,
            "p_valor": valor,
            "p_id_usuario": id_usuario,
            "p_id_categoria": id_categoria,
            "p_codigo": codigo,
            "p_tipo_cod_barra": tipo_cod,
        },
    ).execute()
    return resposta.data
