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

#SEEEDing compliments or insulting words into the DB- Adjectives
comp_words = open('data/compliment-word-list.txt')
neg_words = open('data/negative-word-list.txt')

for line in comp_words:
    word = line.rstrip()
    db_comp = crud.create_adjectives(1, word)

for line in neg_words:
    word = line.rstrip()
    db_comp = crud.create_adjectives(-1, word)
    
