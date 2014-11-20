X-Maze
======

"The software would allow teachers to design their labyrinth rooms with problems, and interconnect into one large maze, with custom rewards in each following room."

Video: http://v.youku.com/v_show/id_XNTQ2MTgyNTU2.html

Try out the sample maze: http://mindey.com/3dmaze.zip

******************************************************************************

In order to run this program, install Panda3D SDK ( http://www.panda3d.org ).
It was developed and tested with Panda3D SDK version 1.8.1.

******************************************************************************
If you are running Ubuntu 12.04 (64 bit version), you can run this in 2 steps:


3. Install:
http://www.panda3d.org/download.php?sdk&version=1.8.1

4. Run:
python main.py

******************************************************************************

Hello world:

```bash
mkdir X-Maze/mazes/X/
touch X-Maze/mazes/X/maze.py
```

```python
# maze.py
X = {}
X[1] = MazeRoom(root)
X[2] = X[1].front.hangTunnel()
X[3] = MazeRoom(X[2]) 
```

******************************************************************************
More info: http://www.halfbakery.com/idea/3D_20Study_20Maze
