# author: j. schere
# written 1/25/2025 on a very indoor day
# a quick script to get the currently playing song from my Spotify and display it on the LCD screen on my desk
# THIS PROGRAM WAS RESTRUCTURED TO UTILIZE FLASK FOR USER AUTHENTICATION IN ACCORDANCE WITH THIS VIDEO:
# *********
# https://www.youtube.com/watch?v=olY_2MW4Eik&t=90s
# *********
# so thank you very much to Imdad Codes for making the stupid user authentication process actually possible, wish i didn't have to mess with a front-end but he made it less of a headache
import requests
from datetime import datetime
from flask import Flask, redirect, request, jsonify, session
import urllib.parse

app = Flask(__name__)
app.secret_key = "a9006eb5e08f58d87d233bf1"

# NECESSARY URLs:
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_URL = "https://api.spotify.com/v1/me/player/currently-playing"
# ----------------

# read the client ID and secret from our local files
# TODO: put them in a single config file
clientID = open("clientId.txt").readline()[:-1] # gotta clip the newline, once again
clientSecret = open("clientSecret.txt").readline()[:-1] # again...
HOST = "192.168.7.18"
redirect_uri = f"http://{HOST}:3000/callback"


# time to restructure everything to be a Flask app...

@app.route('/')

def index():
	return "login <a href='/login'>here</a>"

@app.route('/login')
def login():
	scope = "user-read-currently-playing"
	params = {
		"client_id": clientID,
		"response_type": "code",
		"redirect_uri": redirect_uri,
		"scope": scope,
		'show_dialog': True
	}

	auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

	return redirect(auth_url)

@app.route('/callback')

def callback():
	if 'error' in request.args:
		return jsonify({"error": request.args['error']})
	
	if 'code' in request.args:
		payload = {
			"grant_type": "authorization_code",
			"code": request.args['code'],
			"redirect_uri": redirect_uri,
			"client_id": clientID,
			"client_secret": clientSecret
		}

		response = requests.post(TOKEN_URL, data=payload)
		token_info = response.json()

		session['access_token'] = token_info['access_token']
		session['refresh_token'] = token_info['refresh_token']
		# create a session variable for the time the token will expire, using the current UNIX timestamp and adding the time until the token expires
		# we can use this to know when to refresh the token so that shit doesn't just break on us!
		session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

		return redirect("/currently_playing")
	

@app.route("/currently_playing")
def get_playing():
	if 'access_token' not in session:
		return redirect("/login")
	
	if (datetime.now().timestamp() > session['expires_at']):
		return redirect("/refresh_token")
	
	headers = {
		'Authorization': f"Bearer {session['access_token']}"
	}

	response = requests.get(API_URL, headers=headers)
	print(response)
	return response.json()["item"]["name"]

@app.route("/refresh_token")
def refresh_token():
	if 'refresh_token' not in session:
		return redirect("/login")
	
	if (datetime.now().timestamp() > session['expires_at']):
		req_body = {
			'grant_type': 'refresh_token',
			'refresh_token': session['refresh_token'],
			'client_id': clientID,
			'client_secret': clientSecret
		}
		response = requests.post(TOKEN_URL, data=req_body)
		new_token_info = response.json()
		
		session['access_token'] = new_token_info['access_token']
		session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

		return redirect("/currently_playing")
	
if __name__ == '__main__':
	app.run(host="192.168.7.18", debug=True, port=3000)
