#webpage
#uses flaskr to create working page
from flask import Flask, render_template,redirect,url_for, flash, request

app= Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)
app.debug=True

app.secret_key = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

@app.route('/')
def welcome():
	return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		#check for valid log in
		#if invalid: flash invalid message, redirect to 'welcome'
		#if valid: flash welcome message, redirect to 'addIdea'
		return redirect(url_for('addIdea'))
	return render_template("welcome.html")

@app.route('/searchIdea',methods=['GET','POST'])
def searchIdea():
	print 'hello'
	if request.method=='POST':
		print 'FUCK'
		#this portion executes the search
		#will redirect to results, showing search results
		return redirect(url_for('displayResults'))
	else: return render_template('searchIdea.html')
	
@app.route('/displayResults', methods=['GET'])
def displayResults():
	#all resutls displayed here
	return render_template('displayResults.html', results=results)
	
#####################################################
####START HERE!!!!!!!!!!!!!!!!!!!
#adding RESULTS to the DISPLAY TEMPLATE!!!!!!!!!!!!!!
#####################################################	

@app.route('/addIdea',methods=['GET','POST'])
def addIdea():
	if request.method=='POST':
		#do title check
		#if successful, post idea to db, redirect to display idea showing only new idea
		#if not, flash why re-rendertemplate
		print request.form['body']
		if 1: return redirect(url_for('displayResults', results=results))
		else: 
			flash("ERROR")
			return render_template('addIdea.html')
	else:
		return render_template('addIdea.html')
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	
	if request.method=='POST':
		#Need to check if we can create the user
		#if create, write to db, flash message
		#if not, flash why not
		flash("Registration successful! Welcome to the fold %s"%request.form['regUsername'])
		return redirect(url_for('welcome'))
	return render_template("register.html")
	
if __name__=='__main__':
		app.run()