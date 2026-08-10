"""Contrato para ferramentas que o agente pode executar (CRM, saldo, etc.)."""

from abc import ABC, abstractmethod


class ToolConnector(ABC):
    """Interface unica para qualquer ferramenta externa (REST, SQL, SOAP legado...)."""

    @abstractmethod
    async def executar(self, parametros: dict) -> dict:
        """parametros: argumentos da chamada (ja validados antes de chegar aqui).
        Devolve: resultado estruturado da acao.
        """
        ...


class MockToolConnector(ToolConnector):
    """Implementacao fake -- devolve sempre sucesso, sem tocar em nenhum sistema real."""

    async def executar(self, parametros: dict) -> dict:
        return {"status": "ok", "parametros_recebidos": parametros, "resultado": {}}
