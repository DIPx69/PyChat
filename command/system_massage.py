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

## System Massage

async def system_message(data,success=None):
  datax = data
  timestamp = int(time.time())
  message = data["message"]
  file_name = data["file_name"]
  new_message = {"name":"PyChatBot","message":message,"timestamp":timestamp}
  async with aiofiles.open(file_name, 'r') as f:
   data = json.loads(await f.read())
   data["messages"] = {str(int(key)+1): message for key, message in data["messages"].items()}
   data["messages"]["1"] = new_message
   if success:
     data["room_name"] = datax["args"]
  if len(data["messages"]) >= 11:
     del data["messages"]["11"]
  sorted_messages = sorted(data['messages'].items(), key=lambda x: int(x[0]))
  sorted_messages_dict = {k: v for k, v in sorted_messages}
  data['messages'] = sorted_messages_dict
  async with aiofiles.open(file_name, 'w') as f:
     await f.write(json.dumps(data))