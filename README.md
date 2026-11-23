# Support Assistant

Assistente de suporte técnico desenvolvido para o desafio de **IA e Engenharia de Prompt**, utilizando modelos de linguagem para gerar respostas adaptadas ao perfil de diferentes clientes.

O projeto foi desenvolvido em duas etapas independentes:

- **`mvp-cli`** — preserva o MVP obrigatório do desafio em interface de linha de comando.
- **`main`** — representa a evolução da solução, adicionando interface web, API FastAPI, PostgreSQL, cache persistente e execução com Docker Compose.

A separação das branches mantém o MVP original reproduzível e permite demonstrar também a evolução técnica do projeto.

---

## Aplicação principal — `main`

A branch `main` contém a versão web do Support Assistant.

A aplicação permite selecionar um cliente, informar um problema técnico e gerar respostas personalizadas de acordo com:

- nível técnico;
- estilo de comunicação;
- canal de atendimento;
- tipo de conteúdo;
- versão do prompt.

O frontend também permite comparar diretamente as respostas produzidas pelas versões **V1** e **V2** dos prompts e consultar a avaliação humana utilizada no desafio.

### Tecnologias

- **Python**
- **FastAPI**
- **Groq API**
- **GPT-OSS 120B** (`openai/gpt-oss-120b`)
- **PostgreSQL**
- **React**
- **TypeScript**
- **Vite**
- **Docker**
- **Docker Compose**

---

## MVP obrigatório — `mvp-cli`

A branch `mvp-cli` preserva separadamente a implementação mínima obrigatória do desafio técnico.

Ela contém uma aplicação CLI funcional com:

- geração dos quatro tipos de conteúdo;
- seleção dos perfis de cliente;
- prompts V1 e V2;
- comparação entre versões;
- persistência em `data/history.json`;
- cache de respostas equivalentes;
- avaliação humana pela rubrica obrigatória;
- samples completos das execuções utilizadas.

A branch também possui documentação própria de instalação e execução.

Para acessar o MVP:

```bash
git checkout mvp-cli
```

A `main` não substitui esse MVP. Ela representa uma evolução da solução para uma arquitetura web.

---

## Engenharia de Prompt

Os prompts são construídos dinamicamente a partir de componentes separados:

- **Persona** — define o papel e as responsabilidades do assistente.
- **Contexto** — fornece o perfil do cliente e o ticket.
- **Objetivos** — define a finalidade do conteúdo solicitado.
- **Instruções** — adapta linguagem, profundidade técnica, estilo e canal.
- **Restrições** — estabelece limites técnicos, de segurança e comunicação.
- **Formatos** — define o contrato JSON esperado para cada tipo de resposta.

O módulo `services/prompt_engine.py` combina esses componentes de acordo com o cliente, o ticket, o tipo de conteúdo e a versão do prompt.

### V1

A **V1** representa o prompt básico utilizado como baseline.

Ela é funcional e foi mantida propositalmente mais simples para permitir uma comparação controlada com a versão aprimorada.

### V2

A **V2** utiliza instruções mais específicas para:

- adaptar a linguagem ao nível técnico;
- respeitar o estilo de comunicação;
- adaptar a apresentação ao canal;
- controlar melhor hipóteses e limitações;
- melhorar a estrutura dos quatro tipos de conteúdo.

---

## Tipos de conteúdo

A aplicação gera quatro estruturas diferentes.

### Diagnóstico

Contém:

- hipóteses;
- evidências;
- informações faltantes;
- conclusão.

### Resolução

Contém:

- título;
- etapas de resolução;
- orientações adicionais.

### Esclarecimento

Contém perguntas priorizadas para obter somente as informações necessárias para continuar o atendimento.

### Fluxograma

Gera uma árvore textual de decisão utilizando o formato `decision_tree`.

---

## Perfis de cliente

O projeto possui três perfis armazenados em `data/customers.json`.

| Cliente | Nível técnico | Estilo | Canal |
|---|---|---|---|
| João | Leigo | Didático | Chat |
| Maria | Avançado | Direto | E-mail |
| Carlos | Intermediário | Detalhado | Telefone |

Os perfis são utilizados diretamente na construção dinâmica dos prompts.

---

## Comparação V1 × V2

O desafio exige pelo menos uma comparação controlada entre duas versões de prompt.

A comparação registrada utiliza:

**Cliente:** João  
**Perfil:** leigo, didático, chat  
**Ticket:** `Meu aplicativo fecha sozinho quando tento abrir.`  
**Tipo:** diagnóstico  
**Modelo:** `openai/gpt-oss-120b`  
**Temperatura:** `0.2`

Os mesmos parâmetros foram utilizados nas duas versões, alterando principalmente o prompt.

### Avaliação humana

| Critério | V1 | V2 |
|---|---:|---:|
| Clareza | 3/5 | 5/5 |
| Adequação ao cliente | 4/5 | 5/5 |
| Acionabilidade | 4/5 | 5/5 |
| **Total** | **11/15** | **15/15** |

A avaliação completa e suas justificativas estão documentadas em:

`PROMPT_ENGINEERING_NOTES.md`

---

## Samples

O diretório `samples/` contém cinco registros reais e completos de execução:

- `diagnosis_v1.json`
- `diagnosis_v2.json`
- `resolution_v2.json`
- `clarification_v2.json`
- `flowchart_v2.json`

Os registros incluem, entre outras informações:

- cliente;
- ticket;
- versão do prompt;
- tipo de conteúdo;
- modelo;
- temperatura;
- mensagens enviadas à LLM;
- saída produzida;
- hash do prompt;
- avaliação humana, quando disponível.

