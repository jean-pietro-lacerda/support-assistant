import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import './App.css'

type Tab = 'generate' | 'compare' | 'evaluation'
type Customer = {
  customer_id: string
  name: string
  technical_level: string
  communication_style: string
  channel: string
}
type Comparison = { v1: unknown; v2: unknown }
type EvaluationRecord = {
  [field: string]: unknown
  id: string
  customer_id: string
  customer_profile: { name: string; technical_level: string; communication_style: string; channel: string }
  ticket: string
  prompt_version: string
  content_type: string
  evaluation: Record<string, { score: number; justification: string }>
  output: { hypotheses?: string[]; evidence?: string[]; missing_information?: string[]; conclusion?: string }
  messages?: { role: string; content: string }[]
}
type Evaluation = { notes_markdown: string; history_cli: EvaluationRecord[] }

function nomeDoPerfil(valor: string) {
  const nomes: Record<string, string> = {
    leigo: 'Leigo', intermediario: 'Intermediário', avancado: 'Avançado',
    direto: 'Direto', detalhado: 'Detalhado', didatico: 'Didático',
    chat: 'Chat', email: 'E-mail', telefone: 'Telefone',
  }
  return nomes[valor] ?? valor
}

function RespostaAssistente({ resposta }: { resposta: unknown }) {
  const titulos: Record<string, string> = {
    hypotheses: 'Hipóteses', evidence: 'Evidências',
    missing_information: 'Informações faltantes', conclusion: 'Conclusão',
    title: 'Título', steps: 'Etapas', additional_guidance: 'Orientações adicionais',
    questions: 'Perguntas de esclarecimento', format: 'Formato', flow: 'Fluxo de decisão',
  }

  return <>
    {Object.entries(resposta as Record<string, unknown>).map(([campo, valor]) => {
      const Lista = campo === 'steps' ? 'ol' : 'ul'

      return (
        <div className="answer-field" key={campo}>
          <h4>{titulos[campo] ?? campo}</h4>
          {Array.isArray(valor) ? (
            <Lista>
              {valor.map((item, index) => (
                <li key={index}>{typeof item === 'string' ? item : JSON.stringify(item)}</li>
              ))}
            </Lista>
          ) : (
            <p className={campo === 'flow' ? 'answer-flow' : undefined}>
              {typeof valor === 'string' ? valor : JSON.stringify(valor)}
            </p>
          )}
        </div>
      )
    })}
    <details className="answer-json">
      <summary>JSON completo</summary>
      <pre>{JSON.stringify(resposta, null, 2)}</pre>
    </details>
  </>
}

function formatarNegrito(texto: string) {
  const partes = texto.split('**')

  return partes.map((parte, index) => {
    if (index % 2 === 0) return parte
    if (index === partes.length - 1) return `**${parte}`
    return <strong key={index}>{parte}</strong>
  })
}

async function consultarApi(path: string, body?: object) {
  const response = await fetch(`/api/${path}`, body ? {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  } : undefined)
  if (!response.ok) {
    const data = await response.json().catch(() => null)
    const detail = data?.detail
    throw new Error(typeof detail === 'string' ? detail
      : response.status === 422 ? 'Confira os campos do formulário.'
      : `Não foi possível concluir a solicitação (HTTP ${response.status}).`)
  }
  return response.json()
}

