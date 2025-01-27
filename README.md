# Now Playing LCD:

A neat little program I wrote to display what I'm currently listening to on an LCD screen on my desk. My Raspberry Pi Zero hosts a very simple Flask webserver (my first time using Flask) that I connect to from my computer to authenticate the program to access my Spotify account information.
I initially tried to do it all in the console, but ended up needing to make a front-end for OAuth reasons. Many thanks to [Imdad Codes](https://www.youtube.com/watch?v=olY_2MW4Eik&t=90s) for making that process much less of a hassle.

Once that was set up, I learned how to use the **subprocess** module to pass the access token received to a second program (*autoChange.py*) that uses it to make API calls and update the LCD.

I've been making a bunch of little tools for this LCD setup, and it's really fun and satisfying. I think I'll consolidate them in a larger program soon, using a keypad in a way similar to my [codepad program](https://github.com/scherepi/keypadCode) to select different tools.

----
*The setup, as it sits on my desk:*
![now_playing](https://github.com/user-attachments/assets/30b1352b-1609-42bd-bece-862fb9a6715c)
