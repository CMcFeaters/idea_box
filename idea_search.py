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
	
def ideaQuery(user,title,tags,session=createAll()):
	#a function that can take in up to 3 search options and returns the results as an array
	#user is the user who's ideas we're searching, it will be a User()
	#title is the title string we are searching for, it will include any %'s alreayd, liek will be used
	#tags comes in as a string separated by commas
	results=session.query(Idea)
	if user<>"": results=results.filter(Idea.user_id==user.id)	#if the search is user specificd
	if title<>"": results=results.filter(Idea.title.like(title)) #if a title is included
	if tags<>"":#this one is tricky, it's a string of objects and commas, replace whitespace with %'s
		tags=tags.split(',')
		resArr=[]
		for thing in tags:
			#create an array with results from each tag, adding a% before and after to make life easy
			resArr.append(results.filter(Idea.tags.like(thing)))
		#convert array of results into an array of ideas
		results=resArr[0].union(resArr)
	return results