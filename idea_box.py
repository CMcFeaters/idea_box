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

def user_change(username,thingtochange,changetothis,edremadd, session=createAll()):
	#a function used for editing users
	#username is the username of the user being modified
	#thingtochange is the thing that gets changed
	#changetothis is what the thing gets changed to, when adding this is teh new password, username, the new name
	#edremadd -1 delete user, 0 edit user, 1 add user
	results=session.query(User).filter(User.username==username.lower()).all()
	'''!!!!!!!!!!!!!here!!!!!!!!!!!!!!!!!!!!!'''
	if edremadd==1:
		#add a new user
		if len(results)==0:
			#that username is unique
			pass
		else: return "Username already Exists"
		

def createUser(username,password,session=createAll()):
	#create a new user
	#verifies username does not exist, password is at least 10 characters
	#returns 1 if creation successful
	results=session.query(User).filter(User.username==username.lower())
	#checklength of results
	if len(results.all())>0:
		return "Username already exists"
		session.close()
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
	if len(results)>0:
		#mutliple with the same title
		session.close()
		return "Title Already Exists"
	else:
		session.add(newIdea)
		session.commit()
	session.close()
	return 1
	
def idea_change(user,title,thingtochange,changetothis,edremadd, session=createAll()):
	'''#a function designed to change any partof an idea
	#user owns the idea, title identifies which idea it is
	#thingtochange identifies which item will be changed (tag, title, etc)
	#changetothis is the new value for whatever is being changed (note: if a tag is being editted, this is a tuple, containing which tag to change[0] and what to change it to[1])
	#if a tag is being deleted, the changetothis value contains the name of the tag to be deleted
	#edremadd is a flag signifying if the thingtochange is being edited (0), removed(-1) or added (1)'''
	#find the idea
	idea=session.query(Idea).filter(and_(Idea.user_id==user.id,Idea.title==title)).all()[0]
	
	#makethechanges	
	if edremadd==-1 and thingtochange=="tags":
		#deleting, only works for tags
		idea.__dict__[thingtochange]=idea.__dict__[thingtochange].replace(changetothis,"")
		idea.__dict__[thingtochange]=idea.__dict__[thingtochange].rstrip(" , ")
		
	elif edremadd==0:
		#editing
		if thingtochange=="tags":
			#need to change the specific tag in the array
			idea.__dict__[thingtochange]=idea.__dict__[thingtochange].replace(changetothis[0],changetothis[1])
			
		else: idea.__dict__[thingtochange]=changetothis
		
	elif edremadd==1 and thingtochange=="tags":
		#adding, this only works for tags
		idea.__dict__[thingtochange]+=" , "+changetothis
		print idea.__dict__[thingtochange]
		
	else:
		print "Cannot complete transaction"
	
	#get thefuck out
	

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
	
