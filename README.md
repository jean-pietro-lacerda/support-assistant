# Support Assistant — MVP CLI

Assistente de suporte técnico desenvolvido em **Python**, utilizando Engenharia de Prompt e um modelo de linguagem (LLM) para gerar respostas personalizadas conforme o perfil do cliente.

Esta branch (`cli-mvp`) preserva a versão funcional do projeto em **interface de linha de comando (CLI)**, incluindo a comparação entre prompts V1 e V2 e a avaliação humana dos resultados.

## Tecnologias utilizadas

- **Python** — implementação e interface CLI.
- **Groq API** — integração com a LLM.
- **GPT-OSS 120B** (`openai/gpt-oss-120b`) — modelo utilizado.
- **JSON** — armazenamento de clientes, execuções e avaliações.
- **SHA-256** — identificação de requisições equivalentes para cache.

## Funcionalidades

O sistema oferece cinco opções no terminal:

1. **Gerar conteúdo:** produz respostas personalizadas com V1 ou V2.
2. **Comparar prompts:** executa V1 e V2 para o mesmo cliente, problema e tipo de conteúdo.
3. **Consultar histórico:** permite visualizar execuções anteriores.
4. **Avaliar resposta:** registra notas e justificativas humanas.
5. **Sair:** encerra a aplicação.

### Tipos de conteúdo

| Tipo | Finalidade |
|---|---|
| `diagnosis` | Hipóteses, evidências, informações faltantes e conclusão. |
| `resolution` | Passos para solucionar o problema. |
| `clarification` | Perguntas para obter informações adicionais. |
| `flowchart` | Fluxo de decisão estruturado. |

As respostas seguem formatos JSON definidos e validados pelo sistema.

## Engenharia de Prompt

O projeto utiliza componentes separados de **persona, contexto, objetivos, instruções, restrições e formatos** para organizar a construção dos prompts.

**V1 — Baseline:** versão básica e funcional, utilizada como referência inicial.

**V2 — Aprimorada:** versão com instruções mais específicas para melhorar clareza, adequação ao perfil e utilidade das respostas.

A comparação utiliza o mesmo cliente, ticket, modelo e configurações, permitindo observar os efeitos das alterações nos prompts.

### Avaliação humana

As respostas podem ser avaliadas de **1 a 5** em três critérios:

- **Clarity:** clareza da comunicação.
- **Customer fit:** adequação ao perfil do cliente.
- **Actionability:** utilidade prática das orientações.

Cada nota acompanha uma justificativa. As avaliações ficam armazenadas no histórico.

## Como executar

**1. Clone o repositório e acesse a branch do MVP:**

```bash
git clone https://github.com/SEU-USUARIO/support-assistant.git
cd support-assistant
git checkout cli-mvp
```

Substitua a URL pelo endereço real do repositório.

**2. Crie e ative o ambiente virtual (Ubuntu/Linux):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**4. Configure a API:**

```bash
cp .env.example .env
```

Preencha a variável `GROQ_API_KEY` com sua chave da Groq. O arquivo `.env` não deve ser enviado ao GitHub.

**5. Execute:**

```bash
python main.py
```

O menu interativo será apresentado no terminal.

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

## Histórico e cache

O arquivo `data/history.json` armazena as execuções, incluindo perfil do cliente, problema, versão do prompt, modelo, resposta e avaliação humana.

O cache utiliza o hash das mensagens e considera o modelo, a temperatura e a versão da validação para reutilizar respostas equivalentes, evitando chamadas desnecessárias à API.

## Resultados e documentação

O MVP inclui execuções de diferentes tipos de conteúdo e uma comparação avaliada entre V1 e V2.

Na avaliação registrada para o mesmo diagnóstico:

| Critério | V1 | V2 |
|---|---:|---:|
| Clareza | 3/5 | 5/5 |
| Adequação ao cliente | 4/5 | 5/5 |
| Acionabilidade | 4/5 | 5/5 |
| **Total** | **11/15** | **15/15** |

Essas notas representam uma avaliação humana específica, não uma medição estatística de desempenho.

Para consultar as estratégias utilizadas, as justificativas e as limitações observadas, veja **`PROMPT_ENGINEERING_NOTES.md`**.

---

**Observação:** esta branch representa o MVP CLI concluído. O desenvolvimento posterior da API e da aplicação web ocorre separadamente na branch `main`.
