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
#make a new and simpler search ability, make an importable class?


#storage path for the database
path="C:\\Users\Charles\Dropbox\Programming\DataBases\Idea_Box.db"

def createAll():
	#create the engine, the base and the session
	engine=create_engine('sqlite:///'+path,echo=False)
	Session=sessionmaker(bind=engine)

	session=Session() #create the session object to comm with db
	Base.metadata.create_all(engine) #create our db with the tables
	return session
	
def createUser(username,password):
	#create a new user
	#verifies username does not exist, password is at least 10 characters
	#returns 1 if creation successful
	if session.query(User).filter(username==username).count>0:
		return "Username already exists"
	elif password.length()<=10:
		return "Password too short"
	else:
		session.add(User(username,password))
		session.commit()
		return 1
	

def createIdea(username,title,idea,tags):
	#create a new idea in the database
	#uses username to query user_id
	
	session.add(Idea(user_id,title,idea,tags))
	session.commit()

def deleteUser(username):
	pass
	

