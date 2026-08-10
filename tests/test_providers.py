from providers.llm import MockLLMProvider
from providers.stt import MockSTTProvider
from providers.tools import MockToolConnector
from providers.tts import MockTTSProvider


async def test_mock_stt_provider():
    provider = MockSTTProvider()
    resultado = [chunk async for chunk in provider.stream(audio_chunks=iter([]))]
    assert len(resultado) > 0
    assert all(isinstance(c, str) for c in resultado)


async def test_mock_llm_provider():
    provider = MockLLMProvider()
    mensagens = [{"role": "user", "content": "ola"}]
    resultado = [chunk async for chunk in provider.stream(messages=mensagens)]
    assert len(resultado) > 0
    assert all(isinstance(c, str) for c in resultado)


async def test_mock_tts_provider():
    provider = MockTTSProvider()
    resultado = [chunk async for chunk in provider.stream(text_chunks=iter(["ola"]))]
    assert len(resultado) > 0
    assert all(isinstance(c, bytes) for c in resultado)


async def test_mock_tool_connector():
    connector = MockToolConnector()
    resultado = await connector.executar(parametros={"exemplo": 1})
    assert isinstance(resultado, dict)
    assert resultado["status"] == "ok"
