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
@app.route('/rooms', methods=['GET'])
async def rooms():
   async with aiofiles.open("database/rooms.json", 'r') as f:
     rooms = json.loads(await f.read())
   json_data = {"rooms":rooms}
   return jsonify(json_data)