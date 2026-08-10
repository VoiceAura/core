"""Contrato para o LLM que interpreta o pedido do cliente e gera a resposta."""

from abc import ABC, abstractmethod
from typing import AsyncIterator


class LLMProvider(ABC):
    """Recebe o historico da conversa (e ferramentas disponiveis) e devolve
    a resposta em streaming, token a token."""

    @abstractmethod
    async def stream(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """messages: historico no formato [{"role": ..., "content": ...}, ...]
        tools: schemas das ferramentas disponiveis para function-calling (opcional).
        Devolve: tokens de texto da resposta, incrementalmente.
        """
        ...


class MockLLMProvider(LLMProvider):
    """Implementacao fake -- devolve sempre a mesma resposta canonica."""

    async def stream(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        for token in ["Esta ", "e ", "uma ", "resposta ", "de ", "teste."]:
            yield token
