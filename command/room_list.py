import os
import json
import aiofiles
## Room List From File 

async def all_rooms():
   async with aiofiles.open("database/rooms.json", 'r') as f:
    rooms = json.loads(await f.read())
   return rooms