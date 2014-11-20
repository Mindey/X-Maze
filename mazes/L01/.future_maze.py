# Now let's say we have definition of rooms and tunels in terms of Python dictionary:

segment = {'r1': ['t1le', 't1ri'],
           'r2': []}

# Here we will loop over the definition, and generate the rooms and tunnels from it:

# Generating variable names on the fly: http://stackoverflow.com/questions/4010840/generating-variable-names-on-fly-in-python

# Initial room with its tunnels
r1 = MazeRoom(root)
t1le = r1.left.hangTunnel()
t1ri = r1.right.hangTunnel()

# Next room with its tunnels
r2 = MazeRoom(t1le)

