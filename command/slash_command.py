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
import command as cmd
## Slash Command 

async def slash_command(data):
   parts = data['message'].split()
   command = parts[0][1:].lower()
   args = parts[1:]
   email = data["email"]
   if command in ["rename","re"]:
     await cmd.rename(data,email)
   elif command in ["ban","b"]:
     await cmd.ban(data,email)
   elif command in ["mute","m"]:
     await cmd.mute(data,email) 
   elif command in ["unmute","um"]:
     await cmd.unmute(data,email) 
   elif command in ["unban","u"]:
     await cmd.unban(data,email)
   elif command in ["banlist","bl"]:
     await cmd.ban_list(data)
   elif command in ["mutelist","ml"]:
     await cmd.mute_list(data)
   elif command in ["help","h"]:
     help_text = """

["/rename"] - Rename Chat Name [Owner]
["/help","/h"] - Show Help Menu
["/back","back","1"," "] - Back To Home
["/refresh","/re","re","0",""] - Refresh Chat
["/banlist","/bl"] - To See Ban List
["/mutelist","/ml"] - To See Mute List
["/ban","/b"] [Example: /ban <username> - Ban Someone [Owner]
["/unban","/u"] [Example: /unban <username||index> - Unban Someone [Owner]
["/mute","/m"] [Example: /mute <username> - Mute Someone [Owner]
["/unmute","/um"] [Example: /unmute <username||index> - Unmute Someone [Owner]
"""
     data["message"] = help_text
     await cmd.system_message(data)
   else:
     data["message"] = "Invalid Command"
     await cmd.system_message(data)