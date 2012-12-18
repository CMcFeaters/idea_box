#test code
#this code will test our database project

#test 1
#create an entry
try:
	print "Attempting Importing"
	import sys
	import idea_box
	from idea_tables import Idea, User
	import os
	from idea_box import path as impPath
	sys.path.append("C:\\Users\Charles\Dropbox\Programming\py\general_use")
	from conversion import timeConv
except:
	print "Importing Failed"
	raise 
else:
	print "Importing Complete"
print "----------------------"
'''
This section is only used if we make changes to our database
#delete the existing database for now till it is setup the way we want it
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
	#create the new database and session
try:
	print "Attempting Database Creation"
	session=idea_box.createAll()
except:
	print "Database creation Failed"
else:
	print "Database create Complete"
		
'''		

#thought: this should be written as the inputs from a website
	#this way the program doesn'thave to be re-written when
	#the web interface is added
print "----------------------"	
class test1Error(Exception):
	pass
	
print "Attempting Entry Creation"
try:
	session=idea_box.createAll()
	session.add(User("Charles","Test"))
	print "User Created"
	results=session.query(User).filter(User.username=="Charles")
	if results[0].ideas==[]:
		results[0].ideas=[Idea(results[0].id,"TestIdea","I THINK IT SHOULD WORK PROPERLY","TESTS")]
	else:
		results[0].ideas.append(Idea(results[0].id,"TestIdea","I THINK IT SHOULD WORK PROPERLY","TESTS"))
	session.commit()
	session.close()
except:
	print "Entry Creation Failed"
	raise
else:
	print "Entry Creation Complete"
	
#add query of user and all ideas here

#add 

