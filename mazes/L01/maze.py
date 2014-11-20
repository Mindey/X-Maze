#-*- coding:utf-8 -*-

# This is game level A001
# All rooms have to be registered in a dictionary of the same name as the folder.
L01 = {}
path = 'mazes/L01/'
prerequisites = []

# ----------------------------------------- Room 1 ----------------------------------------- #

# Make a new room
L01['room_1'] = MazeRoom(root, music=path+'room_1_music.ogg', kind='Puzzle')

# Hang a tunnel
L01['tunnel_1'] = L01['room_1'].front.hangTunnel(questions=[], kind='Puzzle')
L01['tunnel_2'] = L01['room_1'].right.hangTunnel(questions=[], kind='Bricks')

# Hang a poster
L01['room_1'].left.hangPoster(path+'poster_1.png', scale=1.5)

# Make a room on tunnel

L01['room_2'] = MazeRoom(L01['tunnel_1'], music=path+'room_2_music.ogg', kind='Bricks')
