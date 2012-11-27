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
from idea_tables import User,Idea, Base

from sqlalchemy import create_engine,and_,or_
from sqlalchemy.orm import sessionmaker
import sys, string
from operator import ne,eq,lt,le,ge,gt
#make a new and improved search ability, make an importable class?


#storage path for the database
path="C:\\Users\Charles\Dropbox\Programming\DataBases\Idea_Box.db"

#create the engine, the base and the session
engine=create_engine('sqlite:///'+path,echo=False)
Session=sessionmaker(bind=engine)

session=Session() #create the session object to comm with db
Base.metadata.create_all(engine) #create our db with the tables

