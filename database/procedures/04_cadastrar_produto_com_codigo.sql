create or replace procedure public.sp_cadastrar_produto_com_codigo(
    in p_nome varchar,
    in p_descricao varchar,
    in p_valor numeric,
    in p_id_usuario bigint,
    in p_id_categoria bigint,
    in p_codigo varchar,
    in p_tipo_cod_barra varchar,
    inout p_produto_id bigint default null
)
language plpgsql
security invoker
set search_path = ''
as $$
begin
    insert into public.produtos (
        nome, descricao, valor, id_usuario, id_categoria
    ) values (
        p_nome, p_descricao, p_valor, p_id_usuario, p_id_categoria
    ) returning id into p_produto_id;

    insert into public.codigos_barra (
        codigo, tipo_cod_barra, id_produto
    ) values (
        p_codigo, p_tipo_cod_barra, p_produto_id
    );
end;
$$;

-- O Supabase/PostgREST publica Functions como RPC. Esta Function fina apenas
-- adapta a API e chama a Procedure; a regra transacional continua na Procedure.
create or replace function public.cadastrar_produto_com_codigo(
    p_nome varchar,
    p_descricao varchar,
    p_valor numeric,
    p_id_usuario bigint,
    p_id_categoria bigint,
    p_codigo varchar,
    p_tipo_cod_barra varchar
)
returns bigint
language plpgsql
volatile
security invoker
set search_path = ''
as $$
declare
    v_produto_id bigint;
begin
    call public.sp_cadastrar_produto_com_codigo(
        p_nome,
        p_descricao,
        p_valor,
        p_id_usuario,
        p_id_categoria,
        p_codigo,
        p_tipo_cod_barra,
        v_produto_id
    );
    return v_produto_id;
end;
$$;

grant execute on procedure public.sp_cadastrar_produto_com_codigo(
    varchar, varchar, numeric, bigint, bigint, varchar, varchar, bigint
) to anon, authenticated;
grant execute on function public.cadastrar_produto_com_codigo(
    varchar, varchar, numeric, bigint, bigint, varchar, varchar
) to anon, authenticated;

