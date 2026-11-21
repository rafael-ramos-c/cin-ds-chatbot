import { useEffect, useRef, useState } from 'react';
import { sendQuestion, type Message } from '../../modules/chat/chat.service';
import './chat.css';

const courses = ['Ciência da Computação', 'Engenharia da Computação', 'Sistemas de Informação', 'Inteligência Artificial'];
const normalProfiles = ['Perfil Novo / Vigente', 'Perfil Antigo'];

export default function ChatPage() {
  const [course, setCourse] = useState(courses[0]);
  const [profile, setProfile] = useState(normalProfiles[0]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const pending = useRef<AbortController | null>(null);
  const last = useRef<HTMLDivElement | null>(null);
  useEffect(() => () => pending.current?.abort(), []);
  useEffect(() => { last.current?.scrollIntoView?.({ behavior: 'smooth' }); }, [messages, busy]);

  function reset() {
    pending.current?.abort(); pending.current = null;
    setBusy(false); setMessages([]); setError(''); setQuestion('');
  }
  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!question.trim() || busy) return;
    const text = question.trim();
    const controller = new AbortController(); pending.current = controller;
    setBusy(true); setError(''); setQuestion('');
    setMessages((m) => [...m, { role: 'user', content: text }]);
    try {
      const result = await sendQuestion(text, course, profile, messages, controller.signal);
      if (controller.signal.aborted) return;
      setMessages((m) => [...m, { role: 'assistant', content: result.resposta ?? '', result }]);
    } catch (err) {
      if (!controller.signal.aborted) {
        setError(err instanceof Error && err.name === 'TimeoutError' ? 'O servidor demorou para responder. Tente novamente.' : err instanceof Error ? err.message : 'Falha de conexão com o servidor.');
        setQuestion(text);
      }
    } finally {
      if (pending.current === controller) { pending.current = null; setBusy(false); }
    }
  }

  return <main className="secgrad-chat">
    <header><h1>Assistente SecGrad CIn</h1><p>Tire dúvidas sobre procedimentos acadêmicos com referências documentais.</p></header>
    <aside className="secgrad-notice">Para decisões administrativas formais, consulte a documentação oficial ou a secretaria. O modo de simulação é identificado nas respostas e não fornece orientação acadêmica gerada por IA.</aside>
    <section className="secgrad-settings" aria-label="Contexto do aluno">
      <label>Curso<select value={course} onChange={(e) => { reset(); setCourse(e.target.value); setProfile(e.target.value === 'Inteligência Artificial' ? 'Único Perfil' : normalProfiles[0]); }}>
        {courses.map((c) => <option key={c}>{c}</option>)}
      </select></label>
      <label>Perfil curricular<select value={profile} onChange={(e) => { reset(); setProfile(e.target.value); }}>
        {(course === 'Inteligência Artificial' ? ['Único Perfil'] : normalProfiles).map((p) => <option key={p}>{p}</option>)}
      </select></label>
      <button type="button" onClick={reset}>Limpar conversa</button>
    </section>
    <section className="secgrad-messages" aria-label="Conversa" aria-live="polite" aria-relevant="additions">
      {!messages.length && <p>Olá! Selecione seu curso e perfil e escreva sua pergunta. O histórico desta conversa permanece apenas nesta sessão da tela.</p>}
      {messages.map((message, i) => <article key={i} className={`secgrad-message ${message.role}`} aria-label={message.role === 'user' ? 'Mensagem enviada' : 'Resposta do assistente'}>
        <strong>{message.role === 'user' ? 'Você' : 'SecGrad'}</strong>
        {message.result?.fallback_acionado ? <>
          <p>Não foram encontradas evidências suficientes para responder com precisão.</p>
          <p>Setor recomendado: <strong>{message.result.setor_sugerido}</strong></p>
          <p>Modelo de e-mail para você revisar e enviar. Nenhuma mensagem é enviada automaticamente.</p>
          <pre className="secgrad-email">{message.result.template_email}</pre>
        </> : <p className="secgrad-answer">{message.content || 'Consulta concluída. Não foi recebida uma resposta gerada.'}</p>}
        {!!message.result?.fontes.length && <details>
          <summary>Fontes e trechos recuperados ({message.result.fontes.length})</summary>
          <p className="secgrad-caption">A recuperação, por si só, não confirma que um trecho responda à pergunta. Confira a página indicada.</p>
          {message.result.fontes.map((source, j) => <section key={j} className="secgrad-source">
            <h2>{source.arquivo} — página {source.pagina}</h2>
            <p className="secgrad-caption">{source.curso}</p>
            <p className="secgrad-excerpt">{source.trecho || 'Trecho não disponível; consulte o documento original.'}</p>
          </section>)}
        </details>}
      </article>)}
      {busy && <p role="status">Consultando os documentos…</p>}
      <div ref={last} />
    </section>
    {error && <p role="alert" className="secgrad-error">{error}</p>}
    <form onSubmit={submit} className="secgrad-input">
      <label htmlFor="question">Sua pergunta</label>
      <textarea id="question" value={question} maxLength={2000} rows={3} onChange={(e) => setQuestion(e.target.value)} placeholder="Ex.: Como solicito segunda chamada de prova?" disabled={busy} />
      <button type="submit" disabled={busy || !question.trim()}>Enviar pergunta</button>
    </form>
  </main>;
}
