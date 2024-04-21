from quart import Quart
from main import app
print(f'[{app}]')

from .rooms import *
from .login import *
from .register import * 
from .create import *
from .validation import *
from .get_username import *
from .send_message import *
from .rename import *
from .system_massage import *
from .slash_command import *
from .room_list import *
from .ban import *
from .unban import *
from .join import *
from .mute import *
from .unmute import *
app.run(host='0.0.0.0', port=800)