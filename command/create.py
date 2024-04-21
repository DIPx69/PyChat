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

## Create Room Stuff

@app.route('/create', methods=['POST'])
async def create():
  payload_client = await request.form
  room_name = payload_client.get("room_name", " ")   
  email = payload_client.get("email", " ").lower()
  key = payload_client.get("key", "")
  hashing_password = hashlib.sha256(key.encode("utf-8")).hexdigest()
  async with aiofiles.open("database/rooms.json", 'r') as f:
    rooms = json.loads(await f.read())
  roomsx = [room.lower() for room in rooms]
  async with aiofiles.open("database/user.json", 'r') as f:
     data = json.loads(await f.read())
  if email in data:
     user_info = data[email]
     server_password = user_info["password"]
     username = user_info["username"]
  else:
    return jsonify({"message":"Email Doesn't Exist"}),401
  if not (4 <= len(room_name) <= 10):
    return jsonify({'message': 'Length Requirement (between 4 and 10 characters)'}),402
  if room_name.lower() in roomsx:
    return jsonify({"message":"Room Name Already Exist"}),402
  if room_name.isspace():
     return jsonify({"message":"Room Name Cannot Be Empty"}),402
  if room_name == "":
     return jsonify({"message":"Room Name Cannot Be Empty"}),402
  if "‎" in room_name:
     return jsonify({"message":"Room Name Cannot Be Contain Invincible Character"}),402
  if room_name.startswith(" "):
     return jsonify({"message":"Room Name Cannot Be Starts With Space"}),402
  if server_password == hashing_password:
    filename = f"rooms/{room_name}"
    timestamp = int(time.time())
    data = {"banned":[],"muted":[],"room_name": room_name, "owner": username, "messages": {"2": {"name": "PyChatBot", "message": f"Room Created By {username}", "timestamp": timestamp},"1": {"name": "D1P", "message": f"Hi Ami Dip. Ami PyChat er Brainless Lead Programmer\nEita Amar 1st API Project and Command Line Project\n", "timestamp": timestamp}
    }}
    rooms.append(room_name)
    async with aiofiles.open("database/rooms.json", 'w') as f:
         await f.write(json.dumps(rooms))
    async with aiofiles.open(filename, 'w') as f:
         await f.write(json.dumps(data))
    return jsonify({"message":"Room Has Been Created"})
  else:
    return jsonify({"message":"Password Did Not Matched"}),401