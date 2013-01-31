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
	return render_template("welcome.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
	searchword=request.args.get('key','')
	print searchword
	if request.method=='POST':
		flash("I'M SURE THAT WORKED FINE")
		return redirect(url_for('welcome'))
	return render_template("register.html")
	
if __name__=='__main__':
		app.run()