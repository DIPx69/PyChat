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

## All Login Related Stuff
@app.route('/login_email_validation', methods=['POST'])
async def login_validation():
   payload_client = await request.form
   email = payload_client.get("email", " ").lower()
   async with aiofiles.open("database/user.json", 'r') as f:
       data = json.loads(await f.read())
   if email not in data:
     message = "Email Doesn't Exist"
     data = {"message":message}
     return jsonify(data),400
   else:
     return jsonify({'message': 'True'}), 200
@app.route('/login_verify', methods=['POST'])
async def login_verify():
   payload_client = await request.form
   email = payload_client.get("email", "").lower()
   password = payload_client.get("password", "")
   async with aiofiles.open("database/user.json", 'r') as f:
       data = json.loads(await f.read())
   if email not in data:
     data = {"message":"Email Doesn't Not Exist"}
     return jsonify(data),400
   user_info = data[email]
   server_password = user_info["password"]
   hashing_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
   if server_password == hashing_password:
     data = {"message":"Password Matched"}
     return jsonify(data),200
   else:
     data = {"message":"Passwords do not match"}
     return jsonify(data),401
@app.route('/login', methods=['POST'])
async def login():
   payload_client = await request.form
   email = payload_client.get("email", "").lower()
   password = payload_client.get("password", "")
   async with aiofiles.open("database/user.json", 'r') as f:
       data = json.loads(await f.read())
   if email.lower() not in data:
     data = {"message":"Email Doesn't Not Exist"}
     return jsonify(data),400
   user_info = data[email]
   server_password = user_info["password"]
   username = user_info["username"]
   hashing_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
   if server_password == hashing_password:
     data = {"message":"Password Matched","username":username}
     return jsonify(data),200
   else:
     data = {"message":"Passwords do not match"}
     return jsonify(data),401