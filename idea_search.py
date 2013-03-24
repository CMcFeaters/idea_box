#this file holds search functions
#there may end up only being one
#search function goals
'''
	-take in parameters, return a result item
	-search by username and/or title and/or tags
	-user/all
	-title like/all
	-tags like/all
	#be lazy and just do 3 queries if necessary, why?  fuckem that's why
	'''

from idea_box import createAll
from idea_tables import User, Idea
	
def ideaQuery(username,title,contains,tags,session=createAll()):
	###a function that can take in up to 3 search options and returns the results as a query object
	
	#user is the user who's ideas we're searching, it will be a User()
	#title is the title string we are searching for, it will include any %'s alreayd, liek will be used
	#tags comes in as a string separated by commas
	
	#this is built around an "and" type filter, should it be on "or" type filter
	
	results=session.query(Idea)
	
	if username<>"": 
		user=session.query(User).filter(User.username==username).all()[0]
		results=results.filter(Idea.user_id==user.id)	#if the search is user specificd
		
	if title<>"": results=results.filter(Idea.title.like("%"+title+"%")) #if a title is included
	
	if contains<>"": results=results.filter(Idea.idea.like("%"+contains+"%")) #if contains are included
	
	if tags<>"":#adjust tags so they are in an array of format [%tag%,%tag%...]
		tags="%"+tags+"%"
		tags=tags.replace(",","%,%")
		tags=tags.split(",")
		
		resArr=[]
		for thing in tags:
			#resArr is an array of queries, each one for tag
			resArr.append(results.filter(Idea.tags.like(thing)))
		#print resArr[0].all()[0]
		for thing in resArr:
			if resArr.index(thing)==0:results=thing
			else: results=results.union(thing)
	session.close()
	
	return results

def userQuery():
	#returns a list of all users except admin
	session=createAll()
	results= session.query(User).filter(User.username!='admin')
	session.close()
	return results