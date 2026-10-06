create or replace view public.vw_produtos_codigos
with (security_invoker = true)
as
select
    p.id as produto_id,
    p.nome as produto,
    p.descricao,
    p.valor,
    coalesce(c.nome, 'Sem categoria') as categoria,
    u.nome as usuario,
    cb.codigo,
    cb.tipo_cod_barra as tipo_codigo
from public.produtos p
join public.usuarios u on u.id = p.id_usuario
join public.codigos_barra cb on cb.id_produto = p.id
left join public.categorias c on c.id = p.id_categoria;

grant select on public.vw_produtos_codigos to anon, authenticated;

