#test code
#this code will test our database project

#test 1
#create an entry
try:
	from idea_box import session
	from idea_tables import Idea, User
except:
	print "Error importing files!"
finally:
	print "#####Test 0: Passed"

class test1Error(Exception):
	pass
	
print "Test 1: Creating and commiting an entry"
try:
		for thing in session.query(User):
			print thing
except:
	print "Did not pass test 1"
finally:
	print "#####Test 1: passed!"

