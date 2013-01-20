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
		z=idea_box.createIdea(testUser,testIdea.title,testIdea.idea,testIdea.tags,session)
		if z!=1:
			print z
			raise Exception("IT WORKED")
	except:
		print "Idea Creation Failed"
		raise
	else:
		print "Idea Creation Successful"
		
def secondIdea():
	#create a duplicate idea for a user with existing ideas
	try:
		#add an idea to a user with no existing ideas, if one does not exist, create a new user
		print "Attempting Second Idea Addition"
		
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
		z=idea_box.createIdea(testUser,testIdea.title,testIdea.idea,testIdea.tags,session)
		if z!=1:raise stdException("BLANK")
		
	except stdException:
		print "Second Idea title already Exists"
	except:
		print "Second Idea Creation Failed"
		raise
	else:
		print "Second Idea Creation Successful"
		
def secondTag():
	try:
		#this tests the idea_tables.idea.addTag(tag) function
		print "Attempting Tag Addition"
		session=idea_box.createAll()
		results=session.query(User).all()
		nResults=[x for x in results if x.ideas!=[]]
		testUser=nResults[random.randrange(len(nResults))]
		
		testUser.ideas[random.randrange(len(testUser.ideas))].addTag("EXTRA!!!!!!!!!!")
		session.commit()
		session.close()
	except:
		print "Tag Addition Failed"
		raise
	else:
		print "Tag Addition Success"

		
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

def changeToLower():
	#a function that changes all usernames to lowercase
	session=idea_box.createAll()
	results=session.query(User).all()
	lNames=[thing.username.lower() for thing in results]
	for i in range(len(results)):
		results[i].username=lNames[i]
		session.add(results[i])
	session.commit()
	session.close
		

def passwordCheck():
	#runs the password check function
	try:
		print "Running Password Check"
		session=idea_box.createAll()
		results=session.query(User).all()
		uName=results[0].username
		pw=results[0].password
		x=idea_box.signInVerify(uName,pw)
		if x==1:
			print "Welcome in ",uName
		else:
			print x
		session.close()
	except:
		print "Password Check Failure"
		raise
	else:
		print "Password Cehck Success"
		
#deleteDB()
#createDB()
print "----------------------"	
newUser()
print "----------------------"	
newIdea()
print "----------------------"	
secondIdea()
print "----------------------"	
changeToLower()
print "----------------------"	
secondTag()
print "----------------------"
passwordCheck()