---

## Arquitetura da aplicação web

A aplicação da branch `main` é dividida em três serviços principais:

```text
                ┌──────────────┐
                │   Groq API   │
                └──────▲───────┘
                       │
Frontend React ──► FastAPI Backend
                       │
                       ▼
                ┌──────────────┐
                │ PostgreSQL   │
                └──────────────┘
```

### Frontend

Responsável pela interface de utilização da aplicação.

Possui três áreas principais:

- **Gerar resposta**
- **Comparar V1 × V2**
- **Minha avaliação**

### Backend

A API FastAPI fornece as principais rotas:

```text
GET  /customers
GET  /evaluation
POST /generate
POST /compare
```

### PostgreSQL

Na versão web, as novas execuções são persistidas em PostgreSQL utilizando JSONB.

Também é utilizado para o mecanismo de cache.

---

## Cache

Antes de realizar uma nova chamada à LLM, a aplicação verifica se já existe uma execução equivalente.

A identificação utiliza SHA-256 sobre as mensagens do prompt e a versão da validação.

A busca também considera:

- provedor;
- modelo;
- temperatura.

Caso exista uma execução equivalente, a resposta armazenada é reutilizada.

O cache foi validado durante os testes da aplicação:

```text
Quantidade inicial:             4
Após uma nova geração:          5
Após repetir a mesma geração:   5
```

A segunda solicitação equivalente reutilizou o registro existente.

---

## Persistência

O PostgreSQL utiliza um volume Docker:

```text
postgres_data
```

Os dados permanecem armazenados mesmo após:

```bash
docker compose down
```

A persistência foi validada reiniciando os serviços e verificando que os registros anteriores continuaram disponíveis.

---

# Execução com Docker

A maneira recomendada de executar a aplicação da branch `main` é utilizando Docker Compose.

## 1. Clone o repositório

```bash
git clone https://github.com/jean-pietro-lacerda/support-assistant.git
cd support-assistant
```

## 2. Configure as variáveis de ambiente

Crie seu `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Preencha as variáveis necessárias:

```env
CHAVE_API_LLM=SUA_CHAVE_GROQ
GROQ_MODEL=openai/gpt-oss-120b

DB_NAME=support_assistant
DB_USER=support_user
DB_PASSWORD=SUA_SENHA
```

O arquivo `.env` não é versionado.

O PostgreSQL do Docker cria automaticamente o banco e o usuário utilizando essas configurações.

---

## 3. Inicie a aplicação

```bash
docker compose up --build
```

Os serviços iniciados são:

```text
frontend
backend
db
```

Acesse:

```text
http://localhost:5173
```

A documentação automática da API pode ser acessada em:

```text
http://localhost:8001/docs
```

---

## Encerrar os serviços

```bash
docker compose down
```

O volume PostgreSQL é preservado.

Para acompanhar os logs:

```bash
docker compose logs -f frontend backend db
```

---

## Inicialização do PostgreSQL

O arquivo:

```text
docker/postgres/001-executions.sql
```

cria automaticamente a estrutura necessária no primeiro uso de um volume novo.

A tabela `executions` armazena os registros utilizados pela aplicação web e pelo mecanismo de cache.

---

## Estrutura resumida

```text
support-assistant/
│
├── backend/
│   ├── routes/
│   ├── api.py
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
│
├── prompts/
│   ├── persona.py
│   ├── context.py
│   ├── objectives.py
│   ├── instructions.py
│   ├── restrictions.py
│   └── formats.py
│
├── services/
│   ├── database.py
│   ├── generation.py
│   ├── llm.py
│   ├── prompt_engine.py
│   └── storage.py
│
├── data/
│   ├── customers.json
│   └── history.json
│
├── docker/
│   └── postgres/
│       └── 001-executions.sql
│
├── samples/
│   ├── diagnosis_v1.json
│   ├── diagnosis_v2.json
│   ├── resolution_v2.json
│   ├── clarification_v2.json
│   └── flowchart_v2.json
│
├── compose.yaml
├── .env.example
├── requirements.txt
├── PROMPT_ENGINEERING_NOTES.md
└── README.md
```

---

## Validações realizadas

Durante o desenvolvimento foram verificados:

- funcionamento do frontend;
- comunicação frontend/backend;
- geração dos quatro formatos;
- comparação V1 × V2;
- visualização da avaliação humana;
- renderização Markdown;
- build e lint do frontend;
- inicialização do PostgreSQL;
- inicialização do FastAPI;
- Docker Compose com os três serviços;
- healthcheck do banco;
- healthcheck do backend;
- funcionamento do cache;
- persistência do PostgreSQL após reinicialização.

---

## Limitações

A avaliação humana registrada utiliza um único cenário controlado.

As respostas de modelos de linguagem podem variar, e a validação estrutural do JSON não garante, por si só, a correção técnica ou semântica de cada resposta.

A aplicação também não mantém automaticamente uma conversa multi-turn entre gerações independentes.

As decisões, limitações e evolução dos prompts são discutidas com mais detalhes em:

`PROMPT_ENGINEERING_NOTES.md`

---

## Branches

### `mvp-cli`

MVP obrigatório do desafio técnico em linha de comando.

Preserva a implementação original baseada em JSON para histórico e cache.

### `main`

Evolução da solução com:

- interface React;
- backend FastAPI;
- PostgreSQL;
- cache persistente;
- comparação visual V1 × V2;
- visualização da avaliação;
- Docker Compose.
