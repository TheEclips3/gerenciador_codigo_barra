import json
import os
from functools import wraps

import redis
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

# Redis e opcional: se estiver indisponivel, a aplicacao continua usando o Supabase.
CACHE_PREFIX = "gerenciador_codigos:"
CACHE_TTL = int(os.getenv("REDIS_CACHE_TTL", "300"))
_redis = None

redis_host = os.getenv("REDIS_HOST")
if redis_host:
    try:
        _redis = redis.Redis(
            host=redis_host,
            port=int(os.getenv("REDIS_PORT", "6379")),
            decode_responses=True,
            username=os.getenv("REDIS_USERNAME", "default"),
            password=os.getenv("REDIS_PASSWORD", ""),
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        _redis.ping()
    except (redis.RedisError, ValueError):
        _redis = None


def _chave_cache(chave: str) -> str:
    return f"{CACHE_PREFIX}{chave}"


def _consultar_com_cache(chave: str, consulta, ttl: int = CACHE_TTL):
    """Cache-aside: tenta Redis, consulta Supabase em caso de miss/falha."""
    chave_completa = _chave_cache(chave)
    if _redis is not None:
        try:
            armazenado = _redis.get(chave_completa)
            if armazenado is not None:
                return json.loads(armazenado)
        except (redis.RedisError, json.JSONDecodeError):
            pass

    resultado = consulta()
    if _redis is not None:
        try:
            _redis.setex(chave_completa, ttl, json.dumps(resultado, ensure_ascii=False, default=str))
        except redis.RedisError:
            pass
    return resultado


def _invalidar_cache():
    """Remove somente chaves deste projeto, sem limpar o Redis de outros sistemas."""
    if _redis is None:
        return
    try:
        chaves = list(_redis.scan_iter(match=f"{CACHE_PREFIX}*", count=100))
        if chaves:
            _redis.delete(*chaves)
    except redis.RedisError:
        pass


def _invalidar_apos_mutacao(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        resultado = funcao(*args, **kwargs)
        _invalidar_cache()
        return resultado
    return wrapper


def _dados(resposta):
    return resposta.data or []


# categorias
@_invalidar_apos_mutacao
def criar_categorias(nome: str):
    dados = _dados(supabase.table("categorias").insert({"nome": nome}).execute())
    return dados[0]["id"] if dados else None


def read_categorias():
    return _consultar_com_cache(
        "categorias:todos",
        lambda: _dados(supabase.table("categorias").select("*").order("id").execute()),
    )


@_invalidar_apos_mutacao
def update_categorias(nome: str, id: int):
    supabase.table("categorias").update({"nome": nome}).eq("id", id).execute()


@_invalidar_apos_mutacao
def delete_categorias(id: int):
    supabase.table("categorias").delete().eq("id", id).execute()


# usuarios
@_invalidar_apos_mutacao
def criar_usuarios(nome: str, cnpj: str):
    dados = _dados(
        supabase.table("usuarios").insert({"nome": nome, "cnpj": cnpj}).execute()
    )
    return dados[0]["id"] if dados else None


def read_usuarios():
    return _consultar_com_cache(
        "usuarios:todos",
        lambda: _dados(supabase.table("usuarios").select("*").order("id").execute()),
    )


@_invalidar_apos_mutacao
def update_usuarios(nome: str, cnpj: str, id: int):
    supabase.table("usuarios").update({"nome": nome, "cnpj": cnpj}).eq(
        "id", id
    ).execute()


@_invalidar_apos_mutacao
def delete_usuarios(id: int):
    supabase.table("usuarios").delete().eq("id", id).execute()


# codigos de barra
@_invalidar_apos_mutacao
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
    chave = f"codigos_barra:usuario:{usuario_id}" if usuario_id is not None else "codigos_barra:todos"

    def consulta():
        if usuario_id is not None:
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

    return _consultar_com_cache(chave, consulta)

@_invalidar_apos_mutacao
def update_codigos_barra(cod: str, tipo_cod: str, id_produto: int, id: int):
    supabase.table("codigos_barra").update(
        {"codigo": cod, "tipo_cod_barra": tipo_cod, "id_produto": id_produto}
    ).eq("id", id).execute()


@_invalidar_apos_mutacao
def delete_codigos_barra(id: int):
    supabase.table("codigos_barra").delete().eq("id", id).execute()


# produtos
@_invalidar_apos_mutacao
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
    chave = f"produtos:usuario:{usuario_id}" if usuario_id is not None else "produtos:todos"

    def consulta():
        query = supabase.table("produtos").select("*")
        if usuario_id is not None:
            query = query.eq("id_usuario", usuario_id)
        return _dados(query.order("id").execute())

    return _consultar_com_cache(chave, consulta)


@_invalidar_apos_mutacao
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


@_invalidar_apos_mutacao
def delete_produtos(id: int):
    supabase.table("produtos").delete().eq("id", id).execute()


# VIEW: relatorio pronto com dados de quatro tabelas
def ver_produtos_cod_bar():
    def consulta():
        resposta = (
            supabase.table("vw_produtos_codigos")
            .select("*")
            .order("produto_id")
            .execute()
        )
        return _dados(resposta)

    return _consultar_com_cache("view:produtos_codigos", consulta)


def ver_categoria_sem_produto():
    def consulta():
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

    return _consultar_com_cache("categorias:sem_produtos", consulta)


# FUNCTION: calcula no banco o valor total do catalogo de um usuario
def calcular_valor_catalogo(id_usuario: int):
    def consulta():
        resposta = supabase.rpc(
            "calcular_valor_catalogo", {"p_id_usuario": id_usuario}
        ).execute()
        return float(resposta.data or 0)

    return _consultar_com_cache(f"catalogo:usuario:{id_usuario}", consulta)


# PROCEDURE: este RPC adaptador executa a Procedure no banco
@_invalidar_apos_mutacao
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