function App() {
  const [tab, setTab] = useState<Tab>('generate')
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loadingCustomers, setLoadingCustomers] = useState(true)
  const [customerError, setCustomerError] = useState('')
  const [customerId, setCustomerId] = useState('')
  const [contentType, setContentType] = useState('diagnosis')
  const [promptVersion, setPromptVersion] = useState('v2')
  const [ticket, setTicket] = useState('')
  const [generatedTicket, setGeneratedTicket] = useState('')
  const [comparedTicket, setComparedTicket] = useState('')
  const [output, setOutput] = useState<unknown>(null)
  const [comparison, setComparison] = useState<Comparison | null>(null)
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const selectedCustomer = customers.find((customer) => customer.customer_id === customerId)

  useEffect(() => {
    let active = true
    consultarApi('customers')
      .then((data: Customer[]) => {
        if (active) {
          setCustomers(data)
          setCustomerId(data[0]?.customer_id ?? '')
        }
      })
      .catch(() => {
        if (active) setCustomerError('Não foi possível carregar os clientes. Verifique se a API está disponível e recarregue a página.')
      })
      .finally(() => { if (active) setLoadingCustomers(false) })
    return () => { active = false }
  }, [])

  async function consultarAvaliacao() {
    setBusy(true)
    setError('')
    try {
      setEvaluation(await consultarApi('evaluation'))
    } catch (erro) {
      setError(erro instanceof Error ? erro.message : 'Não foi possível consultar a avaliação.')
    } finally {
      setBusy(false)
    }
  }

  function selecionarAba(nextTab: Tab) {
    setTab(nextTab)
    setError('')
    if (nextTab === 'evaluation' && !evaluation) void consultarAvaliacao()
  }

  async function enviar(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!customerId || !ticket.trim()) {
      setError('Selecione um cliente e descreva o problema.')
      return
    }
    setBusy(true)
    setError('')
    if (tab === 'generate') {
      setOutput(null)
      setGeneratedTicket(ticket)
    } else {
      setComparison(null)
      setComparedTicket(ticket)
    }
    try {
      const body = { customer_id: customerId, ticket, content_type: contentType }
      if (tab === 'generate') {
        setOutput(await consultarApi('generate', { ...body, prompt_version: promptVersion }))
      } else {
        setComparison(await consultarApi('compare', body))
      }
    } catch (erro) {
      setError(erro instanceof Error ? erro.message : 'Não foi possível concluir a solicitação.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className={tab === 'evaluation' ? 'chat-layout' : 'chat-layout chat-viewport'}>
      <h1>Support Assistant</h1>
      <nav aria-label="Funcionalidades">
        <button type="button" aria-current={tab === 'generate' ? 'page' : undefined} disabled={busy} onClick={() => selecionarAba('generate')}>Gerar resposta</button>
        <button type="button" aria-current={tab === 'compare' ? 'page' : undefined} disabled={busy} onClick={() => selecionarAba('compare')}>Comparar V1 × V2</button>
        <button type="button" aria-current={tab === 'evaluation' ? 'page' : undefined} disabled={busy} onClick={() => selecionarAba('evaluation')}>Minha avaliação</button>
      </nav>

      <section aria-busy={busy} className={tab !== 'evaluation' ? 'support-panel' : 'evaluation-panel'}>
        <h2>{tab === 'generate' ? 'Gerar resposta' : tab === 'compare' ? 'Comparar V1 × V2' : 'Minha avaliação'}</h2>
        {tab !== 'evaluation' && (
          <>
            <form className="chat-workspace" onSubmit={enviar}>
                <fieldset className="chat-controls" disabled={busy || loadingCustomers || customers.length === 0}>
                <div className="fields">
                  <label>Cliente
                    <select value={customerId} onChange={(event) => setCustomerId(event.target.value)} required>
                      <option value="" disabled>Selecione um cliente</option>
                      {customers.map((customer) => <option key={customer.customer_id} value={customer.customer_id}>{customer.name} ({customer.customer_id}) — {nomeDoPerfil(customer.technical_level)}</option>)}
                    </select>
                  </label>
                  <label>Tipo de conteúdo
                    <select value={contentType} onChange={(event) => setContentType(event.target.value)}>
                      <option value="diagnosis">Diagnóstico</option>
                      <option value="resolution">Resolução</option>
                      <option value="clarification">Perguntas de esclarecimento</option>
                      <option value="flowchart">Fluxograma</option>
                    </select>
                  </label>
                  {tab === 'generate' && <label>Prompt
                    <select value={promptVersion} onChange={(event) => setPromptVersion(event.target.value)}>
                      <option value="v1">V1</option>
                      <option value="v2">V2</option>
                    </select>
                  </label>}
                </div>
                {selectedCustomer && <p className="chat-customer-profile">
                  <span>Nível técnico: {nomeDoPerfil(selectedCustomer.technical_level)}</span>
                  <span>Estilo: {nomeDoPerfil(selectedCustomer.communication_style)}</span>
                  <span>Canal: {nomeDoPerfil(selectedCustomer.channel)}</span>
                </p>}
                </fieldset>
                <div className="chat-messages" role="region" aria-label="Conversa">
                  {loadingCustomers && <p role="status">Carregando clientes…</p>}
                  {customerError && <p role="alert" className="error">{customerError}</p>}
                  {!loadingCustomers && !customerError && customers.length === 0 && <p>Nenhum cliente disponível.</p>}
                  {!(tab === 'generate' ? generatedTicket : comparedTicket) && <div className="chat-empty">
                    <h3>Como podemos ajudar?</h3>
                    <p>Descreva o problema no campo abaixo para {tab === 'generate' ? 'gerar uma resposta de suporte.' : 'comparar as respostas dos prompts V1 e V2.'}</p>
                  </div>}
                  {tab === 'generate' && generatedTicket && <div className="support-conversation">
                    <div className="support-message support-user"><h3>Você</h3><p>{generatedTicket}</p></div>
                    {output !== null && <div className="support-message support-assistant"><h3>Assistente</h3><RespostaAssistente resposta={output} /></div>}
                  </div>}
                  {tab === 'compare' && comparedTicket && <div className="support-conversation">
                    <div className="support-message support-user"><h3>Problema enviado</h3><p>{comparedTicket}</p></div>
                    {comparison && <div className="support-comparison">
                      <div className="support-message support-assistant"><h3>V1 — Básico</h3><RespostaAssistente resposta={comparison.v1} /></div>
                      <div className="support-message support-assistant"><h3>V2 — Aprimorado</h3><RespostaAssistente resposta={comparison.v2} /></div>
                    </div>}
                  </div>}
                  {busy && <p role="status" className="chat-status">Aguardando resposta…</p>}
                  {error && <p role="alert" className="error">{error}</p>}
                </div>
                <fieldset className={tab === 'generate' ? 'chat-composer chat-composer-send' : 'chat-composer'} disabled={busy || loadingCustomers || customers.length === 0}>
                  <label htmlFor="chat-ticket">Problema relatado</label>
                  <textarea id="chat-ticket" value={ticket} onChange={(event) => setTicket(event.target.value)} rows={3} placeholder="Descreva o que está acontecendo…" required />
                  <div className="chat-composer-actions">
                    {tab === 'generate' ? (
                      <button type="submit" className="chat-send" aria-label="Enviar mensagem" disabled={busy || !ticket.trim() || !customerId}>
                        <span aria-hidden="true">↑</span>
                      </button>
                    ) : (
                      <button type="submit" disabled={!ticket.trim() || !customerId}>{busy ? 'Aguarde…' : 'Comparar V1 × V2'}</button>
                    )}
                  </div>
                </fieldset>
            </form>
          </>
        )}
        {tab === 'evaluation' && busy && <p role="status">Aguardando resposta…</p>}
        {tab === 'evaluation' && error && <p role="alert" className="error">{error}</p>}
        {tab === 'evaluation' && <>
          {!busy && !evaluation && <button type="button" onClick={() => void consultarAvaliacao()}>Consultar avaliação</button>}
          {evaluation && <>
            <h3>Notas de avaliação</h3>
            <div className="evaluation-notes">
              {evaluation.notes_markdown.split(/\r?\n\s*\r?\n/).map((bloco, index) => {
                if (bloco.startsWith('## ')) return <h4 key={index}>{formatarNegrito(bloco.slice(3))}</h4>
                if (bloco.startsWith('# ')) return <h3 key={index}>{formatarNegrito(bloco.slice(2))}</h3>
                return <p key={index}>{formatarNegrito(bloco)}</p>
              })}
            </div>
            <h3>Histórico avaliado</h3>
            <div className="evaluation-records">
              {evaluation.history_cli.map((registro) => (
                <article className="evaluation-card" key={registro.id}>
                  <h3>{registro.prompt_version.toUpperCase()}</h3>
                  <dl>
                    <dt>Cliente</dt><dd>{registro.customer_profile.name} ({registro.customer_id})</dd>
                    <dt>Perfil</dt><dd>{registro.customer_profile.technical_level} · {registro.customer_profile.communication_style} · {registro.customer_profile.channel}</dd>
                    <dt>Ticket original</dt><dd>{registro.ticket}</dd>
                    <dt>Versão do prompt</dt><dd>{registro.prompt_version}</dd>
                    <dt>Tipo de conteúdo</dt><dd>{registro.content_type}</dd>
                  </dl>
                  <h4>Avaliação humana</h4>
                  {Object.entries(registro.evaluation).map(([criterio, avaliacao]) => (
                    <div className="evaluation-criterion" key={criterio}>
                      <p><strong>{({ clarity: 'Clareza', customer_fit: 'Adequação ao cliente', actionability: 'Acionabilidade' } as Record<string, string>)[criterio] ?? criterio}: {avaliacao.score}/5</strong></p>
                      <p>{avaliacao.justification}</p>
                    </div>
                  ))}
                  <p><strong>Total: {Object.values(registro.evaluation).reduce((total, item) => total + item.score, 0)}</strong></p>
                  <h4>Resposta da LLM</h4>
                  {([
                    ['hypotheses', 'Hipóteses'],
                    ['evidence', 'Evidências'],
                    ['missing_information', 'Informações faltantes'],
                  ] as const).map(([campo, titulo]) => registro.output[campo] && (
                    <div key={campo}>
                      <h5>{titulo}</h5>
                      <ul>{registro.output[campo].map((texto, index) => <li key={index}>{texto}</li>)}</ul>
                    </div>
                  ))}
                  {registro.output.conclusion !== undefined && <><h5>Conclusão</h5><p>{registro.output.conclusion}</p></>}
                  <details>
                    <summary>Detalhes técnicos / JSON completo</summary>
                    {registro.messages?.map((mensagem, index) => (
                      <div key={index}>
                        <h5>messages[{index}] — {mensagem.role}</h5>
                        <pre>{mensagem.content}</pre>
                      </div>
                    ))}
                    <h5>Registro integral</h5>
                    <pre>{JSON.stringify(registro, null, 2)}</pre>
                  </details>
                </article>
              ))}
            </div>
          </>}
        </>}
      </section>
    </main>
  )
}

export default App
