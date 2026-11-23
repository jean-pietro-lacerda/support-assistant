# Avaliação — Diagnóstico de João (V1 × V2)

**Cliente:** João  
**Perfil:** Leigo, didático, chat  
**Ticket:** Meu aplicativo fecha sozinho quando tento abrir.

## V1 — Prompt básico

**Clareza — 3/5**

O diagnóstico apresenta uma estrutura organizada, porém utiliza termos técnicos, como RAM, sem explicações. Isso pode dificultar a compreensão de um cliente leigo.

**Adequação ao cliente — 4/5**

A resposta é compreensível em grande parte, mas alguns termos e informações solicitadas exigem conhecimentos técnicos que o cliente pode não possuir.

**Acionabilidade — 4/5**

A resposta identifica as informações necessárias para avançar no diagnóstico, mas não explica como o cliente pode obtê-las, especialmente informações sobre memória RAM e armazenamento.

**Total: 11/15**

## V2 — Prompt aprimorado

**Clareza — 5/5**

O diagnóstico apresenta informações mais objetivas e organizadas, utilizando uma linguagem mais acessível e evitando termos técnicos desnecessários.

**Adequação ao cliente — 5/5**

A resposta está mais adequada ao perfil leigo, apresentando exemplos familiares, como Android, iPhone e Windows, e utilizando explicações mais compreensíveis sobre as possíveis causas.

**Acionabilidade — 5/5**

As informações solicitadas são mais simples e relevantes para continuar o diagnóstico. Destaca-se a pergunta sobre o aplicativo já ter funcionado anteriormente, que ajuda a investigar o problema sem exigir conhecimentos técnicos avançados.

**Total: 15/15**

## Conclusão comparativa

A V1 conseguiu estruturar corretamente o diagnóstico, identificar possíveis causas e reconhecer a ausência de informações suficientes para uma conclusão definitiva.

Entretanto, a V2 apresentou uma evolução na clareza, na adequação ao perfil do cliente e na facilidade de fornecer as informações necessárias para continuar o atendimento.

A comparação demonstra o benefício das instruções mais específicas de personalização utilizadas na V2, mantendo a V1 como uma versão básica e funcional.

---

## Estratégias de Engenharia de Prompt

### 1. Construção modular

O motor de Engenharia de Prompt foi dividido em seis componentes:

| Componente | Responsabilidade |
|---|---|
| Persona | Define o papel do assistente e suas responsabilidades. |
| Contexto | Incorpora o perfil do cliente e o ticket. |
| Objetivos | Define a finalidade de cada tipo de conteúdo. |
| Instruções | Adapta linguagem, nível técnico, estilo e canal. |
| Restrições | Estabelece limites técnicos, de segurança e de comunicação. |
| Formatos | Define os campos e tipos esperados no JSON. |

O módulo `services/prompt_engine.py` combina esses componentes dinamicamente conforme o cliente, o conteúdo solicitado e a versão escolhida.

Essa separação facilita a manutenção e a reutilização das instruções, evitando a criação de um prompt independente para cada combinação de parâmetros.

### 2. Versionamento dos prompts

A **V1** foi desenvolvida como uma versão básica, funcional e adequada para servir de referência inicial.

A **V2** utiliza instruções mais específicas para adaptar a profundidade técnica, o estilo de comunicação e a apresentação ao perfil selecionado. Também diferencia os objetivos de diagnóstico, resolução, esclarecimento e fluxograma.

O propósito do versionamento é permitir uma comparação controlada entre uma abordagem básica e uma abordagem aprimorada, sem tornar a V1 artificialmente inadequada.

Na avaliação registrada, foram utilizados o mesmo cliente, ticket, tipo de conteúdo, modelo `openai/gpt-oss-120b` e temperatura `0.2`.

### 3. Contexto e separação das mensagens

As instruções do assistente são enviadas na mensagem `system`, enquanto o perfil do cliente e o problema relatado são apresentados na mensagem `user`, delimitados como dados do atendimento.

Essa organização diferencia as regras de comportamento das informações que a LLM deve analisar.

