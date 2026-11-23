# Support Assistant — MVP CLI

Assistente de suporte técnico desenvolvido em **Python**, utilizando Engenharia de Prompt e modelos de linguagem (LLMs) para gerar respostas adaptadas ao perfil do cliente.

Esta branch, `mvp-cli`, preserva a versão funcional do desafio técnico em linha de comando, incluindo geração de conteúdo, comparação entre prompts, histórico, cache e avaliação humana.

## Tecnologias

- **Python** — implementação e interface CLI.
- **Groq API** — integração com a LLM.
- **GPT-OSS 120B** (`openai/gpt-oss-120b`) — modelo utilizado.
- **JSON** — armazenamento de clientes, execuções, respostas e avaliações.
- **SHA-256** — identificação de requisições equivalentes para reutilização de respostas em cache.

## Funcionalidades

O menu da aplicação permite:

1. **Gerar conteúdo:** utilizar V1 ou V2 para produzir uma resposta adaptada ao perfil do cliente.
2. **Comparar prompts:** executar V1 e V2 para o mesmo cliente, ticket e tipo de conteúdo.
3. **Consultar histórico:** visualizar respostas geradas anteriormente.
4. **Avaliar resposta:** registrar notas e justificativas humanas.
5. **Sair:** encerrar a aplicação.

Os quatro tipos de conteúdo disponíveis são:

| Tipo | Descrição |
|---|---|
| `diagnosis` | Hipóteses, evidências, informações faltantes e conclusão. |
| `resolution` | Etapas de resolução do problema. |
| `clarification` | Perguntas de esclarecimento. |
| `flowchart` | Fluxograma textual estruturado de decisão. |

As respostas seguem estruturas JSON específicas para cada tipo de conteúdo, com validação pela aplicação.

## Instalação e execução

**1. Clone o repositório na branch do MVP:**

```bash
git clone -b mvp-cli https://github.com/jean-pietro-lacerda/support-assistant.git
cd support-assistant
```

**2. Crie e ative um ambiente virtual (Ubuntu/Linux):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente:**

```bash
cp .env.example .env
```

Preencha a variável `CHAVE_API_LLM` no arquivo `.env` com sua chave de acesso à Groq.

**5. Inicie a aplicação:**

```bash
python main.py
```

## Engenharia de Prompt

A construção dos prompts utiliza componentes separados para:

- **Persona:** define o papel do assistente.
- **Contexto:** apresenta o cliente e o ticket.
- **Objetivos:** determina o conteúdo que deve ser gerado.
- **Instruções:** adapta a comunicação ao nível técnico, estilo e canal do cliente.
- **Restrições:** estabelece limites para o atendimento.
- **Formatos:** define a estrutura JSON esperada.

### V1 — Prompt básico (baseline)

Versão inicial e funcional, utilizada como referência para comparação.

### V2 — Prompt aprimorado

Versão com orientações mais específicas para personalizar a comunicação, considerando o perfil do cliente e os requisitos do atendimento.

As duas versões permitem avaliar o impacto das instruções de Engenharia de Prompt sobre a qualidade das respostas.

Na comparação registrada, foram mantidos o mesmo cliente, ticket, tipo de conteúdo, modelo e configurações de geração.

## Avaliação humana

As respostas podem receber notas de **1 a 5**, acompanhadas de justificativas, em três critérios:

- **Clarity:** clareza da comunicação.
- **Customer fit:** adequação ao perfil do cliente.
- **Actionability:** utilidade prática da resposta.

### Comparação registrada — Diagnóstico de João

**Cliente:** João  
**Perfil:** leigo, didático, chat  
**Ticket:** Meu aplicativo fecha sozinho quando tento abrir.

| Critério | V1 | V2 |
|---|---:|---:|
| Clareza | 3/5 | 5/5 |
| Adequação ao cliente | 4/5 | 5/5 |
| Acionabilidade | 4/5 | 5/5 |
| **Total** | **11/15** | **15/15** |

A V1 apresentou um diagnóstico estruturado e funcional. A V2 demonstrou melhorias na clareza, na adequação ao perfil leigo e na facilidade de fornecer informações para continuar o atendimento.

Esses resultados representam uma **avaliação humana de um cenário específico**, não uma medição estatística de desempenho.

As notas, justificativas individuais e a conclusão comparativa estão documentadas em [`PROMPT_ENGINEERING_NOTES.md`](PROMPT_ENGINEERING_NOTES.md).

## Histórico e cache

O arquivo `data/history.json` armazena registros das execuções, incluindo dados do cliente, ticket, versão do prompt, modelo utilizado, mensagens enviadas à LLM, resposta gerada e avaliação humana, quando disponível.

O cache utiliza SHA-256 para identificar mensagens equivalentes, considerando também parâmetros como modelo, temperatura e versão da validação.

Esse mecanismo permite reutilizar resultados compatíveis, reduzindo chamadas repetidas à API.

## Exemplos de execução — Samples

A pasta `samples/` contém cinco exemplos reais de execução, extraídos do histórico da aplicação.

Cada arquivo JSON preserva o registro completo da geração correspondente, incluindo:

- Identificação e perfil do cliente.
- Ticket, versão do prompt e tipo de conteúdo.
- Provedor, modelo e parâmetros de geração.
- Mensagens completas enviadas à LLM.
- Resposta original produzida pelo modelo.
- Identificador, data, hash e metadados de validação.
- Avaliação humana, quando disponível.

### Arquivos disponíveis

| Arquivo | Conteúdo |
|---|---|
| `diagnosis_v1.json` | Diagnóstico de João utilizando V1, com avaliação humana. |
| `diagnosis_v2.json` | Diagnóstico de João utilizando V2, com avaliação humana. |
| `resolution_v2.json` | Exemplo de resolução utilizando V2. |
| `clarification_v2.json` | Exemplo de esclarecimento utilizando V2. |
| `flowchart_v2.json` | Fluxograma V2 de Maria sobre o acesso ao site da Alura. |

Os exemplos completos permitem verificar **quais instruções foram enviadas, como a LLM respondeu e quais configurações foram utilizadas**, oferecendo rastreabilidade às gerações apresentadas no projeto.

## Estrutura do projeto

```text
support-assistant/
├── data/
│   ├── customers.json
│   └── history.json
├── prompts/
│   ├── persona.py
│   ├── context.py
│   ├── objectives.py
│   ├── instructions.py
│   ├── restrictions.py
│   └── formats.py
├── services/
│   ├── llm.py
│   ├── prompt_engine.py
│   └── storage.py
├── samples/
│   ├── diagnosis_v1.json
│   ├── diagnosis_v2.json
│   ├── resolution_v2.json
│   ├── clarification_v2.json
│   └── flowchart_v2.json
├── tests/
├── main.py
├── .env.example
├── requirements.txt
├── PROMPT_ENGINEERING_NOTES.md
└── README.md
```

## Desenvolvimento

A branch `mvp-cli` contém o **MVP CLI do desafio técnico**, preservando a implementação em linha de comando e os registros utilizados na avaliação de Engenharia de Prompt.

A evolução do projeto para FastAPI e aplicação web acontece separadamente na branch [`main`](https://github.com/jean-pietro-lacerda/support-assistant/tree/main).

**Repositório:** [jean-pietro-lacerda/support-assistant](https://github.com/jean-pietro-lacerda/support-assistant)