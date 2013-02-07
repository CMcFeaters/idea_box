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
#createUser,deleteUser and change user can all be rolled into 1 function with different
#flags, similar to idea_change

def uniqueUsername(username):
	#a search that returns 1 if username is unique, 0 if not
	session=createAll()
	if len(session.query(User).filter(User.username==username).all())>0:
		session.close()
		return 0
	else: 
		session.close()
		return 1
	
def uniqueTitle(username,title):
	#searches to determine if a title already exists for a given user
	session=createAll()
	user=session.query(User).filter(User.username==username).all()[0]
	if len(session.query(Idea).filter(and_(Idea.user_id==user.id,Idea.title==title)).all())>0:
		session.close()
		return 0
	else:
		session.close()
		return 1

def createUser(username,password,session=createAll()):
	#creates a new user, returns 1 if commited, 0 if not
	if uniqueUsername(username) and len(password)>10:
		session.add(User(username.lower(),password))
		session.commit()
		return 1
	else: return 0

def changeUsername(oldUsername, newUsername, session=createAll()):
	#changes a username to another unique one, 1 if commited, 0 if not
	#usernames are stored in lowercase
	if uniqueUsername(newUsername):
		user=session.query(User).filter(User.username==oldUsername).all()[0]
		user.username=newUsername.lower()
		session.commit()
		return 1
	else: return 0
	
def changePassword(username,password,session=createAll()):
	#changes the password of a user as long as it's 10 characters, 1 if good 0 if not
	if len(password)>=10:
		user=session.query(User).filter(User.username==username).all()[0]
		user.password=password
		session.commit()
		return 1
	else: return 0
	
def deleteUser(username,session=createAll()):
	#deletes a user by username, 1 if good 0 if not
	try:
		user=session.query(User).filter(User.username==username).all()[0]
		session.delete(user)
		session.commit()
		return 1
	except: return 0

def createIdea(username,title,body,tags,session=createAll()):
	#creates a new idea for a user as long as the title is unique, 1 if good 0 if not
	#body and tags can be empty
	user=session.query(User).filter(User.username==username).all()[0]
	if uniqueTitle(username,title):
		session.add(Idea(user.id,title,body,tags))
		session.commit()
		return 1
	else: return 0
	
def deleteIdea(username,title,session=createAll()):
	#deletes an idea
	user=session.query(User).filter(User.username==username).all()[0]
	try:
		idea=session.query(Idea).filter(and_(Idea.user_id==user.id,Idea.title==title)).all()[0]
		session.delete(idea)
		session.commit()
		return 1
	except: return 0

def changeTitle(username,oldTitle,newTitle,session=createAll()):
	#changes a title to a unique new title
	user=session.query(User).filter(User.username==username).all()[0]
	if uniqueTitle(username,newTitle):
		idea=session.query(Idea).filter(and_(Idea.user_id==user.id,Idea.title==oldTitle)).all()[0]
		idea.title=newTitle
		session.commit()
		return 1
	else: return 0

def changeIdea(username,title,newIdea,session=createAll()):
	#changes an idea, 1 if good 0 if not
	try:
		user=session.query(User).filter(User.username==username).all()[0]
		idea=session.query(Idea).filter(and_(Idea.user_id==user.id,Idea.title==title)).all()[0]
		idea.idea=newIdea
		session.commit()
		return 1
	except: return 0
	
def deleteTag(username,title,tag,session=createAll()):
	#replaces a tag in the tag string with "", 1 if good 0 if not
	try:
		user=session.query(User).filter(User.username==username).all()[0]
		idea=session.query(Idea).filter(and_(Idea.user_id==user.id,Idea.title==title)).all()[0]
		idea.tags=idea.tags.replace(tag,"")
		idea.tags=idea.tags.replace(",,",",")#the tags are separated by commas, this deletes any double commas
		idea.tags=idea.tags.lstrip(',')
		idea.tags=idea.tags.rstrip(",")
		session.commit()
		return 1
	except: return 0
	
def addTag(username,title,tag,session=createAll()):
	#adds a tag to the tag string, 1 if good 0 if not
	try:
		user=session.query(User).filter(User.username==username).all()[0]
		idea=session.query(Idea).filter(and_(Idea.user_id==user.id,Idea.title==title)).all()[0]
		idea.tags=idea.tags+","+tag
		session.commit()
		return 1
	except: return 0

def editTag(username,title,oldTag,newTag,session=createAll()):
	#edits oldTag to be newTag, 1 if good 0 if not
		if deleteTag(username,title,oldTag,session):
			if addTag(username,title,newTag,session):
				return 1
			else: return 0
		else: return 0
		
def changeTags(username,title,newTags,session=createAll()):
	#changes all tags, 1 if good 0 if not
	try:
		user=session.query(User).filter(User.username==username).all()[0]
		idea=session.query(Idea).filter(and_(Idea.user_id==user.id,Idea.title==title)).all()[0]
		idea.tags=newTags
		session.commit()
		return 1
	except: return 0
	
def signInVerify(userName,password):
	#a function to check the username against it's password
	#given a username and password, returns 1 if correct or a string defining why
	session=createAll()
	result=session.query(User).filter(User.username==userName)
	if len(result.all())!=1:
		return "Username Not Found"
	elif result[0].password!=password:
		return "Password Incorrect"
	else:
		return 1
	session.close()
	
