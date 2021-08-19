from . import db
import asyncio

async def build_db():
    await db.build()

loop = asyncio.get_event_loop()
loop.run_until_complete(build_db())
