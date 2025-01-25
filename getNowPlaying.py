import requests
import oauthlib

clientID = open("clientId.txt").readline()[:-1] # gotta clip the newline, once again
clientSecret = open("clientSecret.txt").readline()[:-1] # again...

data = {
	'grant_type': 'client_credentials',
	'client_id': clientID,
	'client_secret': clientSecret
}

accessToken = requests.post("https://accounts.spotify.com/api/token", data=data).json()["access_token"]

headers = {

}

