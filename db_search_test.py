#search test 
try:
	print "Attempting Importing"
	import sys, string, random, os, idea_box
	
	from idea_tables import Idea, User
	from idea_search import ideaQuery
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
	
#begin search test instructions here
#how many searches?
#16 searches
#1 for each combination of (user,title,tags,contains)

def genericTest(username,title,contains,tags):
	try:
		#create a string describing what we're testing
		str=""
		if username<>"":
			str=str+"username: %s\n"%username
		else:str=str+"username: none\n"
		if title<>"":
			str=str+"title: %s\n"%title
		else:str=str+"title: none\n"
		if contains<>"":
			str=str+"contains: %s\n"%contains
		else:str=str+"contains: none\n"
		if tags<>"":
			str=str+"tags: %s\n"%tags
			if andor==1: str=str+" and"
			else: str=str+" or"
		else:str=str+"tags: none\n"
		
		print "Attempting Query Test of-\n",str

		session=idea_box.createAll()
		#run the test
		results= ideaQuery(username,title,contains,tags,session)
		
		for thing in results:
			#print '\nresult ',results.all().index(thing)
			print thing
		print "Number of results: ",len(results.all())
		session.close()
	except:
		print "error Query Test: ",str
		raise
	else:
		print "Query test: %s  COMPLETE"%str

print '------------------------'
genericTest("","","","")
print '------------------------'
genericTest("charles","","","")
print '------------------------'
genericTest("charles","%3%","","")
print '------------------------'
genericTest("charles","%3%","%4%","")
print '------------------------'
genericTest("charles","%3%","%4%","tag39")
print '------------------------'
genericTest("charles","","%4%","tag39")
print '------------------------'
genericTest("charles","","","tag39")
print '------------------------'
genericTest("charles","%3%","","tag39")
print '------------------------'
genericTest("charles","","","tag39")
print '------------------------'
genericTest("","%3%","%4%","tag39")
print '------------------------'
genericTest("","%3%","","tag39")
print '------------------------'
genericTest("","%3%","","")
print '------------------------'
genericTest("","%3%","%4%","")
print '------------------------'
genericTest("","","%4%","tag39")
print '------------------------'
genericTest("charles","","","2,1")
print '------------------------'
genericTest("charles","","","7,1")
print '------------------------'