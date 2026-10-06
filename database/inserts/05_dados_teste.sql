insert into public.categorias (nome) values
    ('Alimentos'),
    ('Bebidas'),
    ('Limpeza'),
    ('Categoria sem produto')
on conflict (nome) do nothing;

insert into public.usuarios (nome, cnpj)
select 'Mercado Exemplo', '12345678000190'
where not exists (
    select 1 from public.usuarios where cnpj = '12345678000190'
);

insert into public.produtos (nome, valor, descricao, id_usuario, id_categoria)
select
    'Cafe 500g',
    18.90,
    'Cafe torrado e moido',
    u.id,
    c.id
from public.usuarios u
join public.categorias c on c.nome = 'Alimentos'
where u.cnpj = '12345678000190'
  and not exists (select 1 from public.produtos where nome = 'Cafe 500g');

insert into public.codigos_barra (codigo, tipo_cod_barra, id_produto)
select '7891234567890', 'EAN-13', p.id
from public.produtos p
where p.nome = 'Cafe 500g'
on conflict (codigo) do nothing;

