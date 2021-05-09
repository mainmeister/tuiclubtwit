# **tuiclubtwit**

Stream videos from club twit in a terminal window

# **Installation**

There are two environment variables that the program depends on.

`# set up configuration for the twit club streamer`

`# twitcluburl - the url from the twit club for your shows`

`export twitcluburl=https://twit.memberfulcontent.com/rss/9041?auth={your authorization here}`

`# twitclubstreamer - how to steam the url like "vlc {url}" which will cause vlc to play the url`

`export twitclubstreamer=vlc {url}`

The twitcluburl is the one you get from the club twit subscriber's Podcast page. This is a manditory setting. If this is missing then the program will abort with an appropriate error message "Set environment string twitcluburl to the url for your twitclub stream" and an exit code of 1.

When setting the program to play the stream, use {url} to place the url in the command line
# **Requirements**

Python3.6+

`sudo apt install python`

requests

`$ python -m pip install requests`

html2txt

`python -m pip install html2txt`

# **Usage**

The program is a command line python script. There are no command line arguments.

`$python main.py`
