from .logger import logger
from . import launcher
from . import message_sender


import os

if not os.path.exists(path='sessions'):
    os.mkdir(path='sessions')
