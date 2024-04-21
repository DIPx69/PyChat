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

## Validation Stuff 

@app.route('/email_validation', methods=['POST'])
async def email_validation():
   payload_client = await request.form
   email = payload_client.get("email", " ").lower()
   pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
   async with aiofiles.open("database/user.json", 'r') as f:
       data = json.loads(await f.read())
   if email in data:
     message = "Email Already Exist"
     data = {"message":message}
     return jsonify(data),400
   elif not re.match(pattern, email):
     message = "Invalid Email Address"
     data = {"message":message}
     return jsonify(data),400
   else:
     return jsonify({'message': 'True'}), 200
@app.route('/username_validation', methods=['POST'])
async def username_validation():
   payload_client = await request.form
   username = payload_client.get("username", " ").lower()
   async with aiofiles.open("database/user.json", 'r') as f:
       data = json.loads(await f.read())
   usernames = [info["username"].lower() for email, info in data.items()]
   if username in usernames:
     message = "Username Already Exist"
     data = {"message":message}
     return jsonify(data),400
   elif not (3 <= len(username) <= 20):
       return jsonify({'message': 'Length Requirement (between 3 and 20 characters)'}), 400
   elif ' ' in username:
     return jsonify({'message': 'No Spaces Allowed'}), 400
   elif not username.isalnum():
     return jsonify({'message': 'No Special Characters Allowed'}), 400
   elif username.isdigit():
       return jsonify({'message': "You Can't Use Only Numbers"}), 400
   else:
     return jsonify({'message': 'True'}), 200