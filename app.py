from flask import Flask, request, make_response, redirect, url_for
import json
from colorama import Fore

app = Flask(__name__)

page_views = 0
api_requests = 0

noauth_data = "data/64KB.json"
auth_data = "data/64KB-auth.json"

def page_view():
	global page_views
	page_views += 1
	print(Fore.CYAN + f"{page_views} page views.")

def api_request():
	global api_requests
	api_requests += 1
	print(Fore.CYAN+ f"{api_requests} api requests.")

def fread(filename: str):
	f = open(filename, "r")
	content = f.read()
	f.close()
	return content

@app.route("/")
def root():
	page_view()
	return fread("templates/index.html")

@app.route("/noauth_example")
def noauth_example():
	page_view()
	return fread("templates/noauth_example.html")

@app.route("/api/noauth_example", methods=['POST', 'GET'])
def api_noauth_example():
	api_request()
	if request.method == 'GET':
		if "entries" not in request.args.keys():
			print(Fore.RED + "Somebody tried to GET request the noauth api without the correct parameters.")
			return ""
		print(Fore.GREEN + f"Somebody made a GET request to the noauth api with arguments: {dict(request.args)}")
		return json.loads(fread(noauth_data))[0:int(request.args["entries"])]
	else:
		print(Fore.RED + "Somebody tried to make a POST request to the noauth api. This is invalid, because this request on this url is not accepted")
		return ""

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		page_view()
		return fread("templates/login.html")
	else:

#@app.route("/authenticate", methods=['POST'])
#def authenticate():
		test_username = "test"
		test_password = "test"
		
		username = request.form['username']
		password = request.form['password']

		if username == test_username and password == test_password:
			resp = make_response(redirect(url_for('auth_example')))
			resp.set_cookie('username', username)
			return resp
		return "Invalid credentials", 403

@app.route('/dashboard')
def dashboard():
    username = request.cookies.get('username')
    if username:
        # Here, you can make authenticated API requests
        return f"Welcome, {username}! You are authenticated."
    print(Fore.RED + "Unauthenticated user attempted to access dashboard.")
    return redirect(url_for('login'))

@app.route("/auth_example")
def auth_example():
	page_view()
	username = request.cookies.get('username')
	if username:
		print(Fore.GREEN + "Authenticated user successfully accessed the auth dashboard")
		return fread("templates/auth_example.html")
	else:
		print(Fore.RED + "Unauthenticated user attempted to access auth dashboard")
	return "NOT AUTHENTICATED! Try again..."


@app.route("/api/auth_example", methods=['POST', 'GET'])
def api_auth_example():
	username = request.cookies.get('username')
	if username:
		api_request()
		if request.method == 'GET':
			if "entries" not in request.args.keys():
				print(Fore.RED + "Somebody tried to GET request the auth api without the correct parameters.")
				return ""
			print(Fore.GREEN + f"Somebody made a GET request to the auth api with arguments: {dict(request.args)}")
			return json.loads(fread(noauth_data))[0:int(request.args["entries"])]
		else:
			print(Fore.RED + "Somebody tried to make a POST request to the auth api. This is invalid, because this request on this url is not accepted")
		return "Invalid Request"
	print(Fore.RED + "Someone tried to navigate to the auth dashboard without being authenticated!")
	return "NOT AUTHENTICATED"
