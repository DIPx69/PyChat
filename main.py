import os
import time
import json
import aiofiles
import asyncio
import hashlib
import re
from quart import Quart, jsonify, request,render_template
from quart_rate_limiter import *
app = Quart(__name__,template_folder='')
import command
rate_limiter = RateLimiter(app)
uptime_start = int(time.time())
@app.route('/')
async def uptime():
   uptime_seconds = int(time.time() - uptime_start)
   days = uptime_seconds // (24 * 3600)
   hours = (uptime_seconds % (24 * 3600)) // 3600
   minutes = (uptime_seconds % 3600) // 60
   seconds = uptime_seconds % 60
   if days > 0:
     uptime_text = f"{days}d:{hours}h:{minutes}m:{seconds}s"
   else:
     uptime_text = f"{hours}h:{minutes}m:{seconds}s"
   return jsonify({'uptime': uptime_text})