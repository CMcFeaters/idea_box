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