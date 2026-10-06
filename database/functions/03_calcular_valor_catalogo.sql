create or replace function public.calcular_valor_catalogo(p_id_usuario bigint)
returns numeric
language sql
stable
security invoker
set search_path = ''
as $$
    select coalesce(sum(p.valor), 0)
    from public.produtos p
    where p.id_usuario = p_id_usuario;
$$;

grant execute on function public.calcular_valor_catalogo(bigint) to anon, authenticated;

