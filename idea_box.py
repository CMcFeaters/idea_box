'''idea_box
a box to put ideas for projects in
users can log in
enter data
	title
	paragraph
	headers
view entries
search by headers
'''

'''An entry:
	fid: the users id
	Id: entry id
	string: Title
	string: paragraph entry
	string: search headers
'''
from idead_tables import User,Idea

from sqlalchemy import create_engine,and_,or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys, string
from operator import ne,eq,lt,le,ge,gt
#make a new and improved search ability, make an importable class?
