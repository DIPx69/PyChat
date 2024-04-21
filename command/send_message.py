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
import command
## Send Message

@app.route('/send_message', methods=['POST'])
async def send_message():
  payload_client = await request.form
  message = payload_client.get("message", " ")
  email = payload_client.get("email", " ").lower()
  key = payload_client.get("key", "")
  try:
   room_id = int(payload_client.get("id", ""))
  except:
    return jsonify({"message":"Room Doesn't Exist"}),404
  hashing_password = hashlib.sha256(key.encode("utf-8")).hexdigest()
  async with aiofiles.open("database/user.json", 'r') as f:
       data = json.loads(await f.read())
  if email in data:
     user_info = data[email]
     server_password = user_info["password"]
     username = user_info["username"]
  else:
    return jsonify({"message":"Email Doesn't Exist"}),400
  if message.isspace():
     return jsonify({"message":"Message Cannot Be Empty"}),402
  if server_password == hashing_password:
     timestamp = int(time.time())
     new_message = {"name":username,"message":message,"timestamp":timestamp}
     rooms = await command.all_rooms()
     room_name = rooms[room_id-1]
     filename = f"rooms/{room_name}"
     async with aiofiles.open(filename, 'r') as f:
       data = json.loads(await f.read())
     ban_list = [username.lower() for username in data["banned"]]
     mute_list = [username.lower() for username in data["muted"]]
     if username.lower() in ban_list:
       return jsonify({"message":"Sorry, your account is banned from this chat room"}),404
     if username.lower() in mute_list:
       return jsonify({"message":"Sorry, your account is muted from this chat room"}),402
     data["messages"] = {str(int(key)+1): message for key, message in data["messages"].items()}
     data["messages"]["1"] = new_message
     if len(data["messages"]) >= 11:
       del data["messages"]["11"]
     sorted_messages = sorted(data['messages'].items(), key=lambda x: int(x[0]))
     sorted_messages_dict = {k: v for k, v in sorted_messages}
     data['messages'] = sorted_messages_dict
     async with aiofiles.open(filename, 'w') as f:
         await f.write(json.dumps(data))
     if message.startswith("/"):
       datax = {"room_id":room_id,"message":message,"email":email,"file_name":"rooms/" +room_name}
       await command.slash_command(datax)
     return data
  else:
     return jsonify({"message":"Password Did Not Matched"}),401