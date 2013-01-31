#webpage
#uses flaskr to create working page
from flask import Flask, render_template

app= Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)
app.debug=True


@app.route('/')
def welcome():
	return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template("welcome.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
	return render_template("welcome.html")
	
if __name__=='__main__':
		app.run()