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
	
def createUser(username,password,session=createAll()):
	#create a new user
	#verifies username does not exist, password is at least 10 characters
	#returns 1 if creation successful
	results=session.query(User).filter(User.username==username)
	#checklength of results
	if len(results.all())>0:
		session.close()
		return "Username already exists"
	#check passwordlength
	if len(password)<=10:
		session.close()
		return "Password too short"
	#if it's all good, commit and move on with our lives
	session.add(User(username,password))
	session.commit()
	session.close()
	return 1
	
def createIdea(user,title,idea,tags, session=createAll()):
	#create a new idea in the database
	#"user" is the user that the idea shall be assigned to	
	#check to verify there are no existing ideas with the same title
	#if so, add and commit
	newIdea=Idea(user.id,title,idea,tags)
	
	#check for duplicate titles
	results=session.query(Idea).filter(and_(Idea.user_id==user.id,Idea.title==title)).all()
	print len(results)
	if len(results)>0:
		#mutliple with the same title
		session.close()
		return "Title Already Exists"
	else:
		session.add(newIdea)
		session.commit()
	session.close()
	return 1

def deleteUser(username):
	pass