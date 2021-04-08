import os
import json
from random import choice, randint
from datetime import datetime

import crud
from model import *
import server

os.system('dropdb pul_db')
os.system('createdb pul_db')

connect_to_db(server.app)
db.create_all()

user1 = crud.create_user("test", "pass")
user2 = crud.create_user("TEST", "TEST")
