#webpage
#uses flaskr to create working page
from flask import Flask, render_template,redirect,url_for, flash, request, session
import idea_box,idea_search

app= Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('FLASKR_SETTINGS',silent=True)
app.debug=True

app.secret_key = 'development key'

@app.route('/')
def welcome():
	#standard welcome, you're logged in or you're not
	if session.get('logged_in'):
		return redirect(url_for('addIdea'))
	else: return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
#allows for user login
	if request.method=='POST':
		#check for valid log in
		val=idea_box.signInVerify(request.form['username'].lower(),request.form['password'])
		if val==1:
			session['username']=request.form['username']
			session['logged_in']=True
			flash("Welcome %s!!"%session['username'])
			if session['username']=='admin':
				#logged in as admin, redirect to admin's page
				return redirect(url_for('admin'))
			else:
				#not admin, redirect elsewhere
				return redirect(url_for('addIdea'))
		else:
			flash(val) #val is either 1, or an error message
	return render_template("welcome.html")

@app.route('/admin',methods=['GET','POST'])
def admin():
	#admin page, 
	#displays all users w/ #of ideas
	#allows for the deletion/creation of users and resetting of passwords
	if session['username']=='admin':
		return render_template('admin.html',users=idea_search.userQuery())
	else: return redirect(url_for('welcome'))

@app.route('/deleteUser/<username>',methods=['GET','POST'])
def deleteUser(username):
	#page to delete a user
	if session['username']=='admin':
		if request.method=="POST":
			#delete was ok'd
			if idea_box.deleteUser(username):flash(username + "deleted")
			else: flash("SQL ERROR")
			#go back to admin page
			return redirect(url_for('admin'))
		else: return render_template('adminUsername.html',username=username)
	else: return redirect(url_for('welcome'))
	
@app.route('/resetPassword/<username>',methods=['GET','POST'])
def resetPassword(username):
	#reset a user's password
	if session['username']=='admin':
		if request.method=="POST":
			if len(request.form['newPassword'])>=10 and len(request.form['newPassword'])<=50:
				if request.form['newPassword']==request.form['newPasswordConfirm']:
					if idea_box.changePassword(username,request.form['newPassword']):
						flash(username+ ' password reset Success!')
						return redirect(url_for('admin'))
					else: flash('SQL Error')
				else: flash("Passwords don't match")
			else: flash("10-50 Characters admin")
		return render_template('adminPassword.html',username=username)
	else: return redirect(url_for('welcome'))
	
@app.route('/logout')
def logout():
	session['logged_in']=False
	session['username']=""
	flash("You have been logged out")
	return redirect(url_for('welcome'))
	
@app.route('/searchIdea',methods=['GET','POST'])
def searchIdea():
	#executes a search and displays teh results
	if session.get('logged_in'):#need to verify logged in
		print 'hello'
		if request.method=='POST':
			#search and display
			results=idea_search.ideaQuery(session['username'],request.form['title'],request.form['body'],request.form['tags']).all()
			return render_template('displayResults.html',results=results)
			
		else: return render_template('searchIdea.html')
	else: return redirect(url_for('welcome'))
	
@app.route('/displayAll', methods=['GET'])
def displayAll():
	if session.get('logged_in'):#need to verify logged in
	#all resutls displayed here
		results=idea_search.ideaQuery(session['username'],"","","").all()
		return render_template('displayResults.html', results=results)
	else: return redirect(url_for('welcome'))
	
#####################################################
####START HERE!!!!!!!!!!!!!!!!!!!
#CONSIDER BETTER FEEDBACK FOR EDIT IDEA SECTION (say why you cant change something?)
#####################################################	
@app.route('/deleteIdea/<title>')
def deleteIdea(title):
	#deletes the idea from teh database, no backsies!
	if session.get('logged_in'):
		#attempt to delete idea and show results
		if idea_box.deleteIdea(session['username'],title.lower()):
			flash("Idea deleted")
			return redirect(url_for('displayAll'))
		else:
			#if something fails, explain and show idea
			flash("Could not delete")
			results=idea_search.ideaQuery(session['username'],title.lower(),"","").all()
			return render_template('displayResults.html',results=results)		
	else: return redirect(url_for('welcome'))

