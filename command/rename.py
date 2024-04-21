import os
import time
import json
import aiofiles
import asyncio
import hashlib
import re
from quart import Quart, jsonify, request,render_template
from quart_rate_limiter import *
from main import app
import command as cmd

## Rename Module

async def rename(data,email):
  room_id = data["room_id"]
  email = data["email"]
  parts = data['message'].split()
  command = parts[0][1:].lower()
  args = " ".join(parts[1:])
  rooms = await cmd.all_rooms()
  room_name = rooms[room_id-1]
  file_name = f"rooms/{room_name}"
  new_name = f"rooms/{args}"
  async with aiofiles.open(file_name, 'r') as f:
   data = json.loads(await f.read())
  async with aiofiles.open("database/rooms.json", 'r') as f:
   room_name = json.loads(await f.read())
  owner = data["owner"].lower()
  username = await cmd.get_username_local(email)
  username = username.lower()
  rooms = os.listdir("rooms")
  roomsx = [os.path.splitext(filename.lower())[0] for filename in rooms]
  if username != owner:
    data = {'message':'Only Owner Can Change Room Name',"file_name":file_name}
    return await cmd.system_message(data,success=False)
  if not (4 <= len(args) <= 10):
    data = {'message':'Length Requirement (between 4 and 10 characters)',"file_name":file_name}
    return await cmd.system_message(data,success=False)
  if args.lower() in roomsx:
    data = {"message":"Room Name Already Exist","file_name":file_name}
    return await cmd.system_message(data,success=False)
  os.rename(file_name,new_name)
  timestamp = int(time.time())
  print(f"Change {room_name[room_id-1]} To {args}")
  room_name[room_id-1] = args
  async with aiofiles.open("database/rooms.json", 'w') as f:
     await f.write(json.dumps(room_name))
  data = {"message":f"Room Name Has Been Changed To {args}","args":args,"file_name":new_name}
  await cmd.system_message(data,success=True)