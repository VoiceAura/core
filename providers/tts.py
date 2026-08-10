"""Contrato para conversao de texto em voz (Text-to-Speech)."""

from abc import ABC, abstractmethod
from typing import AsyncIterator


class TTSProvider(ABC):
    """Recebe texto (em chunks) e devolve audio em streaming."""

    @abstractmethod
    async def stream(self, text_chunks: AsyncIterator[str]) -> AsyncIterator[bytes]:
        """text_chunks: texto a sintetizar, incrementalmente.
        Devolve: chunks de audio (bytes), incrementalmente.
        """
        ...


class MockTTSProvider(TTSProvider):
    """Implementacao fake -- devolve bytes fixos, so para validar o pipeline."""

    async def stream(self, text_chunks: AsyncIterator[str]) -> AsyncIterator[bytes]:
        for _ in range(3):
            yield b"\x00\x01\x02\x03"
