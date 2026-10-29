# Gerenciador de Codigos de Barra com Supabase

Trabalho avaliativo que demonstra uma aplicacao Python integrada ao PostgreSQL do Supabase. O sistema gerencia usuarios, categorias, produtos e codigos de barra, indo alem de um CRUD ao utilizar View, Function e Procedure em funcionalidades reais.

## Identificacao
- Integrante: Artur França
- Disciplina: Introducao a Banco de Dados
- Professor(a): Anderson Soares

## Tecnologias

- Python 3.10 ou superior
- Supabase
- PostgreSQL
- Biblioteca `supabase-py`
- Biblioteca `python-dotenv`
- Redis (cache de consultas, com TTL configuravel)
- Biblioteca `redis`

## Recursos do banco utilizados

| Recurso | Nome | Finalidade | Uso na aplicacao |
|---|---|---|---|
| View | `vw_produtos_codigos` | Reunir produto, usuario, categoria e codigo em um relatorio | Menu Produtos, opcao 7 |
| Function | `calcular_valor_catalogo` | Somar o valor dos produtos de um usuario | Menu Produtos, opcao 8 |
| Procedure | `sp_cadastrar_produto_com_codigo` | Cadastrar produto e codigo juntos na mesma transacao | Menu Produtos, opcao 2 |

O Supabase publica Functions pela API RPC, mas nao publica `CALL` de Procedures
diretamente. Por isso, `cadastrar_produto_com_codigo` funciona como adaptador
RPC e chama internamente a Procedure `sp_cadastrar_produto_com_codigo`. A regra
de cadastro transacional permanece implementada e executada na Procedure.

## Principais tabelas

- `usuarios`: proprietarios dos produtos;
- `categorias`: classificacao dos produtos;
- `produtos`: nome, descricao, valor, usuario e categoria;
- `codigos_barra`: codigo unico associado a um produto.

## Estrutura

```text
gerenciador_codigo_barra/
|-- src/                 # codigo-fonte Python
|   |-- index.py         # acesso ao Supabase e cache opcional
|   `-- interface.py     # menus da aplicacao
|-- database/
|   |-- tables/          # tabelas e permissoes
|   |-- views/           # View do relatorio
|   |-- functions/       # Function de calculo
|   |-- procedures/      # Procedure e adaptador RPC
|   `-- inserts/         # dados de demonstracao
|-- .env.example
|-- requirements.txt
`-- interface.py         # ponto de entrada
```

## Como o Redis funciona

O Redis e usado como cache (padrao cache-aside) nas consultas de categorias,
usuarios, produtos, codigos de barra, relatorio da View, categorias sem produtos
e total do catalogo. O TTL padrao e de 300 segundos. Quando um cadastro,
atualizacao, exclusao ou cadastro integrado e concluido, as chaves de cache
com o prefixo `gerenciador_codigos:` sao invalidadas. Se o Redis estiver
indisponivel ou nao configurado, a aplicacao continua consultando o Supabase.
O cache e desativado por padrao; para habilita-lo, configure `REDIS_HOST` no
arquivo `.env`. A aplicacao nao tenta conectar a um servidor Redis remoto por
padrao.

As credenciais ficam em variaveis de ambiente; nao coloque a senha diretamente
no codigo nem publique o arquivo `.env`.

## Configuracao do Supabase

1. Crie um projeto em [Supabase](https://supabase.com/).
2. Abra **SQL Editor** no painel do projeto.
3. Execute o arquivo `database/setup.sql` inteiro. Como alternativa, execute,
   nesta ordem:
   - `database/tables/01_tabelas.sql`
   - `database/views/02_vw_produtos_codigos.sql`
   - `database/functions/03_calcular_valor_catalogo.sql`
   - `database/procedures/04_cadastrar_produto_com_codigo.sql`
   - `database/inserts/05_dados_teste.sql`
4. Em **Project Settings > API**, copie a URL e a chave publica `anon` ou
   `publishable`.
5. Copie `.env.example` para `.env` e preencha:

```env
SUPABASE_URL=https://SEU-PROJETO.supabase.co
SUPABASE_KEY=SUA_CHAVE_PUBLICA
REDIS_HOST=SEU_HOST_REDIS
REDIS_PORT=6379
REDIS_USERNAME=default
REDIS_PASSWORD=SUA_SENHA_REDIS
REDIS_CACHE_TTL=300
```

As variaveis Redis sao opcionais; remova-as ou deixe `REDIS_HOST` sem valor para
desativar o cache. Nunca publique `.env`, uma chave `service_role` ou uma chave
secreta. A senha Redis deve ser inserida somente localmente em `.env`.

## Como executar



```powershell
python -m pip install -r requirements.txt
python interface.py
```

Para demonstrar os recursos avaliados, abra **Produtos e recursos SQL** e use
as opcoes 2 (Procedure), 7 (View) e 8 (Function).

## Seguranca

Para facilitar a avaliacao sem sistema de login, os scripts concedem acesso as
tabelas para a chave publica e deixam RLS desativada. Isso e adequado apenas
para demonstracao academica sem dados reais. Em producao, use Supabase Auth,
habilite RLS e defina politicas por usuario.

## Video e README

Interface e README do projeto feito com uso de inteligência artificial. Link para o Youtube do video: [video](https://youtu.be/gdx77UdQeI4)
