#webpage
#uses flaskr to create working page
from flask import Flask, render_template,redirect,url_for, flash, request, session
import idea_box,idea_search

app= Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)
app.debug=True

app.secret_key = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

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
			print val
			session['username']=request.form['username']
			session['logged_in']=True
			flash("Welcome %s!!"%session['username'])
			return redirect(url_for('addIdea'))
		else:
			flash(val) #val is either 1, or an error message
	return render_template("welcome.html")

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
#edit username
#edit password
#edit idea title
#edit idea body
#edit idea tags
#delete idea
#####################################################	

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
		if idea_box.uniqueUsername(request.form['regUsername'].lower()):
			if len(request.form['regPassword'])>=10:
				if request.form['regPassword']==request.form['passwordConfirm']:
					#we're good, create it and send on our way
					idea_box.createUser(request.form['regUsername'].lower(),request.form['regPassword'])
					flash("Registration successful! Welcome to the fold %s"%request.form['regUsername'])
					return redirect(url_for('welcome'))
					
				#if not, tell why then back to register page	
				else: flash("Passwords don't match")
			else: flash("10 or more characters for a password")
		else: flash("Username %s alread in use"%request.form['regUsername'])
		
		
	return render_template("register.html")
	
if __name__=='__main__':
		app.run()