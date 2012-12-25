#test code
#this code will test the querying ability of our database
#it will also show all information we have existing in the database
#more to come.
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


#thought: this should be written as the inputs from a website
	#this way the program doesn'thave to be re-written when
	#the web interface is added
print "----------------------"	
class test1Error(Exception):
	pass
	
print "Attempting User Querying"
try:
	session=idea_box.createAll()
	results=session.query(User)
	print "printing all users:"
	for thing in results:
		print "----------"
		print thing
	session.close
except:
	print "User Querying Failed"
	raise
else:
	print "User Querying Complete"
	

print "Attempting Idea Querying"
try:
	#this section will query the user table for each user
	#then query the idea table for each idea belonging to the user
	session=idea_box.createAll()
	names=session.query(User)
	print "printing all Ideas of each User:"
	
	for thing in names:
		print "Ideas for: %s"%(thing.username)		
		print thing.ideas
				
	session.close
except:
	print "Idea Querying Failed"
	raise
else:
	print "Idea Querying Complete"
	


