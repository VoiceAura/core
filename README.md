# Voice-Agents — Visão, Arquitetura

*Documento de apresentação - equipa de 6, orçamento zero, validação inicial em Angola.*

**Como usar este documento:** serve para dois momentos — o guião da apresentação, e a referência que qualquer um dos 6 vai abrir na primeira semana de trabalho. A secção 2.0 é a mais importante do documento inteiro vale a pena ler duas vezes antes de escrever a primeira linha de código.

---

## 1.Visão

Não estamos a construir "mais um chatbot de voz." Estamos a construir um motor de conversa por voz que tenta chegar o mais perto possível do nível humano: uma voz que ninguém consegue dizer com certeza se é IA pausas naturais, sabe ouvir, deixa-se interromper, interrompe quando faz sentido. Esse motor ganha depois uma segunda capacidade: ouvir uma voz humana por pouco tempo (15-30 segundos, na prática) e clonar essa voz a um nível em que nem o próprio dono a distingue da versão gerada pela IA.

Só depois de termos esse motor a passar por humano é que ele se ramifica para o primeiro caso de uso real: **call center**. capaz de fazer ações a nivel do sistema da empresa que nos contratou ex: Consultar saldo, validar identidade etc. Também vamos a call centers reais pedir as bases de diálogo atendente-cliente deles, para afinar os modelos ao nosso caso de uso.

**Na prática, hoje:**
- **Orçamento:** zero. Toda a stack é open source (secção 3).
- **Validação:** primeiro em Angola. Ambição de crescer depois.
- **Código:** open source desde o início.
- **Equipa:** 6 pessoas, todas com Python/FastAPI/Django.

---

## 2. Arquitetura

### 2.0 A regra de ouro: tudo o que "ouve e fala" é substituível

Isto aplica-se aos 6, não só a quem mexe em STT/LLM/TTS:

> **Construímos o que decide e lembra** — orquestração, memória, contexto, ferramentas. É a nossa propriedade intelectual. **O que ouve e fala é peça trocável** — STT, LLM, TTS. Hoje open source, amanhã possivelmente pago ou construído por nós, sempre por trás da mesma interface.

Três regras simples, sem exceção:

```python
from abc import ABC, abstractmethod

class STTProvider(ABC):
    @abstractmethod
    async def stream(self, audio_chunks): ...

class LLMProvider(ABC):
    @abstractmethod
    async def stream(self, messages, tools): ...

class TTSProvider(ABC):
    @abstractmethod
    async def stream(self, text_chunks): ...
```

1. Estas três classes abstratas (mais `ToolConnector`, secção 2.2) são o único ponto de entrada para falar com STT/LLM/TTS. Não existe segundo caminho.
2. Um ficheiro de configuração por ambiente/cliente decide qual implementação concreta carrega (`WhisperSTTProvider`, `QwenLLMProvider`...) — nunca espalhado pelo código.
3. **Nenhum código de negócio chama `whisper.transcribe()`, uma API de LLM, ou equivalente diretamente.** Se aparecer isso num pull request, é para rejeitar, não para "resolver depois."

É isto que nos permite trocar Whisper por um STT pago, ou Qwen por outro LLM, daqui a 6 meses sem tocar em orquestração, ferramentas ou regras de negócio — muda o ficheiro de configuração, mais nada.

### 2.1 Visão geral do sistema

Canais de entrada: o cliente comunica por telefone, WhatsApp ou navegador.
Voice Orchestrator (propriedade intelectual): recebe a conversa, gere as sessões, deteta quando cada participante fala, permite interrupções naturais e encaminha cada pedido para o cliente correto.
Camada de IA (commodity): converte voz em texto (STT), o LLM interpreta o pedido e gera a resposta, e o TTS converte a resposta novamente em voz. Estes componentes podem ser trocados por modelos melhores sem alterar a arquitetura.
Contexto e ferramentas (propriedade intelectual): o agente consulta a base de conhecimento do cliente, aplica regras de negócio, executa ações (como consultar um CRM) e, se a ação for sensível, envia-a para aprovação humana antes de a executar.

Além disso, existe um módulo (muito importante) de clonagem de voz para demonstrações, que utiliza uma amostra de voz com humana real.

O principal diferencial da plataforma está na orquestração das conversas, na gestão do contexto, nas regras de negócio e nas integrações, e não nos modelos de IA utilizados.

| Etapa | Alvo |
|---|---|
| VAD (fim de turno) | 100-150ms |
| STT (primeiro texto) | 150-300ms |
| LLM (primeiro token) | 150-300ms |
| TTS (primeiro áudio) | 100-200ms |
| Rede/jitter | 50-100ms |
| **Total realista** | **550-1050ms** |

### 2.2 Camada de Ferramentas (Context + Tools(Depois do MVP))

