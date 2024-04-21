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

## Ban User Module
async def ban_list(data):
   room_id = data["room_id"]
   rooms = await cmd.all_rooms()
   room_name = rooms[room_id-1]
   file_name = f"rooms/{room_name}"
   async with aiofiles.open(file_name, 'r') as f:
     data = json.loads(await f.read())
   banned_user = data['banned']
   list_user = "\nBanned User\n"
   for index, element in enumerate(banned_user, 1):
    list_user += f'[{index}] {element}\n'
   data = {"message":list_user,"file_name":file_name}
   await cmd.system_message(data)
async def ban(data,email):
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
  async with aiofiles.open("database/rooms.json", 'r') as f:
   room_name = json.loads(await f.read())
  owner = room_data["owner"].lower()
  username = await cmd.get_username_local(email)
  username = username.lower()
  async with aiofiles.open("database/user.json", 'r') as f:
     data = json.loads(await f.read())
  usernames = [info["username"].lower() for email, info in data.items()]
  if args.lower() not in usernames:
    print("Hey")
    data = {'message':'Username Not Found',"file_name":file_name}
    return await cmd.system_message(data,success=False)
  if username != owner:
    data = {'message':'Only Owner Can Ban User',"file_name":file_name}
    return await cmd.system_message(data,success=False)
  if args.lower() == owner.lower():
    data = {'message':"You Can't Ban Owner","file_name":file_name}
    return await cmd.system_message(data,success=False)
  if args.lower() == username:
    data = {"message":"You Can't Ban Yourself","file_name":file_name}
    return await cmd.system_message(data,success=False)
  if args.lower() in banned_list:
    data = {"message":"User Already Banned","file_name":file_name}
    return await cmd.system_message(data,success=False)
  else:
   room_data["banned"].append(args)
   async with aiofiles.open(file_name, 'w') as f:
     await f.write(json.dumps(room_data))
   data = {"message":f"{args} Has Been Banned","file_name":file_name}
   await cmd.system_message(data)