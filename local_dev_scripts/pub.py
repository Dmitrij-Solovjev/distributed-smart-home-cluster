import asyncio
from nats.aio.client import Client as NATS
from nats.js.errors import APIError, NotFoundError

async def ensure_stream(js, name: str, subjects: list[str]):
    try:
        await js.stream_info(name)
        print(f"Stream '{name}' already exists")
    except NotFoundError:
        await js.add_stream(
            name=name,
            subjects=subjects,
            retention="limits",
            storage="file",
        )
        print(f"Stream '{name}' has been created")
    except APIError as e:
        print(f"APIError occurred: {e}")
        raise

async def run_publisher():
    # 1) Подключаемся к NATS
    nc = NATS()
    await nc.connect(servers=["nats://127.0.0.1:4222"])
    js = nc.jetstream()

    # 2) Убедимся, что поток 'events' существует
    await ensure_stream(js, name="events", subjects=["events"])

    # 3) Публикуем сообщение
    ack = await js.publish("events", b"Hello from Python!")
    print(f"Message published, sequence: {ack.seq}")

    # 4) Закрываем соединение
    await nc.drain()

if __name__ == "__main__":
    asyncio.run(run_publisher())

