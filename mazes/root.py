# Maze Root

root = Entrance(Point3(0,-10,0), dim=Point2(0,0), direction='back')

for directory in sorted([d for d in os.listdir('mazes') if os.path.isdir(os.path.join('mazes',d))]):
    guess = os.path.join(os.getcwd(),os.path.join(os.path.join('mazes',directory),'maze.py'))
    if os.path.exists(guess):
        # Todo: Read file, and replace all 'abc/def/ghi.xxx' into os.path.join(os.getcwd(), 'abc/def/ghi.xxx') before execution:
        execfile(guess)
        if directory in vars().keys():
            for varname in vars()[directory].keys():
                self.mazeAreas.append(vars()[directory][varname])

 