Cada cliente empresarial configura as suas próprias ferramentas sem tocar no núcleo:

1. **Manifesto por cliente** (YAML/JSON) — ferramentas ativas, endpoints, credenciais (cofre de segredos, nunca texto simples), coleção de RAG associada.
2. **`ToolConnector` abstrato** — interface única (`executar(parametros) -> resultado`), com implementações concretas por tipo de sistema (REST, SQL com allowlist, SOAP legado se preciso).
3. **Isolamento por tenant** — não é só um filtro `cliente_id`; coleções/schemas separados no pgvector e credenciais separadas, para um bug de código nunca vazar dados entre clientes.

**Prompt em duas camadas:** estática por cliente (persona, tom de marca, regras inegociáveis, quando escalar) e dinâmica por turno (resumo do estado — não o transcript completo — mais resultados de RAG e schemas das ferramentas disponíveis). Prompt curto = latência mais baixa, não só custo mais baixo.

**Estado da conversa em Redis**, por sessão, como objeto estruturado — nunca o histórico bruto:

```json(exemplo)
{
  "session_id": "...",
  "cliente_id": "...",
  "intents_visitados": ["consultar_saldo"],
  "pendente_confirmacao": null,
  "ultimo_resumo_conversa": "Cliente confirmou identidade, perguntou saldo..."
}
```

**Fine-tuning:** LoRA/QLoRA sobre o Qwen base (Axolotl ou LLaMA-Factory, ambos grátis). Prioridade do primeiro fine-tune: fidelidade ao formato de function-calling e saber quando recusar/escalar — os dois erros mais caros num call center automático são inventar informação e executar uma ação que não devia.

### 2.3 Aprovação de ações sensíveis — os dois mecanismos

Duas camadas de proteção:

1. **Confirmação do cliente, dentro da própria chamada.** Para qualquer ação que altera algo, o agente pede confirmação verbal explícita antes de agir — *"Confirma que quer suspender o serviço X?"*. Garante que a intenção do cliente ficou clara e registada.
2. **Fila de aprovação humana, para ações de alto risco.** Transferências, reembolsos grandes, e o que a equipa definir como "alto risco" por cliente não executam logo após a confirmação do cliente — ficam em stand-by numa fila que um funcionário humano revê e aprova (ou rejeita) antes do executor tocar no sistema real.

*Nota: isto é trabalho a mais do que uma confirmação só — mas como é dinheiro real a mover-se num cenário de banco, vale bem o esforço extra .*

### 2.4 Demo de Clonagem de Voz

Captura da voz
O cliente grava uma pequena amostra de voz (15–30 segundos).
O áudio é enviado e guardado temporariamente de forma encriptada.
Extração da voz
O OpenVoice v2 analisa a amostra e cria um embedding de voz (características da voz, como timbre).
Esse embedding permite ao TTS reproduzir uma voz semelhante.
Uso durante a demo
O agente continua a funcionar normalmente com STT + LLM.
Apenas a saída de voz é alterada para usar a voz clonada do cliente.

## 3. Stack Tecnológica + Licenças

Tudo abaixo é grátis e open source. As duas exceções reais de custo estão na secção 3.6.

### 3.1 STT — Speech-to-Text

| Opção | Licença | Porquê |
|---|---|---|
| **faster-whisper (distil-large-v3)** — recomendado | MIT | Multilingue robusto incl. português, 4-6x mais rápido que Whisper vanilla, corre em GPU de 4-6GB |
| Vosk | Apache 2.0 | Streaming nativo, CPU-only — qualidade em português é inferior |
| Voxtral (Mistral) | Apache 2.0 | Streaming nativo 80ms-2.4s — confirmar cobertura de português antes de apostar |

### 3.2 LLM

| Opção | Licença | Porquê |
|---|---|---|
| **Qwen 2.5/3 (7-14B)** — recomendado | Apache 2.0 | Melhor cobertura multilingue open source, function-calling nativo forte |
| Llama 3.3 | Meta, comercial livre até 700M utilizadores/mês | Tooling mais maduro (Axolotl, vLLM) |
| Mistral Small/Large 3 | Apache 2.0 | Forte em português europeu |

Serving: **vLLM** (continuous batching, atende várias chamadas em paralelo). Quantização AWQ/GGUF int4/int8 reduz VRAM 2-4x — testar sempre com diálogos próprios, não confiar em benchmarks genéricos.

### 3.3 TTS

| Opção | Licença | Uso |
|---|---|---|
| **Kokoro-82M** — voz padrão | Apache 2.0 | Leve, corre até em CPU, inclui português (validar sotaque com utilizadores angolanos) |
| Piper — fallback | Verificar por voz | 30+ línguas, hardware muito modesto |

