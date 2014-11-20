X-Maze
======
## About:
The software is intended to use game addiction for real life problem solving ([video](http://v.youku.com/v_show/id_XNTQ2MTgyNTU2.html)).

The principle is to allow teachers to design their mazes with tunnels and problems inside tunnels.

1. Install **Panda3D 1.8.1**:
[http://www.panda3d.org/download.php?sdk&version=1.8.1](http://www.panda3d.org/download.php?sdk&version=1.8.1)

2. Run:
python main.py

## For example:

```bash
wget http://www.panda3d.org/download/panda3d-1.8.1/panda3d1.8_1.8.1~precise_amd64.deb
sudo dpkg -i panda3d1.8_1.8.1~precise_amd64.deb
wget http://mindey.com/3dmaze.zip
unzip 3dmaze.zip
cd 3dmaze/
python main.py
```

## Hello world:

```python
mkdir X-Maze/mazes/X/
touch X-Maze/mazes/X/maze.py
# maze.py
X = {}
X[1] = MazeRoom(root)
X[2] = X[1].front.hangTunnel()
X[3] = MazeRoom(X[2]) 
```

## More info:

* Origin: http://www.halfbakery.com/idea/3D_20Study_20Maze
* Note: this project is just a proof-of-concept. Not a scalable one.