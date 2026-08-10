"""Contrato para conversao de voz em texto (Speech-to-Text).

Implementacoes reais (ex: FasterWhisperProvider) vivem em ficheiros
separados dentro deste mesmo pacote. Nenhum codigo fora de /providers
deve chamar uma biblioteca de STT diretamente -- so atraves desta interface.
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator


class STTProvider(ABC):
    """Recebe audio em streaming e devolve texto transcrito, tambem em streaming."""

    @abstractmethod
    async def stream(self, audio_chunks: AsyncIterator[bytes]) -> AsyncIterator[str]:
        """audio_chunks: chunks de audio (bytes) a chegar em tempo real.
        Devolve: texto transcrito, incrementalmente (pode ser palavra a palavra).
        """
        ...


class MockSTTProvider(STTProvider):
    """Implementacao fake -- nao depende de nenhum modelo real.
    Serve para quem estiver a construir contra esta interface testar
    sem esperar pela implementacao real (FasterWhisperProvider).
    """

    async def stream(self, audio_chunks: AsyncIterator[bytes]) -> AsyncIterator[str]:
        for palavra in ["Ola", "isto", "e", "uma", "transcricao", "de", "teste"]:
            yield palavra