**⚠️ Não usar em produção comercial:** XTTS v2 (Coqui) e F5-TTS aparecem em quase todos os tutoriais de "clonagem grátis" — ambos são licença **não-comercial** (CPML / CC-BY-NC). Ótima qualidade, mas ilegal de usar comercialmente sem pagar — e a Coqui Inc. fechou em 2024, por isso nem há hoje quem venda a licença comercial do XTTS.

### 3.4 Clonagem de Voz

**OpenVoice v2** (MyShell, MIT desde abril 2024) — a única opção séria totalmente livre para uso comercial hoje. Clona a partir de 1-5 segundos de referência, separa tom de voz de estilo de fala. Com Pipecat/LiveKit: 500-1000ms ponta-a-ponta — bom para o "uau" da demo, não é tempo real perfeito.

### 3.5 Orquestração e Telefonia

**LiveKit (self-hosted, Apache 2.0) + Pipecat (Apache 2.0)** — a decisão mais arriscada da stack, porque é onde a equipa tem menos experiência. Desde 2026 o LiveKit tem SIP nativo — não precisamos de Twilio/Asterisk só para atender chamadas reais.

*Alternativa mais simples para começar:* se o self-hosted (Kubernetes/Docker, TURN/STUN, certificados) atrasar demasiado a semana 1, é legítimo começar com Pipecat sobre o transporte Daily (tier grátis generoso) e migrar para self-hosted quando o volume justificar.

### 3.6 Onde o "grátis" tem limites

Duas exceções reais de custo — o resto é genuinamente $0 de software:
1. **Linha de telefone real (PSTN).** Nenhuma operadora entrega chamadas reais de graça — precisa de um trunk SIP/DID que cobra por minuto ou por número. Manter mínimo (1 número de teste) até haver volume.
2. **GPU em escala.** Uma GPU de consumo (RTX 3060/4070, 8-12GB) chega para o MVP, com $0 além de eletricidade. Deixa de chegar quando for preciso atender várias chamadas simultâneas — aí entra GPU cloud, ainda barato comparado a APIs pagas por chamada.

### 3.7 Ferramentas e Dados

- Tool-calling nativo do LLM (Qwen/Llama já suportam) — **não usar LangChain em produção** para isto; a camada extra de abstração custa mais em debugging do que poupa em código.
- **pgvector** (extensão PostgreSQL) para RAG — a equipa já conhece Postgres, evita introduzir mais um sistema.
- **Redis** para estado de sessão (secção 2.2) e TTL da clonagem de voz (secção 2.4).
- **WhatsApp Cloud API** (Meta) — acesso técnico grátis, primeiras 1.000 conversas/mês grátis, depois custo por conversa.

---
## 4. Roadmap + Divisão de Responsabilidades (6 pessoas)

### 4.1 MVP — 2 meses

**Critério de sucesso**

Ao final de 2 meses, a equipa deverá entregar uma aplicação web funcional capaz de demonstrar um sistema completo de conversação por voz baseado em IA, utilizando exclusivamente modelos open source, sem necessidade de fine-tuning nesta fase.

O MVP deverá incluir:

- Conversação por voz em tempo real entre utilizador e IA.
- Conversão de voz para texto (Speech-to-Text) em streaming.
- Geração de respostas utilizando um LLM sem fine-tuning.
- Conversão de texto para voz (Text-to-Speech) com elevada naturalidade, procurando uma voz o mais próxima possível da fala humana.
- Um módulo de clonagem de voz onde seja possível:
  - gravar ou enviar uma amostra de voz;
  - gerar uma voz clonada;
  - utilizar essa voz como voz principal do assistente;
  - guardar múltiplas vozes clonadas;
  - selecionar qualquer voz armazenada para futuras conversas;
  - utilizar qualquer voz clonada para converter texto em fala.
- Interface web simples para testar todas estas funcionalidades.

Nesta fase o foco será validar a arquitetura, a qualidade da conversa, a latência do sistema e a qualidade da síntese de voz. O objetivo não é inteligência especializada, mas sim construir uma base sólida sobre a qual versões futuras poderão adicionar fine-tuning, RAG, ferramentas, integrações empresariais e funcionalidades avançadas.

### 4.2 Divisão de Responsabilidades (6 pessoas)

| Pessoa | Responsabilidade |
|--------|------------------|
| Dev A | Frontend Web, interface de conversação, gestão das vozes clonadas e integração WebRTC. |
| Dev B | Pipeline de áudio, STT, streaming e gestão da comunicação em tempo real. |
| Dev C | Integração do LLM, gestão de contexto e orquestração da conversa. |
| Dev D | Sistema TTS, clonagem de voz, armazenamento e seleção das vozes. |
| Dev E | Backend (FastAPI/Django), autenticação, APIs e persistência dos dados. |
| Alassana Djigo | Infraestrutura, Docker, CI/CD, monitorização, testes e deploy. |
