#!/bin/bash
# get the list of screens with the name "discordbot"
screens=$(screen -ls | grep discordbot | awk '{print $1}')
# get the oldest screen
oldest=$(echo "$screens" | head -n 1)
# send the quit command to the oldest screen
screen -X -S "$oldest" quit
