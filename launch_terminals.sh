#!/usr/bin/env bash

# measurement in characters experimentally defined :)
WIDTH=75
HEIGHT=18

gnome-terminal --geometry ${WIDTH}x${HEIGHT}+0-0 -e "docker exec -it sender bash" & # left down
gnome-terminal --geometry ${WIDTH}x${HEIGHT}+0+0 -e "docker exec -it sender bash" & # left up
gnome-terminal --geometry ${WIDTH}x${HEIGHT}-0+0 -e "docker exec -it receiver bash" & # right up
gnome-terminal --geometry ${WIDTH}x${HEIGHT}-0-0 -e "docker logs -f receiver" & # right down