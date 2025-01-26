from argparse import ArgumentParser
import I2C_LCD_driver as driver
import requests
import time

# Constants
API_URL = "https://api.spotify.com/v1/me/player/currently-playing"
my_lcd = driver.lcd()

# helper functions
def get_time_remaining(progress, duration):
    return (duration - progress) / 1000

def display_song(song_name):
    global my_lcd
    my_lcd.lcd_clear()
    my_lcd.lcd_display_string("Now Playing:", 1)
    my_lcd.lcd_display_string(song_name, 2)

parser = ArgumentParser()
parser.add_argument('auth_token', type=str, help='The authorization token for the Spotify API')
args = parser.parse_args()
print(f"Received auth token: {args.auth_token}")

AUTH_TOKEN = args.auth_token



headers = {
    'Authorization': f"Bearer {AUTH_TOKEN}"
}

while True:
	try:
		print("making request to api")
		response = requests.get(API_URL, headers=headers)
		if (response.status_code == 204):
			print("nothing playing")
			my_lcd.lcd_clear()
			my_lcd.lcd_display_string("Now Playing:", 1)
			my_lcd.lcd_display_string("Nothing.",2)
			time.sleep(5)
			continue
		current_song = response.json()["item"]["name"]
		song_duration = response.json()["item"]["duration_ms"]
		song_progress = response.json()["progress_ms"]
		display_song(current_song)
		print(current_song + " is playing with " + str(get_time_remaining(song_progress, song_duration)) + " seconds remaining")
		if ((get_time_remaining(song_progress, song_duration) / 2) > 5):
			time.sleep(get_time_remaining(song_progress, song_duration) / 2)
		else:
			time.sleep(5)
	except Exception as e:
		print(f"Error: {e}")
		my_lcd.lcd_clear()
		my_lcd.lcd_display_string("Oh my.", 1)
		my_lcd.lcd_display_string("Something broke.", 2)
		exit(1)
