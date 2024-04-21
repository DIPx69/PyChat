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

## Unban User Module

async def unban(data,email):
  room_id = data["room_id"]
  email = data["email"]
  parts = data['message'].split()
  command = parts[0][1:].lower()
  args = " ".join(parts[1:])
  rooms = await cmd.all_rooms()
  room_name = rooms[room_id-1]
  file_name = f"rooms/{room_name}"
  async with aiofiles.open(file_name, 'r') as f:
   room_data = json.loads(await f.read())
  banned_list = [user.lower() for user in room_data["banned"]]
  try:
   index = int(args)-1
   args = banned_list[index]
  except:
    ...
  async with aiofiles.open("database/rooms.json", 'r') as f:
   room_name = json.loads(await f.read())
  owner = room_data["owner"].lower()
  username = await cmd.get_username_local(email)
  username = username.lower()
  if username != owner:
    data = {'message':'Only Owner Can Unban User',"file_name":file_name}
    return await cmd.system_message(data,success=False)
  if args.lower() in banned_list:
    data = {"message":"User Already Unbanned","file_name":file_name}
    room_data["banned"] = [ban_user.lower() for ban_user in room_data["banned"] if ban_user.lower() != args.lower()]
    async with aiofiles.open(file_name, 'w') as f:
     await f.write(json.dumps(room_data))
     data = {"message":f"{args} Has Been Unbanned","file_name":file_name}
    return await cmd.system_message(data)
  else:
   data = {"message":f"Username Not Found","file_name":file_name}
   await cmd.system_message(data)