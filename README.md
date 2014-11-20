X-Maze
======
## About:
我写了这个程序为了试试把游戏成瘾现象应用太为了解决现实生活中的问题。
The software is intended to use *GAME ADDICTION* for real life *PROBLEM SOLVING* ([video](http://v.youku.com/v_show/id_XNTQ2MTgyNTU2.html)).

**PRINCIPLE** is to allow teachers to design their mazes with problems inside tunnels between rooms.<br>
**REWARD** is to meet other people who move same direction, to unlock secrets together, and get money.<br>
**钱流：** { 学校，大学，企业 } -> { 解决了在游戏里包括的问题的玩儿家 }

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

现在我觉得这个想法应该基于更一般的别的系统，比如，加密货币，人物管理系统，股市等。