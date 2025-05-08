import nats
import asyncio

async def main():
    nc = await nats.connect("nats://nats-broker:4222")
    await nc.publish("retranslate_msg", b'{"message": "Hello from relay service!"}')
    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())

