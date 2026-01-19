import asyncio
from nano_wait import wait_async

async def main():
    print("Início do wait_async")
    result = await wait_async(2, smart=False, speed="slow")
    print(f"Esperou: {result} segundos")

asyncio.run(main())
