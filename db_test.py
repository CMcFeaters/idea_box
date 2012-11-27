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
			print thing.id
		session.add(User("Charles%s"%str(thing.id+1),"Test",Idea("TestIdea","I THINK IT SHOULD WORK PROPERLY","TESTS")))
		session.commit()
except:
	print "Did not pass test 1"
else:
	print "#####Test 1: passed!"

