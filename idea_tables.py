'''
idea_tables
this contains all of the setup data for the tables
'''
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()

class User(Base):
	'''the user class'''
	__tablename__='users'
	
	id=Column(Integer,primary_key=True)
	username=Column(String)#will be all lowercase
	password=Column(String)
	
	ideas=relationship("Idea", backref="users")
	
	def __init__(self,username,password):
		self.username=username
		self.password=password#this is something you could do some security work with

	

class Idea(Base):
	'''the ideas table'''
	__tablename__='ideas'
	
	id=Column(Integer,primary_key=True)
	
	user_id=Column(Integer,ForeignKey('users.id'))
	title=Column(String(20))
	idea=Column(String)
	tags=Column(String)
	
	
	def __init__(self,id,title,idea,tag):
		self.user_id=id
		self.title=title
		self.idea=idea
		self.tag=tag
	
	def addTag(self,tag):
		#adds a tag to the self.tag string, separated with a comma
		if self.tag=="":
			self.tag=tag
		else:
			self.tag=self.tag+" , "+tag
		
	def __repr__(self):
		return "User: %s\nTitle: %s\nIdea:\n%s\nTags: %s"%(self.user_id,self.title,self.idea,self.tag)
		