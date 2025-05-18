import os
import time
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
    data = msg.data.decode()
    print(f"Received message on '{msg.subject}': {data}")
    sender_id = data.split()[-1]
    own_id = os.environ.get("NODE_ID").split('-')[-1]
    if sender_id != own_id:
        response = f"Hello from {own_id} to {sender_id}"
        await msg._client.publish("retr_msg", response.encode())
        print(f"Sent response: {response}")
        time.sleep(1);

async def main():
    nats_url = os.environ.get("NATS_URL", "nats://localhost:4222")
    own_id = os.environ.get("NODE_ID").split('-')[-1]

    nc = NATS()
    await nc.connect(servers=[nats_url])
    js = nc.jetstream()

    await ensure_stream(js, name="retr_msg", subjects=["retr_msg"])

    await js.subscribe("retr_msg", cb=message_handler)

    # Send initial message to the other node
    target_id = "1" if own_id == "0" else "0"
    message = f"Hello from {own_id} to {target_id}"

    await js.publish("retr_msg", message.encode())
    print(f"Sent message: {message}")

    print("Waiting for messages...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
