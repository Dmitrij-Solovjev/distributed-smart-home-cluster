import os
import asyncio
from nats.aio.client import Client as NATS
from nats.js.errors import NotFoundError

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

async def message_handler(msg):
    sender_id = msg.data.decode().split()[-1]
    own_id = os.environ.get("NODE_ID")
    if sender_id != own_id:
        print(f"Received message: {msg.data.decode()}")
        response = f"Hello from {own_id} to {sender_id}"
        await msg.respond(response.encode())

async def main():
    node_id = os.environ.get("NODE_ID")
    nats_url = os.environ.get("NATS_URL", "nats://localhost:4222")

    nc = NATS()
    await nc.connect(servers=[nats_url])
    js = nc.jetstream()

    await ensure_stream(js, name="retr_msg", subjects=["retr_msg"])

    await nc.subscribe("retr_msg", cb=message_handler)

    # Отправляем приветственное сообщение
    target_id = "2" if node_id == "1" else "1"
    message = f"Hello from {node_id} to {target_id}"
    await js.publish("retr_msg", message.encode())

    print(f"Node {node_id} is running and awaiting messages...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