@app.route('/editIdea/<title>', methods=['GET','POST'])
def editIdea(title):
	#sends the idea in title to the same template as add idea
	#but all appropriate information is filled in

	if session.get('logged_in'):
		if request.method=="POST":
			#change the title, then the body, then the tags, redirect to display the new idea
			#any errors will flash why, then redirect to display the idea in its current state
			newTitle=request.form['title'].lower()
			if idea_box.changeTitle(session['username'],title,newTitle):
				if idea_box.changeIdea(session['username'],newTitle,request.form['body']):
					if idea_box.changeTags(session['username'],newTitle,request.form['tags']):
						flash("Idea change Success!")
					else:
						flash("Could not change tags")
				else:
					flash("Could not change body")
			else:
				flash("Could not change title")
				results=idea_search.ideaQuery(session['username'],title.lower(),"","").all()[0]
				return render_template('editIdea.html',idea=results)
			#display the edited idea
			results=idea_search.ideaQuery(session['username'],newTitle,"","").all()
			return render_template('displayResults.html',results=results)
		else:
			#we need the edit data, send to edit page
			results=idea_search.ideaQuery(session['username'],title.lower(),"","").all()[0]
			return render_template('editIdea.html',idea=results)
	else: return redirect(url_for('welcome.html'))

@app.route('/editUsername/<username>',methods=['GET','POST'])
def editUsername(username):
	#changes the username and/or password as long as they meet requirements
	if session['logged_in']:#verify logged in
		if request.method=="POST":
			changeState=idea_box.changeUsername(session['username'],request.form['newUsername'].lower())
			if changeState==1:	#see if we can change it
				session['username']=request.form['newUsername'].lower()
				flash("Username Changed")
				return redirect(url_for("welcome"))
			else: flash(changeState)

		else: return render_template("editUsername.html",username=session['username'])
	else: return redirect(url_for('welcome'))

@app.route('/editPassword',methods=['GET','POST'])
def editPassword():
	#change password, verify old password, check new password
	if session.get('logged_in'):
		if request.method=="POST": #ready to change?
			if idea_box.signInVerify(session['username'],request.form['oldPassword'])==1: #a bunch of checks
				if request.form['newPassword']==request.form['newPasswordConfirm']:
					if idea_box.changePassword(session['username'],request.form['newPassword']):
						flash("Password change successful!")
						return redirect(url_for('welcome'))
						
					else: flash("Password length incorrect!")
				else: flash("Passwords do not match!")
			else: flash("Password incorrect")
		return render_template('editPassword.html')
		
	else: return redirect(url_for('welcome'))
@app.route('/addIdea',methods=['GET','POST'])
def addIdea():
	#checks if user is logged in, if title is unique
	#if so, creates idea, then displays it
	#else flashes error 
	if session.get('logged_in'):#need to verify logged in
		if request.method=='POST':
			if idea_box.uniqueTitle(session['username'],request.form['title'].lower()):
				#checks passed, create the idea
				idea_box.createIdea(session['username'],request.form['title'].lower(),request.form['body'],request.form['tags'])
				flash("New Idea Added!")
				results=idea_search.ideaQuery(session['username'],request.form['title'],"","").all()
				return render_template('displayResults.html',results=results)
			#display errors and redirect accordingly
			else: flash('Title already exists')	
	else: return redirect(url_for('welcome'))
	return render_template('addIdea.html')
	

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method=='POST':
		#check if the usrname is valid, if so create it and send to welcoem page
		#check username
		userCheck=idea_box.usernameCheck(request.form['regUsername'])
		if userCheck==1: #username is ok
			if len(request.form['regPassword'])>=10 and len(request.form['regPassword'])<=50:
				if request.form['regPassword']==request.form['passwordConfirm']:#password ok
					#create this bad mother
					if idea_box.createUser(request.form['regUsername'].lower(),request.form['regPassword']):
						flash("Registration successful! Welcome to the fold %s"%request.form['regUsername'])
						return redirect(url_for('welcome'))
					else: flash("SQL ERROR")
				else: flash("Passwords don't match")
			else: flash("10-50 Characters for the password")
		else: flash(userCheck)
	return render_template("register.html")
	
if __name__=='__main__':
		app.run()