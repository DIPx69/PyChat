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


## Get Username 

@app.route('/get_username', methods=['POST'])
async def get_username():
   payload_client = await request.form
   email = payload_client.get("email", "").lower()
   async with aiofiles.open("database/user.json", 'r') as f:
       data = json.loads(await f.read())
   if email in data:
     user_info = data[email]
     username = user_info["username"]
     data = {"username":username}
     return jsonify(data)
   else:
     return jsonify({"message":"Email Doesn't Exist"}),401
async def get_username_local(email):
   async with aiofiles.open("database/user.json", 'r') as f:
       data = json.loads(await f.read())
   if email in data:
     user_info = data[email]
     username = user_info["username"]
     return username