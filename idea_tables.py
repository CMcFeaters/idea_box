'''
idea_tables
this contains all of the setup data for the tables
'''
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref
class User(Base):
	'''the user class'''
	__tablename__='users'
	
	id=Column(Integer,primary_key)
	username=Column(String)#will be all lowercase
	password=Column(String)
	ideas=relationship("Idea",order_by="Ideas.id", backref="users"))
	
	def __init__(self,username,password):
		self.username=username
		self.password=password#this is something you could do some security work with
	

class Idea(Base):
	'''the ideas table'''
	__tablename__='ideas'
	
	id=Column(Integer,primary_key)
	
	user_id=Column(Integer,ForeignKey('user.id'))
	title=Column(String(20))
	idea=Column(String)
	tags=Column(String)
	
	user=relationship("User",backref=backref('ideas', order_by=id))
	
	def __init__(self,user,title,idea):
		self.user=user
		self.title=title
		self.idea=idea
		self.tag=""
	
	def addTag(self,tag):
		#adds a tag to the self.tag string, separated with a comma
		if self.tag=="":
			self.tag=tag
		else:
			self.tag=self.tag+","+tag
		
	def __repr__(self):
		return "User: %s\nTitle: %s\nIdea:\n%s\nTags: %s"%(self.user,self.title,self.idea,self.tag)