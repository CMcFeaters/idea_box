#test code
#this code will test our database project

#test 1
#create an entry
try:
	print "Attempting Importing"
	import sys, string, random, os, idea_box
	
	from idea_tables import Idea, User
	
	from idea_box import path as impPath
	sys.path.append("C:\\Users\Charles\Dropbox\Programming\py\general_use")
	from error_classes import stdException
	from conversion import timeConv
	from random_tools import id_generator
except:
	print "Importing Failed"
	raise 
else:
	print "Importing Complete"
print "----------------------"

#This section is only used if we make changes to our database
#delete the existing database for now till it is setup the way we want it
def deleteDB():
	try:
		print "Attempting Database Deletion"
		if os.path.exists(impPath) and os.path.isfile(impPath):
			print "file found"
			print "Last accessed: "+timeConv(os.path.getatime(impPath))
			os.remove(impPath)
	except:
		print "Database deletion Failed"
	else:
		print "Database deletion Complete"
	print "----------------------"
		
def createDB():
	#create the new database and session
	try:
		print "Attempting Database Creation"
		session=idea_box.createAll()
	except:
		print "Database creation Failed"
	else:
		print "Database create Complete"
	

#thought: this should be written as the inputs from a website
	#this way the program doesn'thave to be re-written when
	#the web interface is added



def newUser():
	#this function creats a new user
	try:
		#create a new use with a randomly generated username
		print "Attempting New User Creation"
		session=idea_box.createAll()
		username=id_generator()
		# try to creat a user
		x=idea_box.createUser(username,"10LONGCHARACTERS",session)
		while x!=1:
			#if the username already exists, create a different one and try again
			username=id_generator()
			x=idea_box.createUser(username,"10LONGCHARACTERS",session)
	except:
		print "User Creation Error"
		raise
	else:
		print "User Creation Successful"

def newIdea():
	#create a new idea for a user with no existing ideas
	try:
		#add an idea to a user with no existing ideas, if one does not exist, create a new user
		print "Attempting First Idea Addition"
		
		#find a user with no ideas
		session=idea_box.createAll()
		results=session.query(User)
		
		#check for a user with no ideas
		x=[thing for thing in results if thing.ideas==[]]
		
		#the test user has no ideas, we will add a new one
		testUser=x[0]
		testIdea=Idea(testUser.id,"TEST IDEA_%s"%(id_generator(random.randrange(3),string.digits)),"%s"%(id_generator(10,string.ascii_uppercase)),id_generator(5,string.ascii_uppercase))
		print testIdea
		z=idea_box.createIdea(testUser,testIdea.title,testIdea.idea,testIdea.tags,session)
		if z!=1:
			print z
			raise Exception("IT WORKED")
	except:
		print "Idea Creation Failed"
		raise
	else:
		print "Idea Creation Successful"
		
def dupIdea():
	#create a duplicate idea for a user with existing ideas
	try:
		#add an idea to a user with no existing ideas, if one does not exist, create a new user
		print "Attempting Duplicate First Idea Addition"
		
		#find a user with no ideas
		session=idea_box.createAll()
		results=session.query(User)
		
		#check for a user with no ideas
		x=[thing for thing in results if thing.ideas!=[]]
		
		#the test user has no ideas, we will add a new one
		testUser=x[0]
		
		#find an existing idea and it's title
		controlIdea=session.query(Idea).filter(Idea.user_id==testUser.id).all()[0]
		
		testIdea=Idea(testUser.id,controlIdea.title,"%s"%(id_generator(10,string.ascii_uppercase)),id_generator(5,string.ascii_uppercase))
		print testIdea
		z=idea_box.createIdea(testUser,testIdea.title,testIdea.idea,testIdea.tags,session)
		if z!=1:raise stdException("BLANK")
		
	except stdException:
		print "Duplicate Idea Title Exists"
	except:
		print "Duplicte IDea Creation Failed"
		raise
	else:
		print "Duplicate Idea Creation Successful"
		
def deleteUser():
	try:
		print "Attempting Delete User"
		session=idea_box.createAll()
		results=session.query(User).all()
		testUser=results[random.randrange(len(results))]
		session.delete(testUser)
		session.commit()
		session.close()
	except:
		print "User Deletion Failed"
		raise
	else:
		print "User Deletion Successful"
'''#add an idea to a user with no existing ideas
try:
	print "Attempting Entry Creation"
	session=idea_box.createAll()
	session.add(User("Charles","Test"))
	print "User Created"
	results=session.query(User).filter(User.Id==0)
	if results[0].ideas==[]:
		#if the ideas are empty, we'll add the first one
		results[0].ideas=[Idea(results[0].id,"TestIdea","I THINK IT SHOULD WORK PROPERLY","TESTS")]
	else:
		print 'test'
		#if they are not empty, we need to append an idea
		results[0].ideas.append(Idea(results[0].id,"TestIdea","I THINK IT SHOULD WORK PROPERLY","TESTS"))
	session.commit()
	session.close()
except:
	print "Entry Creation Failed"
	raise
else:
	print "Entry Creation Complete"
	
#add an idea to a user with an existin gidea
'''
print "----------------------"	
newUser()
print "----------------------"	
newIdea()
print "----------------------"	
dupIdea()
print "----------------------"	
deleteUser()