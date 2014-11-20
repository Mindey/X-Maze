X-Maze
======

"The software would allow teachers to design their labyrinth rooms with problems, and interconnect into one large maze, with custom rewards in each following room."

Video: http://v.youku.com/v_show/id_XNTQ2MTgyNTU2.html

Try out the sample maze: http://mindey.com/3dmaze.zip

******************************************************************************
Developed on Ubuntu 12.04 (64 bit version):

1. Install **Panda3D 1.8.1**:
[http://www.panda3d.org/download.php?sdk&version=1.8.1](http://www.panda3d.org/download.php?sdk&version=1.8.1)

2. Git checkout, or download:
```bash
wget http://mindey.com/3dmaze.zip
unzip 3dmaze.zip
cd 3dmaze/
```

2. Run:
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

Note: this project is just a proof-of-concept. Not a scalable one.