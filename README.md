# Support Assistant — MVP CLI

Assistente de suporte técnico desenvolvido em **Python**, utilizando Engenharia de Prompt e modelos de linguagem (LLMs) para gerar respostas adaptadas ao perfil do cliente.

Esta branch, `mvp-cli`, preserva a versão funcional do desafio técnico em linha de comando, incluindo geração de conteúdo, comparação entre prompts e avaliação humana.

## Tecnologias

- **Python** — implementação e interface CLI.
- **Groq API** — integração com a LLM.
- **GPT-OSS 120B** (`openai/gpt-oss-120b`) — modelo utilizado.
- **JSON** — armazenamento de clientes, execuções e avaliações.
- **SHA-256** — identificação de requisições equivalentes para cache.

## Funcionalidades

O menu da aplicação permite:

1. **Gerar conteúdo:** utilizar V1 ou V2 para produzir uma resposta personalizada.
2. **Comparar prompts:** executar V1 e V2 para o mesmo cliente, problema e tipo de conteúdo.
3. **Consultar histórico:** visualizar respostas anteriores.
4. **Avaliar resposta:** registrar notas e justificativas humanas.
5. **Sair:** encerrar o programa.

Os quatro tipos de conteúdo disponíveis são:

| Tipo | Descrição |
|---|---|
| `diagnosis` | Hipóteses, evidências, informações faltantes e conclusão. |
| `resolution` | Etapas de resolução do problema. |
| `clarification` | Perguntas de esclarecimento. |
| `flowchart` | Fluxograma estruturado de decisão. |

As respostas seguem formatos JSON específicos, validados pela aplicação.

## Instalação e execução

**1. Clone o repositório e selecione a branch do MVP:**

```bash
git clone -b mvp-cli https://github.com/jean-pietro-lacerda/support-assistant.git
cd support-assistant
```

**2. Crie e ative o ambiente virtual (Ubuntu/Linux):**

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

Preencha a variável `GROQ_API_KEY` no `.env` com sua chave de acesso.

**5. Inicie a aplicação:**

```bash
python main.py
```

## Engenharia de Prompt

A construção dos prompts utiliza componentes separados para persona, contexto, objetivos, instruções, restrições e formato de resposta.

**V1 — Baseline:** prompt básico e funcional, utilizado como referência inicial.

**V2 — Aprimorada:** prompt com orientações mais específicas para melhorar clareza, personalização e utilidade prática.

A comparação mantém o mesmo cliente, ticket, modelo e configurações, permitindo analisar as diferenças entre as versões.

## Avaliação humana

Cada resposta pode receber notas de **1 a 5**, acompanhadas de justificativas, em três critérios:

- **Clarity:** clareza da comunicação.
- **Customer fit:** adequação ao perfil do cliente.
- **Actionability:** utilidade prática da resposta.

### Resultado da comparação registrada

| Critério | V1 | V2 |
|---|---:|---:|
| Clareza | 3/5 | 5/5 |
| Adequação ao cliente | 4/5 | 5/5 |
| Acionabilidade | 4/5 | 5/5 |
| **Total** | **11/15** | **15/15** |

Os resultados representam uma avaliação humana específica, não uma medição estatística de desempenho.

As justificativas, estratégias e limitações estão documentadas em [`PROMPT_ENGINEERING_NOTES.md`](PROMPT_ENGINEERING_NOTES.md).

## Histórico e cache

O arquivo `data/history.json` registra as execuções, incluindo cliente, ticket, versão do prompt, modelo, resposta e avaliação humana.

O cache utiliza SHA-256 para identificar mensagens equivalentes, considerando também modelo, temperatura e versão da validação. Isso permite reutilizar respostas e reduzir chamadas à API.

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
├── tests/
├── main.py
├── .env.example
├── requirements.txt
├── PROMPT_ENGINEERING_NOTES.md
└── README.md
```

## Desenvolvimento

Esta branch contém o **MVP CLI do desafio técnico**, preservado como referência para a Engenharia de Prompt e suas avaliações.

A evolução do projeto para FastAPI e aplicação web acontece separadamente na branch [`main`](https://github.com/jean-pietro-lacerda/support-assistant/tree/main).

**Repositório:** [jean-pietro-lacerda/support-assistant](https://github.com/jean-pietro-lacerda/support-assistant)
