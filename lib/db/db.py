from os.path import isfile
import asyncio
import asqlite

DB_PATH = "./data/db/database.db"
BUILD_PATH = "./data/db/build.sql"

async def build():
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            if isfile(BUILD_PATH):
                await scriptexec(BUILD_PATH)

async def commit():
    async with asqlite.connect(DB_PATH) as connection:
        await connection.commit()

async def scriptexec(path):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            with open(path, "r", encoding="utf-8") as script:
                await cursor.executescript(script.read())

async def close():
    async with asqlite.connect(DB_PATH) as connection:
        await connection.close()

async def field(command, *values):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(command, tuple(values))

            if (fetch := await cursor.fetchone()) is not None: 
                return fetch[0]

async def record(command, *values):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(command, tuple(values))
            
            return await cursor.fetchone()

async def records(command, *values):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(command, tuple(values))

            return await cursor.fetchall()

async def column(command, *values):
     async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(command, tuple(values))

            return [item[0] for item in await cursor.fetchall()]

async def execute(command, *values):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(command, tuple(values))

async def multiexec(command, valueset):
    async with asqlite.connect(DB_PATH) as connection:
        async with connection.cursor() as cursor:
            await cursor.executemany(command, valueset)
            
