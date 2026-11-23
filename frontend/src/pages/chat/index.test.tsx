import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import ChatPage from './index';
import { sendQuestion, type ChatResult } from '../../modules/chat/chat.service';
vi.mock('../../modules/chat/chat.service', () => ({ sendQuestion: vi.fn() }));
const send = vi.mocked(sendQuestion);
const result: ChatResult = { contexto: 'Texto', fontes: [{ arquivo: 'norma.pdf', pagina: 3, curso: 'IA', trecho: '<script>não executar</script>\nLinha seguinte' }], distancia_minima: 0.2, fallback_acionado: false, resposta: '[SIMULAÇÃO DE INTEGRAÇÃO — NÃO É RESPOSTA ACADÊMICA]' };
beforeEach(() => { send.mockReset().mockResolvedValue(result); });
function submit(text = 'Como solicito segunda chamada?') { fireEvent.change(screen.getByLabelText('Sua pergunta'), { target: { value: text } }); fireEvent.click(screen.getByRole('button', { name: 'Enviar pergunta' })); }
describe('Fluxos da tela SecGrad', () => {
  it('mostra o aviso de simulação e citações com trecho seguro', async () => {
    render(<ChatPage />); submit();
    expect(await screen.findByText(result.resposta!)).toBeInTheDocument();
    expect(screen.getByText(/norma.pdf — página 3/)).toBeInTheDocument();
    expect(screen.getByText(/<script>não executar/)).toBeInTheDocument(); expect(document.querySelector('script')).toBeNull();
  });
  it('usa perfil único para IA e limpa histórico ao mudar contexto', async () => {
    render(<ChatPage />); submit(); await screen.findByText(result.resposta!);
    fireEvent.change(screen.getByLabelText('Curso'), { target: { value: 'Inteligência Artificial' } });
    expect(screen.getByLabelText('Perfil curricular')).toHaveValue('Único Perfil'); expect(screen.queryByText(result.resposta!)).toBeNull();
    submit('Nova pergunta'); await waitFor(() => expect(send).toHaveBeenCalledTimes(2)); expect(send.mock.calls[1][3]).toEqual([]);
  });
  it('renderiza fallback e e-mail sem enviá-lo', async () => {
    send.mockResolvedValue({ ...result, fallback_acionado: true, resposta: undefined, setor_sugerido: 'SecGrad', template_email: 'Olá, preciso de ajuda.' });
    render(<ChatPage />); submit(); expect(await screen.findByText('Olá, preciso de ajuda.')).toBeInTheDocument(); expect(screen.getByText(/Nenhuma mensagem é enviada automaticamente/)).toBeInTheDocument();
  });
  it('exibe erro e permite tentar novamente', async () => {
    send.mockRejectedValueOnce(new Error('Servidor indisponível')); render(<ChatPage />); submit();
    expect(await screen.findByRole('alert')).toHaveTextContent('Servidor indisponível'); expect(screen.getByLabelText('Sua pergunta')).toHaveValue('Como solicito segunda chamada?'); expect(screen.getByRole('button', { name: 'Enviar pergunta' })).toBeEnabled();
    fireEvent.click(screen.getByRole('button', { name: 'Enviar pergunta' }));
    expect(await screen.findByText(result.resposta!)).toBeInTheDocument();
    expect(screen.getAllByLabelText('Mensagem enviada')).toHaveLength(1);
    expect(send.mock.calls[1][3]).toEqual([]);
  });
  it('descarta resposta que chega depois de limpar a conversa', async () => {
    let resolve!: (r: ChatResult) => void; send.mockReturnValue(new Promise((r) => { resolve = r; }));
    render(<ChatPage />); submit(); fireEvent.click(screen.getByRole('button', { name: 'Limpar conversa' }));
    await act(async () => { resolve(result); }); expect(screen.queryByText(result.resposta!)).toBeNull();
  });
});
