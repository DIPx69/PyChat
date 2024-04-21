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

## Register Account Stuff

@app.route('/register', methods=['POST'])
async def register():
   payload_client = await request.form
   email = payload_client.get("email", "").lower()
   username = payload_client.get("username", "")
   password = payload_client.get("password", "")
   async with aiofiles.open("database/user.json", 'r') as f:
       data = json.loads(await f.read())
   if email in data:
     message = "Email Already Exist"
     data = {"message":message}
     return jsonify(data),400
   hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
   data[email] = {
     "password": hashed_password,
     "username": username
   }
   async with aiofiles.open("database/user.json", 'w') as f:
       await f.write(json.dumps(data))
   message = f"Account Created [{email}]"
   data = {"message":message}
   return jsonify(data),200