O assistente foi projetado para responder diretamente ao cliente final, considerando seu nível técnico, sem assumir que um cliente avançado possui permissões administrativas ou acesso ao código-fonte.

### 4. Estruturação das respostas

Foram definidos quatro contratos JSON:

- **Diagnóstico:** hipóteses, evidências, informações faltantes e conclusão.
- **Resolução:** título, etapas e orientações complementares.
- **Esclarecimento:** perguntas necessárias para avançar no atendimento.
- **Fluxograma:** árvore textual de decisão com etapas e destinos identificáveis.

A estruturação permite armazenar, consultar e comparar as respostas, mantendo campos específicos para cada finalidade.

A validação da aplicação verifica o formato JSON, os tipos e algumas propriedades obrigatórias. A avaliação da qualidade do conteúdo permanece uma atividade distinta.

## Decisões e evolução dos prompts

### Personalização por canal

Além do nível técnico e do estilo de comunicação, a V2 adapta a apresentação para chat, e-mail e telefone.

Na adaptação por e-mail, optou-se por gerar a comunicação diretamente pela LLM, incluindo saudação personalizada e encerramento profissional dentro dos campos JSON existentes.

Essa decisão preserva os contratos de saída, sem exigir novos campos ou uma etapa adicional de montagem da mensagem.

### Otimização das instruções

Durante o desenvolvimento, foram identificadas redundâncias entre orientações gerais, restrições e regras específicas de apresentação.

A otimização foi concentrada nas instruções da V2 para e-mail, especialmente em `prompts/formats.py`, removendo repetições e tornando mais clara a apresentação dos conteúdos.

No fluxograma, as instruções foram reformuladas para orientar ações e perguntas diretamente ao cliente, considerando as informações já presentes no ticket.

As alterações foram localizadas para preservar os prompts da avaliação original de João. As mensagens e os hashes dessa comparação permaneceram idênticos.

### Histórico, cache e rastreabilidade

O arquivo `data/history.json` registra as execuções com identificação do cliente, ticket, versão, conteúdo, modelo, configurações, mensagens enviadas e saída gerada.

O sistema utiliza hashing SHA-256 sobre as mensagens e a versão da validação para identificar o prompt. Na busca do cache, também compara provedor, modelo e temperatura.

Os cinco arquivos de `samples/` contêm registros reais e completos extraídos do histórico, incluindo as avaliações humanas quando disponíveis.

Essa abordagem permite examinar as entradas e configurações associadas a cada resultado sem precisar repetir as chamadas à API.

## Limitações e decisões de escopo

**Avaliação limitada:** a comparação humana documentada utiliza um único cenário de diagnóstico. O resultado de 15/15 na V2 representa uma melhoria observada nesse caso, mas não garante desempenho superior em todas as situações.

**Variação das respostas:** mesmo com instruções explícitas, a LLM pode produzir conteúdo que não corresponda integralmente ao comportamento esperado. A validação estrutural do JSON não garante correção técnica ou coerência semântica.

**Atendimento sem continuidade conversacional:** cada geração considera o perfil e o ticket fornecidos naquele momento, sem incorporar automaticamente as respostas de interações anteriores.

**Apresentação por e-mail:** para preservar o JSON existente, saudação e encerramento são inseridos em campos já definidos. Isso simplifica a integração atual, mas mistura elementos de apresentação com conteúdos estruturados.

**Escopo do MVP:** a solução prioriza Engenharia de Prompt, execução via CLI, comparação de versões, persistência e cache. A interface web e o deploy não são necessários para demonstrar os requisitos mínimos desta implementação.

## Considerações finais

O projeto demonstra uma evolução de Engenharia de Prompt fundamentada na personalização, na estruturação das respostas e na comparação entre versões.

Os resultados da avaliação de João evidenciam melhorias na V2 para o cenário analisado, enquanto as otimizações posteriores buscaram reduzir redundâncias e melhorar a clareza das instruções sem comprometer os registros avaliados.

A estratégia adotada prioriza uma solução modular, executável e verificável, reconhecendo que a qualidade das respostas da LLM também depende das informações disponíveis e da avaliação humana.