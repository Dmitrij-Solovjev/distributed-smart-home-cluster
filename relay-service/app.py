# relay-service/app.py
# https://medium.com/@denis.volokh/event-driven-application-in-python-using-nats-bfe7a22c13d4

import asyncio
from nats.aio.client import Client as NATS

async def run():
    nats = NATS()

    # Connect to the NATS server
    await nats.connect("nats://localhost:4222")

    # Publishing a message
    subject = "events.updates"
    message = "Hello, NATS!"
    await nats.publish(subject, message.encode())

    print(f"Published message: {message} to {subject}")

    # Close the connection to the server
    await nats.close()

if __name__ == "__main__":
    asyncio.run(run())
