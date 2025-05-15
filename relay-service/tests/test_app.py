'''

import asyncio
import pytest

# Импортируем main из вашего приложения
from app import main

class DummyNC:
    async def publish(self, *args, **kwargs):
        pass

    async def close(self):
        pass

async def dummy_connect(url):
    # Проверим, что URL передаётся правильно, если нужно
    assert url.startswith("nats://")
    return DummyNC()

@pytest.mark.asyncio
async def test_main_runs(monkeypatch):
    # Заменяем nats.connect на заглушку
    monkeypatch.setattr("nats.connect", dummy_connect)
    # Должен завершиться без исключений
    await main()

'''
