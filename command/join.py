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
# Join Chat Room

@app.route('/join', methods=['POST'])
async def join():
   payload_client = await request.form
   try:
     room_id = int(payload_client.get("id", " "))
     email = payload_client.get("email", " ")
     if room_id < 0:
       return jsonify({"message":"Room Doesn't Exist"}),404
     username = await command.get_username_local(email.lower())
   except:
     return jsonify({"message":"Room Doesn't Exist"}),404
   rooms = await command.all_rooms()
   try:
     room_name = rooms[room_id-1]
     print(f"Joining {room_name} [{room_id-1}]")
   except:
     return jsonify({"message":"Room Doesn't Exist"}),404
   filename = f"rooms/{room_name}"
   async with aiofiles.open(filename, 'r') as f:
      data = json.loads(await f.read())
   ban_list = [username.lower() for username in data["banned"]]
   if username.lower() in ban_list:
     return jsonify({"message":"Sorry, your account is banned from this chat room"}),404
   return jsonify(data)