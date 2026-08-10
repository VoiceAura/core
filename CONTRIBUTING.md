# Como contribuir

## Correr o projeto localmente

1. Copia `.env.example` para `.env`.
2. `docker compose up --build`
3. A API fica disponivel em http://localhost:8000/health

Para so correr testes/lint em Python (sem Docker):

1. `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
2. `pip install -r requirements.txt`
3. `pytest`
4. `ruff check .`

## Branching

- `main` e protegida -- ninguem faz push direto, tudo entra por Pull Request.
- Uma branch por tarefa: `feat/nome-da-tarefa` (ex: `feat/stt-fasterwhisper`).
- Abre o PR assim que tiveres algo a mostrar, mesmo incompleto (marca como Draft).
- O PR so pode ser mergeado com o CI verde (lint + testes a passar) e 1 review.

## Providers (seccao 2.0 do README)

Nunca chames uma biblioteca de STT/LLM/TTS diretamente fora de `/providers`.
Usa sempre a interface abstrata (`STTProvider`, `LLMProvider`, `TTSProvider`, `ToolConnector`)
e o mock correspondente enquanto a implementacao real nao estiver pronta.
