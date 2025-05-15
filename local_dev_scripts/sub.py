import asyncio
from nats.aio.client import Client as NATS

async def message_handler(msg):
    print(f"Получено сообщение на '{msg.subject}': {msg.data.decode()}")

async def main():
    nc = NATS()
    await nc.connect("nats://localhost:4222")

    # Подписка на топик 'events' с асинхронным обработчиком
    await nc.subscribe("events", cb=message_handler)

    print("Ожидание сообщений...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
