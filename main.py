#
# 3DStudyMaze is a Panda3D application for building and
# running an education course in virtual environment.
#
# It will feature:
# - Simple maze definition language
# - Connectivity between mazes
# - Auto-adjusting room and tunnel sizes
# - Support-ticket instructor locks
# - LaTeX-editable walls
#
# It is based on the idea, published on Halfbakery:
# http://www.halfbakery.com/idea/3D_20Study_20Maze
#
# Panda3D game engine is available at:
# http://www.panda3d.org
# 
# Inyuki < Made in The Internet >
# Contact: mindey@gmail.com
#
# The initial commit is based on Panda3D sample program named "Bump-Mapping":
# http://www.panda3d.org/manual/index.php/Sample_Programs:_Normal_Mapping
# Licensed, probably, under http://www.panda3d.org/license.php
#

import direct.directbase.DirectStart
from panda3d.core import WindowProperties
from panda3d.core import TextNode
from panda3d.core import Point2, Point3, Vec3, Vec4
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import CardMaker
import sys, os
from pandac.PandaModules import Texture
from PIL import Image, ImageDraw
from pandac.PandaModules import TransparencyAttrib
from copy import copy
from direct.gui.DirectEntry import DirectEntry
from panda3d.core import TextureStage

rootNode = render.attachNewNode( 'rootNode' )


# We need a starting point for drawing either a room or a tunnel.
class Entrance:
    
    def __init__(self, WallTopLeft=Point3(), offset=Point2(), dim=Point2(0,0), direction='back', kind='entrance' ):

        self.dim = dim
        self.direction = direction
        self.offset = offset
        
        if direction == 'left':
            ExitLeftTop     = Point3(WallTopLeft + Point3( 0, offset.x, -offset.y) )
            ExitRightTop    = Point3(ExitLeftTop + Point3( 0, dim.x     ,                0) )
            ExitLeftBottom  = Point3(ExitLeftTop + Point3( 0, 0         ,      -dim.y) )
            ExitRightBottom = Point3(ExitLeftTop + Point3( 0, dim.x     ,      -dim.y) )

        if direction == 'right':
            ExitLeftTop     = Point3(WallTopLeft + Point3( 0, -offset.x, -offset.y) )
            ExitRightTop    = Point3(ExitLeftTop + Point3( 0, -dim.x     ,                0) )
            ExitLeftBottom  = Point3(ExitLeftTop + Point3( 0, 0          ,      -dim.y) )
            ExitRightBottom = Point3(ExitLeftTop + Point3( 0, -dim.x     ,      -dim.y) )

        if direction == 'back':
            ExitLeftTop     = Point3(WallTopLeft + Point3( -offset.x, 0, -offset.y) )
            ExitRightTop    = Point3(ExitLeftTop + Point3( -dim.x     , 0,                0) )
            ExitLeftBottom  = Point3(ExitLeftTop + Point3( 0               , 0,      -dim.y) )
            ExitRightBottom = Point3(ExitLeftTop + Point3( -dim.x     , 0,      -dim.y) )

        if direction == 'front':
            ExitLeftTop     = Point3(WallTopLeft + Point3( offset.x, 0, -offset.y) )
            ExitRightTop    = Point3(ExitLeftTop + Point3( dim.x     , 0,                0) )
            ExitLeftBottom  = Point3(ExitLeftTop + Point3( 0         , 0,      -dim.y) )
            ExitRightBottom = Point3(ExitLeftTop + Point3( dim.x     , 0,      -dim.y) )

        if direction == 'bottom':
            ExitLeftTop     = Point3(WallTopLeft + Point3( offset.x, -offset.y, 0) )
            ExitRightTop    = Point3(ExitLeftTop + Point3( dim.x     ,                0, 0) )
            ExitLeftBottom  = Point3(ExitLeftTop + Point3( 0         ,      -dim.y, 0) )
            ExitRightBottom = Point3(ExitLeftTop + Point3( dim.x     ,      -dim.y, 0) )

        if direction == 'top':
            ExitLeftTop     = Point3(WallTopLeft + Point3( offset.x, offset.y, 0) )
            ExitRightTop    = Point3(ExitLeftTop + Point3( dim.x     ,               0, 0) )
            ExitLeftBottom  = Point3(ExitLeftTop + Point3( 0         ,      dim.y, 0) )
            ExitRightBottom = Point3(ExitLeftTop + Point3( dim.x     ,      dim.y, 0) )


        if kind == 'entrance':
            self.ExitLeftTop = ExitLeftTop
            self.ExitRightTop = ExitRightTop
            self.ExitLeftBottom = ExitLeftBottom
            self.ExitRightBottom = ExitRightBottom
        if kind == 'exit': 
            if direction in ['left', 'right', 'back', 'front']:
                self.ExitLeftTop     = ExitRightTop
                self.ExitRightTop    = ExitLeftTop
                self.ExitLeftBottom  = ExitRightBottom
                self.ExitRightBottom = ExitLeftBottom
            if direction in ['bottom', 'top']:
                self.ExitLeftTop     = ExitLeftBottom
                self.ExitRightTop    = ExitRightBottom
                self.ExitLeftBottom  = ExitLeftTop
                self.ExitRightBottom = ExitRightTop
            if direction == 'left': self.direction = 'right'
            if direction == 'right': self.direction = 'left'
            if direction == 'back': self.direction = 'front'
            if direction == 'front': self.direction = 'back'
            if direction == 'bottom': self.direction = 'top'
            if direction == 'top': self.direction = 'bottom'


class Wall:
    
    def __init__(self, LeftBottom=Point3( -15, 50, -10), RightBottom=Point3(  15, 50, -10), \
                       LeftTop=Point3( -15, 50,  10), RightTop=Point3(  15, 50,  10) ):
        
        self.cm   = CardMaker('card')
        self.cm.setUvRange( Point2( 0, 0 ), Point2( 1, 1) )
        self.cm.setFrame( LeftBottom, RightBottom, RightTop, LeftTop )
        self.card = rootNode.attachNewNode(self.cm.generate())
        
class Room:

    def __init__(self, RightFrontTop, RightFrontBottom, RightBackTop, RightBackBottom, \
                       LeftFrontTop,   LeftFrontBottom, LeftBackTop,  LeftBackBottom):

        self.left_wall   = Wall( LeftBackBottom, LeftFrontBottom,  LeftBackTop, LeftFrontTop,  Tile='left.png')
        self.right_wall  = Wall( RightFrontBottom, RightBackBottom, RightFrontTop, RightBackTop,  Tile='right.png')
        self.back_wall   = Wall( RightBackBottom, LeftBackBottom, RightBackTop, LeftBackTop,  Tile='back.png')
        self.front_wall  = Wall( LeftFrontBottom, RightFrontBottom, LeftFrontTop, RightFrontTop,  Tile='front.png')
        self.bottom_wall = Wall( LeftBackBottom, RightBackBottom, LeftFrontBottom, RightFrontBottom,  Tile='bottom.png')
        self.top_wall    = Wall( LeftFrontTop, RightFrontTop, LeftBackTop, RightBackTop,  Tile='top.png')

class Tunnel:

    def __init__(self, RightFrontTop, RightFrontBottom, RightBackTop, RightBackBottom, \
                       LeftFrontTop,   LeftFrontBottom, LeftBackTop,  LeftBackBottom):

        self.left_wall   = Wall( LeftBackBottom, LeftFrontBottom,  LeftBackTop, LeftFrontTop,  Tile='left.png')
        self.right_wall  = Wall( RightFrontBottom, RightBackBottom, RightFrontTop, RightBackTop,  Tile='right.png')
        self.bottom_wall = Wall( LeftBackBottom, RightBackBottom, LeftFrontBottom, RightFrontBottom,  Tile='bottom.png')
        self.top_wall    = Wall( LeftFrontTop, RightFrontTop, LeftBackTop, RightBackTop,  Tile='top.png')

class Poster(Wall):
    
    def __init__(self, WallTopLeft=Point3(), PosterLeftTop=Point2(), directions=('y+','z+'), document='hi-res.png', scale=1.0, aspect='3:4' ):

        # Here, just needs to determine the positions of the 'LeftTop', 'RightTop', 'LeftBottom', 'RightBottom'  points.
        # They all will depend on the coordinate of the maze wall's point of reference (e.g., LeftTop corner of the wall),
        # and the position, and the directions, along which to add the position.x and position.y coordinates.

        # Determine dimensions of the document:
        if document.split('.')[-1] in [ 'avi', 'mp4' ]:
            # If the document is video:
            if aspect == '9:16':
                img_h, img_w = 9*200*scale, 16*200*scale
            else:
                img_h, img_w = 3*500*scale, 4*500*scale
        else:
            # If the document is image:
            img=Image.open(document,'r')
            img_w, img_h = img.size

        document_x, document_y = scale*img_w/100, scale*img_h/100

        # Save filename for later use in activating videos.
        self.document = document

        # Margin from the wall
        m = 0.01

        # Margin for activation area (it could later be a function of img_h, img_w):
        a = 5.

        # The coordinates depend on the orientation of the wall, here specified by 'directions' instead of 'face'.
        # Maybe I should just have rotation matrices for each case, and write it more compactly, but for now:
        if directions == ('y+','z+'):            # Poster on left wall
            margin = Point3(m,0,0)
            active = Point3(a,0,0)
            PosterLeftTop     = Point3(WallTopLeft   + Point3( 0, PosterLeftTop.x, -PosterLeftTop.y) + margin)
            PosterRightTop    = Point3(PosterLeftTop + Point3( 0, document_x     ,                0) )
            PosterLeftBottom  = Point3(PosterLeftTop + Point3( 0, 0              ,      -document_y) )
            PosterRightBottom = Point3(PosterLeftTop + Point3( 0, document_x     ,      -document_y) )

        if directions == ('y-','z+'):            # Poster on right wall
            margin = Point3(-m,0,0)
            active = Point3(-a,0,0)
            PosterLeftTop     = Point3(WallTopLeft   + Point3( 0, -PosterLeftTop.x, -PosterLeftTop.y) + margin)
            PosterRightTop    = Point3(PosterLeftTop + Point3( 0, -document_x     ,                0) )
            PosterLeftBottom  = Point3(PosterLeftTop + Point3( 0, 0               ,      -document_y) )
            PosterRightBottom = Point3(PosterLeftTop + Point3( 0, -document_x     ,      -document_y) )

        if directions == ('x-','z+'):            # Poster on back wall
            margin = Point3(0,m,0)
            active = Point3(0,a,0)
            PosterLeftTop     = Point3(WallTopLeft   + Point3( -PosterLeftTop.x, 0, -PosterLeftTop.y) + margin)
            PosterRightTop    = Point3(PosterLeftTop + Point3( -document_x     , 0,                0) )
            PosterLeftBottom  = Point3(PosterLeftTop + Point3( 0               , 0,      -document_y) )
            PosterRightBottom = Point3(PosterLeftTop + Point3( -document_x     , 0,      -document_y) )

        if directions == ('x+','z+'):            # Poster on front wall
            margin = Point3(0,-m,0)
            active = Point3(0,-a,0)
            PosterLeftTop     = Point3(WallTopLeft   + Point3( PosterLeftTop.x, 0, -PosterLeftTop.y) + margin)
            PosterRightTop    = Point3(PosterLeftTop + Point3( document_x     , 0,                0) )
            PosterLeftBottom  = Point3(PosterLeftTop + Point3( 0              , 0,      -document_y) )
            PosterRightBottom = Point3(PosterLeftTop + Point3( document_x     , 0,      -document_y) )

        if directions == ('x+','y+'):            # Poster on bottom wall
            margin = Point3(0,0,m)
            active = Point3(0,0,a)
            PosterLeftTop     = Point3(WallTopLeft   + Point3( PosterLeftTop.x, -PosterLeftTop.y, 0) + margin)
            PosterRightTop    = Point3(PosterLeftTop + Point3( document_x     ,                0, 0) )
            PosterLeftBottom  = Point3(PosterLeftTop + Point3( 0              ,      -document_y, 0) )
            PosterRightBottom = Point3(PosterLeftTop + Point3( document_x     ,      -document_y, 0) )

        if directions == ('x+','y-'):            # Poster on top wall
            margin = Point3(0,0,-m)
            active = Point3(0,0,-a)
            PosterLeftTop     = Point3(WallTopLeft   + Point3( PosterLeftTop.x, PosterLeftTop.y, 0) + margin)
            PosterRightTop    = Point3(PosterLeftTop + Point3( document_x     ,               0, 0) )
            PosterLeftBottom  = Point3(PosterLeftTop + Point3( 0              ,      document_y, 0) )
            PosterRightBottom = Point3(PosterLeftTop + Point3( document_x     ,      document_y, 0) )

        Wall.__init__(self, LeftBottom=PosterLeftBottom, RightBottom=PosterRightBottom, \
                       LeftTop=PosterLeftTop, RightTop=PosterRightTop ) 

        self.tex = loader.loadTexture(document)
        self.card.setTexture(self.tex)

        if document.split('.')[-1] in [ 'avi', 'mp4' ]:
            self.card.setTexScale(TextureStage.getDefault(), self.tex.getTexScale())
            self.media = loader.loadSfx(document)
            self.tex.synchronizeTo(self.media)
        else:
            self.tex.setMinfilter(Texture.FTLinearMipmapLinear)

        # Poster activation area (used for starting the playing of a movie)

        # For activation area
        FurtherLeftTop    = Point3(PosterLeftTop     + active)
        FurtherRightTop   = Point3(PosterRightTop    + active)
        FurtherLeftBottom = Point3(PosterLeftBottom  + active)
        FurtherRightBottom= Point3(PosterRightBottom + active)

        PointList = [PosterLeftTop, PosterRightTop, PosterLeftBottom, PosterRightBottom, \
                     FurtherLeftTop, FurtherRightTop, FurtherLeftBottom, FurtherRightBottom]

        self.x_minus = min([item.x for item in PointList])
        self.x_plus  = max([item.x for item in PointList])
        self.y_minus = min([item.y for item in PointList])
        self.y_plus  = max([item.y for item in PointList])
        self.z_minus = min([item.z for item in PointList])
        self.z_plus  = max([item.z for item in PointList])

    def addPage():
        pass

    def addFrame():
        pass

    def flipPage():
        pass

class MazeWall:
    
    def __init__(self, origin=Point3(0,50,0), dim=Point2(120,120), orientation='front', reference='center' ):

        self.exits = []

        # Possible references of the wall: center and corners
        references = [(0, (  0., 0.), 'xy',   'center'     ),
                      (1, (  1., 1.), 'x+y+', 'LeftBottom' ),
                      (2, (  1.,-1.), 'x+y-', 'LeftTop'    ),
                      (3, ( -1., 1.), 'x-y+', 'RightBottom'),
                      (4, ( -1, -1.), 'x-y-', 'RightTop'   )]

        # Finding index of the reference
        for item in references:
            if reference in item:
                reference = item[0]

        # Possible orientations of the wall: corresponding to the walls they are used to draw for a room.
        orientations = [(0, 'x-', 'left'  ),
                        (1, 'x+', 'right' ),
                        (2, 'y-', 'back'  ),
                        (3, 'y+', 'front' ),
                        (4, 'z-', 'bottom'),
                        (5, 'z+', 'top'   )]

        # Finding index of the orientation
        for item in orientations:
            if orientation in item:
                orientation = item[0]

        # Delta is half the distance from center
        D = Point2( dim.x/2., dim.y/2.)
        d = Point2( references[reference][1] )
        delta2d = Point2(D.x*d.x, D.y*d.y)

        # Possible four corners in 2d:
        LeftBottom2d  = Point2(0,0) + Point2(-dim.x/2., -dim.y/2.) + delta2d
        RightBottom2d = Point2(0,0) + Point2( dim.x/2., -dim.y/2.) + delta2d
        LeftTop2d     = Point2(0,0) + Point2(-dim.x/2.,  dim.y/2.) + delta2d
        RightTop2d    = Point2(0,0) + Point2( dim.x/2.,  dim.y/2.) + delta2d
        corners2d = [LeftBottom2d, RightBottom2d, LeftTop2d, RightTop2d]
        
        # What 3D coordinates these delta has to be applied to, depends on card's orientation:
        if orientation == 0: x = 'y+'; y = 'z+'
        if orientation == 1: x = 'y-'; y = 'z+'
        if orientation == 2: x = 'x-'; y = 'z+'
        if orientation == 3: x = 'x+'; y = 'z+'
        if orientation == 4: x = 'x+'; y = 'y+'
        if orientation == 5: x = 'x+'; y = 'y-'
        # Saving for use in method hangPoster
        self.x = x; self.y = y
        # Saving for use in method hangExit
        self.orientation = orientations[orientation][2]
        # Saving for use in method cutWindow
        self.dim = dim

        # Possible four corners in 3d:
        corners3d = [Point3(0,0,0)+origin, Point3(0,0,0)+origin, Point3(0,0,0)+origin, Point3(0,0,0)+origin]

        if x == 'x+':
            for i in range(4): corners3d[i] += Point3(corners2d[i].x, 0., 0.)
        if x == 'x-':
            for i in range(4): corners3d[i] -= Point3(corners2d[i].x, 0., 0.)
        if x == 'y+':
            for i in range(4): corners3d[i] += Point3(0., corners2d[i].x, 0.)
        if x == 'y-':
            for i in range(4): corners3d[i] -= Point3(0., corners2d[i].x, 0.)
        if y == 'y+':
            for i in range(4): corners3d[i] += Point3(0., corners2d[i].y, 0.)
        if y == 'y-':
            for i in range(4): corners3d[i] -= Point3(0., corners2d[i].y, 0.)
        if y == 'z+':
            for i in range(4): corners3d[i] += Point3(0., 0., corners2d[i].y)

        self.LeftBottom   = Point3(corners3d[0])
        self.RightBottom  = Point3(corners3d[1])
        self.LeftTop      = Point3(corners3d[2])
        self.RightTop     = Point3(corners3d[3])

        self.wall    = Wall( self.LeftBottom, self.RightBottom, self.LeftTop, self.RightTop )
        self.posters = {}

        # Store texture filename as a variable
        self.texture = os.path.join('temp', str(id(self))+'_tiled.png')
        self.alpha   = os.path.join('temp', str(id(self))+'_alpha.png')

        self.addTexture( Tile=orientations[orientation][2]+'.png', repeat=(10,10), bg_dim = (dim.x*10,dim.y*10) )
        self.addAlpha()
        self.updateTexture()

    def addTexture(self, Tile='default.png', repeat=(10,10), bg_dim=(0,0)):

        Tile = os.path.join('textures', Tile)

        # In case the Tile file does not exist, create and use default.png, so that it could be changed later.
        if not os.path.isfile(os.path.join(os.getcwd(),Tile)):
            im = Image.new('RGB', (150,150)); draw = ImageDraw.Draw(im)
            draw.rectangle([(0, 0), (150, 150)], outline='white');    draw.text((55, 70), "Default")
            im.save(os.path.join('textures', 'default.png'), 'PNG');    Tile = os.path.join('textures', 'default.png')

        # Reading the tile
        img=Image.open(Tile,'r')
        img_w, img_h = img.size

        # If the wall's dimensions in pixelsaren't specified
        if bg_dim[0] == 0 or bg_dim[1] == 0:

            # We tile by creating the image of the size it would take if you repeat the tiles that many times.
            background = Image.new("RGB", ( img_w*repeat[0], img_h*repeat[1]), (255,255,255))
            for i in range(repeat[0]):
                for j in range(repeat[1]):
                    background.paste(img,(i*img_w, j*img_h))

        else:
            # We tile into the dimensions:
            background = Image.new("RGB", (int(bg_dim[0]), int(bg_dim[1])), (255,255,255))
            for i in range(int(bg_dim[0]/img_w+1)):
                for j in range(int(bg_dim[1]/img_h+1)):
                    background.paste(img,(i*img_w,j*img_h))
            
        # We add a one-pixel white corner:
        draw = ImageDraw.Draw(background)
        draw.rectangle([(0, 0), (img_w*repeat[0], img_h*repeat[1])], outline='white')

        background.save(self.texture, 'PNG')
            
    def addAlpha(self):

        # Making transparency mapping file
        im = Image.new("RGB", (int(self.dim.x)*10, int(self.dim.y)*10), (255,255,255)); draw = ImageDraw.Draw(im)
        im.save(self.alpha)

    def cutWindow(self, window=(Point2(25,20),Point2(100,100))):
        # Reading the alpha tile
        im = Image.open(self.alpha,'r')
        img_w, img_h = im.size
        # How many pixels per 'blender unit'
        ratio_x, ratio_y = img_w/self.dim.x, img_h/self.dim.y
        draw = ImageDraw.Draw(im)
        draw.rectangle([(int(ratio_x*window[0].x), int(ratio_y*window[0].y)), \
                        (int(ratio_x*window[1].x-1), int(ratio_y*window[1].y-1))], fill="#000000")
        im.save(self.alpha, "PNG")
        self.updateTexture()

    def updateTexture(self):
        # Try to add default textures depending on the orientation of the wall
        try:
            self.wall.tex = loader.loadTexture(self.texture, self.alpha)
            self.wall.tex.reload()
            self.wall.card.setTexture(self.wall.tex)
            self.wall.card.setTransparency(True)
            self.wall.card.setTransparency(TransparencyAttrib.MBinary)
        except:
            pass

    def newTexture(self, Tile='default.png', repeat=(10,10), bg_dim=(0,0)):
        if not os.path.isfile('textures/%s' % Tile.split('/')[-1]):
                os.system('cp %s textures/' % Tile)
        else:
            if not os.stat('textures/%s' % Tile.split('/')[-1]).st_size == os.stat(Tile).st_size:
                    os.system('cp %s textures/' % Tile)

        Tile = Tile.split('/')[-1]
        self.addTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)
        self.updateTexture()

    def hangPoster(self, document='hi-res.png', offset=Point2(1,1), scale=1.0, aspect='3:4'):
        self.posters[document] = Poster( self.LeftTop, offset, (self.x, self.y), document, scale, aspect )

    def hangPosters(self, folder='.', starting=1, rows=3, cols=4, scale=1.0, spacing=0.25, offset=Point2(0,0)):
        # ( With an assumption that all the pages of the book are equal rectangles )

        # Get the pixel size of one page
        img=Image.open(os.path.join(folder,str(starting)+'.png'),'r')
        img_w, img_h = img.size

        # Get the dimensions of a single page in blender units
        doc_x, doc_y = scale*img_w/100, scale*img_h/100

        # Compute the dimensions of the resulting mat, with spacing
        rez_x = doc_x * cols + spacing * (cols + 1)
        rez_y = doc_y * rows + spacing * (rows + 1)

        # Return an informative error if the size exceeds dimensions of the wall
        if self.dim.x < rez_x or self.dim.y < rez_y:
            print 'Either height or width exceed the corresponding dimension of the wall.'
            print 'Dimensions of the wall: x=%s, y=%s' % (self.dim.x, self.dim.y)
            print 'Dimensions of the mat:  x=%s, y=%s' % (rez_x, rez_y)
        else:
            # Compute the upper limits for coordinates within which this point can be:
            max_x = self.dim.x - rez_x
            max_y = self.dim.y - rez_y

            # IF LeftTop corner of the mat is not outside the limits:
            if 0.0 <= offset.x < max_x and 0.0 <= offset.y < max_y:
                print 'Adding the pages to a wall.'
                I = offset + Point2(spacing, spacing)
                D = Point2(doc_x+spacing, doc_y+spacing)
                i = 0
                for row in range(rows):
                    for col in range(cols):

                        fn = os.path.join(folder,str(starting+i)+'.png')
                        pos = I + Point2(col*D.x,0) + Point2(0,row*D.y)

                        if os.path.isfile(fn):
                            self.hangPoster(fn, pos, scale)

                        i += 1
            else:
                print 'Although dimensions are right, your offset point is out of range.'
                print 'Range allows for offset: 0.0 < x < %s, 0.0 < y < %s' % (max_x, max_y)
                print 'The actual dimensions of the offset: x=%s, y=%s' % (offset.x, offset.y)

    def hangExit(self, offset=Point2(1,1), dim=Point2(5,8)):
        self.cutWindow((offset, Point2(offset+dim)))
        e = Entrance( self.LeftTop, offset, dim, self.orientation, kind='exit')
        self.exits.append( e )
        return e

    def hangTunnel(self, offset=0, dim=Point2(10,10), questions = 0, kind='Default'):
              # questions =[('problem1.png', 'answer1'), \
              #            ('problem2.png', 'answer2'), \
              #            ('problem3.png', 'answer3'), \
              #                    ]):
        if questions == 0:
            questions = []
        if offset == 0:
            # Set it so that the tunnel would be hung at the center of the wall:
            n = self.dim.x/2. - dim.x/2.
            m = self.dim.y/2. - dim.y/2.
            offset = Point2(n, m)

        exit = self.hangExit(offset, dim)
        self.exits.append(exit)
        tunnel = MazeTunnel(exit, questions, kind=kind)
        return tunnel

class MazeTunnel:
    def __init__(self, entrance, questions=[], kind='Default'): #('problem1.png', 'answer1')]):

        # Since tunnel is a container of questions, it is appropriate to start estimating the length
        # depending on the questions answered, and only add the margin 'epsilon' at the end of tunnel
        # once all the questions had been answered.

        # At this moment, the questions will have to be passed to constructor function. However, it is preferable to have flexible 'addQuestion' method.
        # The problem is that all the later rooms' coordinates will depend on the tunnel's length, so the part of maze that follows that tunnel would have
        # to be all updated. 

        # Here, I added 'invisible question', as it is not actually appearing, after all: in this implementation,
        # we let the user thrugh the tunnel when the current answer is equal to the number of questions.
        questions += [('invisible', 'question')]
        self.questions = questions
        self.length = len(questions)*10 

        self.epsilon = 5
        self.which = Point3(0,0,0)
                               # LEFT   RIGHT   BOTTOM   TOP
        if entrance.direction == 'left': # x+
            self.directions = ['front','back','bottom','top']
            self.left   = MazeWall(entrance.ExitRightTop, Point2(self.length, entrance.dim.y), orientation='front', reference='LeftTop')
            self.right  = MazeWall(entrance.ExitLeftTop, Point2(self.length, entrance.dim.y), orientation='back', reference='RightTop')
            self.bottom = MazeWall(entrance.ExitRightBottom, Point2(self.length, entrance.dim.x), orientation='bottom', reference='LeftTop')
            self.top    = MazeWall(entrance.ExitRightTop, Point2(self.length, entrance.dim.x), orientation='top', reference='LeftBottom')
            self.exit = Entrance(entrance.ExitLeftTop+Point3(self.length,0,0), offset=Point2(), dim=entrance.dim, direction=entrance.direction, kind='entrance')
            self.dim = Point3(self.length, entrance.dim.x, entrance.dim.y)
            self.which.x = 1
        if entrance.direction == 'right': # x-
            self.directions = ['back','front','bottom','top']
            self.left   = MazeWall(entrance.ExitRightTop, Point2(self.length,entrance.dim.y), orientation='back', reference='LeftTop')
            self.right  = MazeWall(entrance.ExitLeftTop, Point2(self.length,entrance.dim.y), orientation='front', reference='RightTop')
            self.bottom = MazeWall(entrance.ExitRightBottom, Point2(self.length, entrance.dim.x), orientation='bottom', reference='RightBottom')
            self.top    = MazeWall(entrance.ExitRightTop, Point2(self.length, entrance.dim.x), orientation='top', reference='RightTop')
            self.exit = Entrance(entrance.ExitLeftTop+Point3(-self.length,0,0), offset=Point2(), dim=entrance.dim, direction=entrance.direction, kind='entrance')
            self.dim = Point3(self.length, entrance.dim.x, entrance.dim.y)
            self.which.x = -1
        if entrance.direction == 'back': # y+
            self.directions = ['left','right','bottom','top']
            self.left   = MazeWall(entrance.ExitRightTop, Point2(self.length,entrance.dim.y), orientation='left', reference='LeftTop')
            self.right  = MazeWall(entrance.ExitLeftTop, Point2(self.length,entrance.dim.y), orientation='right', reference='RightTop')
            self.bottom = MazeWall(entrance.ExitRightBottom, Point2(entrance.dim.x, self.length), orientation='bottom', reference='LeftBottom')
            self.top    = MazeWall(entrance.ExitLeftTop, Point2(entrance.dim.x, self.length), orientation='top', reference='RightTop')
            self.exit = Entrance(entrance.ExitLeftTop+Point3(0,self.length,0), offset=Point2(), dim=entrance.dim, direction=entrance.direction, kind='entrance')
            self.dim = Point3(entrance.dim.x, self.length, entrance.dim.y)
            self.which.y = 1
        if entrance.direction == 'front': # y-
            self.directions = ['right','left','bottom','top']
            self.left   = MazeWall(entrance.ExitRightTop, Point2(self.length,entrance.dim.y), orientation='right', reference='LeftTop')
            self.right  = MazeWall(entrance.ExitLeftTop, Point2(self.length,entrance.dim.y), orientation='left', reference='RightTop')
            self.bottom = MazeWall(entrance.ExitRightBottom, Point2(entrance.dim.x,self.length), orientation='bottom', reference='RightTop')
            self.top    = MazeWall(entrance.ExitLeftTop, Point2(entrance.dim.x,self.length), orientation='top', reference='LeftBottom')
            self.exit = Entrance(entrance.ExitLeftTop+Point3(0,-self.length,0), offset=Point2(), dim=entrance.dim, direction=entrance.direction, kind='entrance')
            self.dim = Point3(entrance.dim.x, self.length, entrance.dim.y)
            self.which.y = -1
        if entrance.direction == 'bottom': # z+
            self.directions = ['left','right','front','back']
            self.left   = MazeWall(entrance.ExitLeftBottom, Point2(entrance.dim.y,self.length), orientation='left', reference='LeftBottom')
            self.right  = MazeWall(entrance.ExitRightTop, Point2(entrance.dim.y,self.length), orientation='right', reference='LeftBottom')
            self.bottom = MazeWall(entrance.ExitRightTop, Point2(entrance.dim.x,self.length), orientation='front', reference='RightBottom')
            self.top    = MazeWall(entrance.ExitRightBottom, Point2(entrance.dim.x, self.length), orientation='back', reference='LeftBottom')
            self.exit = Entrance(entrance.ExitLeftTop+Point3(0,0,self.length), offset=Point2(), dim=entrance.dim, direction=entrance.direction, kind='entrance')
            self.dim = Point3(entrance.dim.x, entrance.dim.y, self.length)
            self.which.z = 1
        if entrance.direction == 'top':
            self.directions = ['left','right','back','front']
            self.left   = MazeWall(entrance.ExitLeftTop, Point2(entrance.dim.y,self.length), orientation='left', reference='LeftTop')
            self.right  = MazeWall(entrance.ExitRightTop, Point2(entrance.dim.y,self.length), orientation='right', reference='RightTop')
            self.bottom = MazeWall(entrance.ExitLeftTop, Point2(entrance.dim.x,self.length), orientation='back', reference='RightTop')
            self.top    = MazeWall(entrance.ExitLeftBottom, Point2(entrance.dim.x, self.length), orientation='front', reference='LeftTop')
            self.exit = Entrance(entrance.ExitLeftTop+Point3(0,0,-self.length), offset=Point2(), dim=entrance.dim, direction=entrance.direction, kind='entrance')
            self.dim = Point3(entrance.dim.x, entrance.dim.y, self.length)
            self.which.z = -1

        # Find the center of the area:
        total = entrance.ExitLeftTop + self.exit.ExitRightBottom
        self.center = Point3(total.x/2, total.y/2, total.z/2)

        self.update_limits()

        # Painting the walls:
        if entrance.direction in ['front', 'back']:
            repeat1 = (len(questions),1)
            repeat2 = (len(questions),1)
            repeat3 = (1,len(questions))
            repeat4 = (1,len(questions))

        if entrance.direction in ['left', 'right']:
            repeat1 = (len(questions),1)
            repeat2 = (len(questions),1)
            repeat3 = (len(questions), 1)
            repeat4 = (len(questions), 1)

        if entrance.direction in ['bottom', 'top']:
            repeat1 = (1, len(questions))
            repeat2 = (1, len(questions))
            repeat3 = (1, len(questions))
            repeat4 = (1, len(questions))
        
        if kind == 'Puzzle':
            self.left.newTexture(Tile='textures/peace.gif', repeat=repeat1, bg_dim=(0,0))
            self.right.newTexture(Tile='textures/peace.gif', repeat=repeat2, bg_dim=(0,0))
            self.bottom.newTexture(Tile='textures/peace.gif', repeat=repeat3, bg_dim=(0,0))
            self.top.newTexture(Tile='textures/peace.gif', repeat=repeat4, bg_dim=(0,0))
        elif kind == 'Bricks':
            self.left.newTexture(Tile='textures/checks.jpg', repeat=repeat1, bg_dim=(0,0))
            self.right.newTexture(Tile='textures/checks.jpg', repeat=repeat2, bg_dim=(0,0))
            self.bottom.newTexture(Tile='textures/checks.jpg', repeat=repeat3, bg_dim=(0,0))
            self.top.newTexture(Tile='textures/checks.jpg', repeat=repeat4, bg_dim=(0,0))
        elif kind == 'Marvel':
            self.left.newTexture(Tile='textures/autumnleaves.jpg', repeat=repeat1, bg_dim=(0,0))
            self.right.newTexture(Tile='textures/autumnleaves.jpg', repeat=repeat2, bg_dim=(0,0))
            self.bottom.newTexture(Tile='textures/autumnleaves.jpg', repeat=repeat3, bg_dim=(0,0))
            self.top.newTexture(Tile='textures/autumnleaves.jpg', repeat=repeat4, bg_dim=(0,0))
        elif kind == 'Colorful':
            self.left.newTexture(Tile='textures/turtlegirl.png', repeat=repeat1, bg_dim=(0,0))
            self.right.newTexture(Tile='textures/turtlegirl.png', repeat=repeat2, bg_dim=(0,0))
            self.bottom.newTexture(Tile='textures/turtlegirl.png', repeat=repeat3, bg_dim=(0,0))
            self.top.newTexture(Tile='textures/turtlegirl.png', repeat=repeat4, bg_dim=(0,0))

            
            

    def update_limits(self, current=1):
        # Update the number of problems solved in this tunnel.
        try:
            self.current_problem += 1
        except:
            self.current_problem = current

        self.answer = self.questions[self.current_problem-1][1]

        remaining_problems = len(self.questions) - self.current_problem
        
        # Add epsilon only to the nearer end of the tunnel:
        self.x_minus = self.center.x - self.dim.x/2
        if self.which.x == 1: self.x_minus -= abs(self.which.x)*self.epsilon 
        self.x_plus  = self.center.x + self.dim.x/2
        if self.which.x ==-1: self.x_plus  += abs(self.which.x)*self.epsilon
        self.y_minus = self.center.y - self.dim.y/2
        if self.which.y == 1: self.y_minus -= abs(self.which.y)*self.epsilon
        self.y_plus  = self.center.y + self.dim.y/2
        if self.which.y ==-1: self.y_plus  += abs(self.which.y)*self.epsilon
        self.z_minus = self.center.z - self.dim.z/2
        if self.which.z == 1: self.z_minus -= abs(self.which.z)*self.epsilon
        self.z_plus  = self.center.z + self.dim.z/2
        if self.which.z ==-1: self.z_plus  += abs(self.which.z)*self.epsilon

        # Correction depending on questions answered:
        if self.which.x == 1: self.x_plus   -= remaining_problems*10.
        if self.which.x ==-1: self.x_minus  += remaining_problems*10.
        if self.which.y == 1: self.y_plus   -= remaining_problems*10.
        if self.which.y ==-1: self.y_minus  += remaining_problems*10.
        if self.which.z == 1: self.z_plus   -= remaining_problems*10.
        if self.which.z ==-1: self.z_minus  += remaining_problems*10.
        
        # If all of the poroblems had been solved, add epsilon to the further end of the tunnel:
        if self.current_problem == len(self.questions):
            if self.which.x ==-1: self.x_minus -= abs(self.which.x)*self.epsilon 
            if self.which.x == 1: self.x_plus  += abs(self.which.x)*self.epsilon
            if self.which.y ==-1: self.y_minus -= abs(self.which.y)*self.epsilon
            if self.which.y == 1: self.y_plus  += abs(self.which.y)*self.epsilon
            if self.which.z ==-1: self.z_minus -= abs(self.which.z)*self.epsilon
            if self.which.z == 1: self.z_plus  += abs(self.which.z)*self.epsilon

        # For active zone (zone in which the question is activated)

        # Start with copying the coordinates of the tunnel zone:
        self.active_x_minus = copy(self.x_minus)
        self.active_x_plus  = copy(self.x_plus)
        self.active_y_minus = copy(self.y_minus)
        self.active_y_plus  = copy(self.y_plus)
        self.active_z_minus = copy(self.z_minus)
        self.active_z_plus  = copy(self.z_plus)

        # If not all problems of the tunnel are solved, then, depending on the direction of the tunnel, modify
        if self.current_problem < len(self.questions):

            # the limits along that axis by either adding or subtracting from either positive or negative tunnel limit.

            if self.which == Point3(-1, 0, 0): # x-
                self.active_x_minus = copy(self.x_minus)
                self.active_x_plus  = self.active_x_minus + 10
            if self.which == Point3( 1, 0, 0): # x+
                self.active_x_plus = copy(self.x_plus)
                self.active_x_minus = self.active_x_plus - 10
            if self.which == Point3( 0,-1, 0): # y-
                self.active_y_minus = copy(self.y_minus)
                self.active_y_plus  = self.active_y_minus + 10
            if self.which == Point3( 0, 1, 0): # y+
                self.active_y_plus = copy(self.y_plus)
                self.active_y_minus = self.active_y_plus - 10
            if self.which == Point3( 0, 0,-1): # z-
                self.active_z_minus = copy(self.z_minus)
                self.active_z_plus  = self.active_z_minus + 10
            if self.which == Point3( 0, 0, 1): # z+
                self.active_z_plus = copy(self.z_plus)
                self.active_z_minus = self.active_z_plus - 10
        else:

            # Make arbitrary non-zero (cause zero very popular starting point), zero-volume point

            self.active_x_minus = self.active_x_plus
            self.active_y_minus = self.active_y_plus
            self.active_z_minus = self.active_z_plus

    def setTextures(self, Tile='default.png', repeat=(10,10), bg_dim=(0,0)):
        self.left.newTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)
        self.right.newTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)
        self.bottom.newTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)
        self.top.newTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)

    def __repr__(self):
        return str((self.x_minus, self.x_plus, self.y_minus, self.y_plus, self.z_minus, self.z_plus))

        
class MazeRoom:

    def __init__(self, entrance, dim=Point3(50,50,50), offset=0, music='basic.ogg', kind='Default'):

        if offset == 0:
            # we need to choose the wall, the dimensions of which we are going to take:

            try:  # in case it is a tunnel
                if entrance.exit.direction in ['left', 'right']:
                    x, y = dim.y/2., dim.z/2.
                    x -= entrance.dim.y/2.
                    y -= entrance.dim.z/2.
                if entrance.exit.direction in ['back', 'front']:
                    x, y = dim.x/2., dim.z/2.
                    x -= entrance.dim.x/2.
                    y -= entrance.dim.z/2.
                if entrance.exit.direction in ['bottom', 'top']:
                    x, y = dim.x/2., dim.y/2.
                    x -= entrance.dim.x/2.
                    y += entrance.dim.y/2.
            except: # in case it is root
                if entrance.direction in ['left', 'right']:
                    x, y = dim.y/2., dim.z/2.
                if entrance.direction in ['back', 'front']:
                    x, y = dim.x/2., dim.z/2.
                if entrance.direction in ['bottom', 'top']:
                    x, y = dim.x/2., dim.y/2.

            #print type(entrance.dim)
            offset = Point2(x,y)

        self.music_file = music
        
        if isinstance(entrance,MazeTunnel):
            entrance = entrance.exit

        origin = entrance.ExitLeftTop
        if entrance.direction == 'left':
            reference = 'LeftBackTop'
            origin -= Point3(0, offset.x, -offset.y)
        if entrance.direction == 'right':
            reference = 'RightFrontTop'
            origin -= Point3(0, -offset.x, -offset.y)
        if entrance.direction == 'back':
            reference = 'RightBackTop'
            origin -= Point3(-offset.x, 0, -offset.y)
        if entrance.direction == 'front':
            reference = 'LeftFrontTop'
            origin -= Point3(offset.x, 0, -offset.y)
        if entrance.direction == 'bottom':
            reference = 'LeftFrontBottom'
            origin -= Point3(offset.x, -offset.y, 0)
        if entrance.direction == 'top':
            reference = 'LeftBackTop'
            origin -= Point3(offset.x, offset.y, 0)

        # Possible references of the room: center and corners            # \/ Diametrically opposite to: \/
        references = [(0, ( 0., 0., 0.), 'xyz',    'center'          ),
                      (1, ( 1., 1., 1.), 'x+y+z+', 'LeftBackBottom'  ),  #       'RightFrontTop' 
                      (2, ( 1., 1.,-1.), 'x+y+z-', 'LeftBackTop'     ),  #       'RightFrontBottom'
                      (3, ( 1.,-1., 1.), 'x+y-z+', 'LeftFrontBottom' ),  #       'RightBackTop'
                      (4, ( 1.,-1.,-1.), 'x+y-z-', 'LeftFrontTop'    ),  #       'RightBackBottom'
                      (5, (-1., 1., 1.), 'x-y+z+', 'RightBackBottom' ),  #       'LeftFrontTop'
                      (6, (-1., 1.,-1.), 'x-y+z-', 'RightBackTop'    ),  #       'LeftFrontBottom'
                      (7, (-1.,-1., 1.), 'x-y-z+', 'RightFrontBottom'),  #       'LeftBackTop'
                      (8, (-1.,-1.,-1.), 'x-y-z-', 'RightFrontTop'   )]  #       'LeftBackBottom'

        # Finding index of the reference
        for item in references:
            if reference in item:
                reference = item[0]

#       if reference == 6: origin += Point3( offset.x, 0, offset.y )

        # Delta is half the distance from center
        D = Point3( dim.x/2., dim.y/2., dim.z/2.)
        d = Point3( references[reference][1] )
        delta = Point3(D.x*d.x, D.y*d.y, D.z*d.z)
        position  = Point3(origin + delta)
     
        # Drawing six sides:
        self.left   = MazeWall(position - Point3(dim.x/2.,0,0), Point2(dim.y,dim.z), 'left')
        self.right  = MazeWall(position + Point3(dim.x/2.,0,0), Point2(dim.y,dim.z), 'right')
        self.back   = MazeWall(position - Point3(0,dim.y/2.,0), Point2(dim.x,dim.z), 'back')
        self.front  = MazeWall(position + Point3(0,dim.y/2.,0), Point2(dim.x,dim.z), 'front')
        self.bottom = MazeWall(position - Point3(0,0,dim.z/2.), Point2(dim.x,dim.y), 'bottom')
        self.top    = MazeWall(position + Point3(0,0,dim.z/2.), Point2(dim.x,dim.y), 'top')

        # Define limits for the MazeRoom: since walls are parallel to axes, it's easy:
        self.x_minus = position.x - dim.x/2
        self.x_plus  = position.x + dim.x/2
        self.y_minus = position.y - dim.y/2
        self.y_plus  = position.y + dim.y/2
        self.z_minus = position.z - dim.z/2.
        self.z_plus  = position.z + dim.z/2.


        # Cuting window on the appropriate created wall, to coincide with the entrance.
        if entrance.direction == 'left': self.left.cutWindow((offset, Point2(offset+entrance.dim)))
        if entrance.direction == 'right': self.right.cutWindow((offset, Point2(offset+entrance.dim)))
        if entrance.direction == 'back': self.back.cutWindow((offset, Point2(offset+entrance.dim)))
        if entrance.direction == 'front': self.front.cutWindow((offset, Point2(offset+entrance.dim)))
        if entrance.direction == 'bottom': self.bottom.cutWindow((offset, Point2(offset+entrance.dim)))
        if entrance.direction == 'top': self.top.cutWindow((offset, Point2(offset+entrance.dim)))

        # Putting wallpapers on the walls:
        if kind == 'Puzzle':
            self.bottom.newTexture(Tile='textures/peace.gif', repeat=(4,4), bg_dim=(0,0))
            self.top.newTexture(Tile='textures/puzzle.gif', repeat=(4,4), bg_dim=(0,0))
            self.left.newTexture(Tile='textures/puzzle.gif', repeat=(4,4), bg_dim=(0,0))
            self.right.newTexture(Tile='textures/puzzle.gif', repeat=(4,4), bg_dim=(0,0))
            self.back.newTexture(Tile='textures/puzzle.gif', repeat=(4,4), bg_dim=(0,0))
            self.front.newTexture(Tile='textures/puzzle.gif', repeat=(4,4), bg_dim=(0,0))
        elif kind == 'Bricks':
            self.bottom.newTexture(Tile='textures/redplates.jpg', repeat=(4,4), bg_dim=(0,0))
            self.top.newTexture(Tile='textures/bricks.png', repeat=(4,4), bg_dim=(0,0))
            self.left.newTexture(Tile='textures/bricks.png', repeat=(4,4), bg_dim=(0,0))
            self.right.newTexture(Tile='textures/bricks.png', repeat=(4,4), bg_dim=(0,0))
            self.back.newTexture(Tile='textures/bricks.png', repeat=(4,4), bg_dim=(0,0))
            self.front.newTexture(Tile='textures/bricks.png', repeat=(4,4), bg_dim=(0,0))
        elif kind == 'Marvel':
            self.bottom.newTexture(Tile='textures/autumnleaves.jpg', repeat=(4,4), bg_dim=(0,0))
            self.top.newTexture(Tile='textures/redbubble.jpg', repeat=(4,4), bg_dim=(0,0))
            self.left.newTexture(Tile='textures/redbubble.jpg', repeat=(4,4), bg_dim=(0,0))
            self.right.newTexture(Tile='textures/redbubble.jpg', repeat=(4,4), bg_dim=(0,0))
            self.back.newTexture(Tile='textures/redbubble.jpg', repeat=(4,4), bg_dim=(0,0))
            self.front.newTexture(Tile='textures/redbubble.jpg', repeat=(4,4), bg_dim=(0,0))
        elif kind == 'Colorful':
            self.bottom.newTexture(Tile='textures/autumnleaves.jpg', repeat=(4,4), bg_dim=(0,0))
            self.top.newTexture(Tile='textures/turtlegirl.png', repeat=(4,4), bg_dim=(0,0))
            self.left.newTexture(Tile='textures/turtlegirl.png', repeat=(4,4), bg_dim=(0,0))
            self.right.newTexture(Tile='textures/turtlegirl.png', repeat=(4,4), bg_dim=(0,0))
            self.back.newTexture(Tile='textures/turtlegirl.png', repeat=(4,4), bg_dim=(0,0))
            self.front.newTexture(Tile='textures/turtlegirl.png', repeat=(4,4), bg_dim=(0,0))
            
            
            


    def __repr__(self):
        return str((self.x_minus, self.x_plus, self.y_minus, self.y_plus, self.z_minus, self.z_plus))

    def setTextures(self, Tile='default.png', repeat=(10,10), bg_dim=(0,0)):
        self.left.newTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)
        self.right.newTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)
        self.back.newTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)
        self.front.newTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)
        self.bottom.newTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)
        self.top.newTexture(Tile=Tile, repeat=repeat, bg_dim=bg_dim)

class StudyMaze(DirectObject):


    def __init__(self):

        # Cleanup the temporary directory before execution
        os.system('rm -rf %s*' % os.path.join(os.getcwd(), 'temp/') )

        # List of all the areas (MazeRooms, MazeTunnels) in the maze.
        self.mazeAreas = []
        self.margin = 2.0 # (Minimum distance to a wall.)

        # Saving the current state
        self.question_displayed = False

        # Load the 'empty room' model. 
        self.room = loader.loadModel("models/emptyroom")
        self.room.reparentTo(rootNode)

        # Load background music.
        self.music_file = ''
        self.active_video = ''
        self.sound_correct = ''
        self.sound_wrong = ''
        self.qsound = base.loader.loadSfx('sounds/qsound.ogg') # question appearance sound
        self.osound = base.loader.loadSfx('sounds/osound.ogg') # omit of question sound
        self.wsound = base.loader.loadSfx('sounds/wsound.ogg') # wrong answer sound
        self.csound = base.loader.loadSfx('sounds/csound.ogg') # correct answer sound

        # ========================================================
        # >>>>>>>>>>>>>>>>> MAZE WALLS IMAGES >>>>>>>>>>>>>>>>>>>>

        execfile('mazes/root.py')

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # ========================================================

        # Show framerate
        base.setFrameRateMeter(True)

        # Make the mouse invisible, turn off normal mouse controls
        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        # Set the current viewing target: facing y+, from (0,0,0)
        self.focus = Vec3(0,0,0)
        self.heading = 0
        self.pitch = 0
        self.mousex = 0
        self.mousey = 0
        self.last = 0
        self.mousebtn = [0,0,0]

        # Start the camera control task:
        taskMgr.add(self.controlCamera, "camera-task")
        self.accept("escape", sys.exit, [0])
        self.accept("mouse1", self.setMouseBtn, [0, 1])
        self.accept("mouse1-up", self.setMouseBtn, [0, 0])
        self.accept("mouse2", self.setMouseBtn, [1, 1])
        self.accept("mouse2-up", self.setMouseBtn, [1, 0])
        self.accept("mouse3", self.setMouseBtn, [2, 1])
        self.accept("mouse3-up", self.setMouseBtn, [2, 0])

    def setMouseBtn(self, btn, value):
        self.mousebtn[btn] = value

    def whichAreas(self, point3):
        results = []
        for area in self.mazeAreas:
            if area.x_minus < point3.x < area.x_plus and \
               area.y_minus < point3.y < area.y_plus and \
               area.z_minus < point3.z < area.z_plus:
                results.append(area)
        
        return results

    def display_question(self, source=('problem1.png', 'answer1')):
        self.qsound.play()
        cmi = CardMaker("Problem")
        cmi.setFrame(-0.9,0.2,-0.9,0.9)
        self.card = render2d.attachNewNode(cmi.generate())
        tex = loader.loadTexture( source[0] )
        self.answer = source[1]
        self.card.setTexture(tex) 

    def hide_question(self):
        try:
            if self.card:
                self.card.removeNode()
                self.question_displayed = False
            if self.q:
                self.osound.play()
                self.q.destroy()
        except:
            pass

 
    def controlCamera(self, task):
        # figure out how much the mouse has moved (in pixels)
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()

        # clearly: necessary for mouse movement
        if base.win.movePointer(0, 100, 100):
            self.heading = self.heading - (x - 100) * 0.2
            self.pitch = self.pitch - (y - 100) * 0.2

        # limits up/down movement of the camera
        if (self.pitch < -90): self.pitch = -90
        if (self.pitch >  90): self.pitch =  90

        # clearly: necessary for direction movement
        base.camera.setHpr(self.heading,self.pitch,0)
        dir = base.camera.getMat().getRow3(1)

        # clearly: necessary for forth/back movement
        elapsed = task.time - self.last
        if (self.last == 0): elapsed = 0
        if (self.mousebtn[0]):
            self.focus = self.focus + dir * elapsed*30
        if (self.mousebtn[1]) or (self.mousebtn[2]):
            self.focus = self.focus - dir * elapsed*30
        base.camera.setPos(self.focus - (dir*5))

        # >>>>>>>>>>>>>>>>> MAZE AREAS' LIMITS >>>>>>>>>>>>>>>>>>>


        # Get current camera position
        point = Point3(base.camera.getX(), base.camera.getY(),  base.camera.getZ())
        #print point

        # Check which area we are in, assuming single-area-presence for now:
        # // Later we will set priorities, in the cases of overlapping limits of
        #    a MazeRoom and limits of a MazeTunnel. //


        # Function that checks for answer, used to update tunnel limits.
        def setText(textEntered):
            if textEntered == self.tunnel.answer: # i.e., if answer is correct:
                self.csound.play()
                try:
                    self.tunnel.update_limits()
                    self.hide_question()
                except: 
                    pass
            else:
                self.wsound.play()
            textObject.setText(textEntered)

        # Function that clears the answer field.
        def clearText():
            self.q.enterText('')


        # Set the limits of that room:
        try:
            AL = self.whichAreas(point)

            # Logically, if we are in more than 1 area, we should let the movement along the axis of the tunnel.
            # Determining the axis:
            if len(AL) > 1:
                pass
            elif len(AL) == 1:
                for item in AL:
                    if isinstance(item, MazeTunnel):
                        free = item.which
                        if (item.active_x_minus < point.x < item.active_x_plus) and \
                           (item.active_y_minus < point.y < item.active_y_plus) and \
                            (item.active_z_minus < point.z < item.active_z_plus):

                            if not self.question_displayed:

                                # Display question
                                self.tunnel = item
                                self.q = DirectEntry(width=12, text = "" ,scale=.05, pos=(-0.4, 0, -0.7), \
                                         command=setText, initialText="Step away, and type answer!", numLines = 3,focus=1,focusInCommand=clearText)
                                self.display_question( item.questions[item.current_problem-1] )
                                self.question_displayed = True

                        else:                               # Either not in active zone anymore
                            self.hide_question()
                    else:                                   # Or not in MazeTunnel anymore.
                        self.hide_question()

                        # Change music:

                        if self.music_file == '':
                            self.music_file = item.music_file
                            self.music = base.loader.loadSfx(self.music_file)
                            self.music.play()
                            self.music.setVolume(0.5)

                        if item.music_file != self.music_file:
                            self.music.stop()
                            self.music_file = item.music_file
                            if os.path.isfile(self.music_file):
                                self.music = base.loader.loadSfx(item.music_file)
                                self.music.play()
                                self.music.setVolume(0.5)

                        # Check if we are not in any Poster's activation area,
                        # and activate the poster, in which's are we are in.
                        WallList = [item.left, item.right, item.back, item.front, item.bottom, item.top]
                        for wall in WallList:
                            if len(wall.posters):
                                for poster in wall.posters.values():
                                    if poster.document.split('.')[-1] in [ 'avi', 'mp4' ]:
                                        if (poster.x_minus < point.x < poster.x_plus) and \
                                           (poster.y_minus < point.y < poster.y_plus) and \
                                           (poster.z_minus < point.z < poster.z_plus):
                                            if self.active_video == '':
                                                self.active_video = poster.media
                                            if id(self.active_video) != id(poster.media):
                                                self.active_video.stop()
                                                self.active_video = poster.media
                                            if self.active_video.getTime() > 0.0:
                                                self.active_video.setTime(0.0)
                                            self.active_video.play()

                free = Point3(0,0,0)
                AL = AL[0]

            if self.music_file != '':
                self.accept("z", self.music.stop)        # z - for 'sleep zzz'
            if self.active_video != '':                        
                self.accept("x", self.active_video.stop) # x - for 'cross-out'
                self.accept("c", self.active_video.play) # c - for 'continue'

            left_lim   = AL.x_minus + self.margin
            right_lim  = AL.x_plus - self.margin
            back_lim   = AL.y_minus + self.margin
            front_lim  = AL.y_plus - self.margin
            bottom_lim = AL.z_minus + self.margin
            top_lim    = AL.z_plus - self.margin
            if ( point.x < left_lim ) and not free.x:   base.camera.setX(left_lim )
            if ( point.x > right_lim ) and not free.x:  base.camera.setX(right_lim )
            if ( point.y < back_lim ) and not free.y:   base.camera.setY(back_lim )
            if ( point.y > front_lim ) and not free.y:  base.camera.setY(front_lim )
            if ( point.z < bottom_lim ) and not free.z: base.camera.setZ(bottom_lim )
            if ( point.z > top_lim ) and not free.z:    base.camera.setZ(top_lim )
        except:
            pass

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        self.focus = base.camera.getPos() + (dir*5)
        self.last = task.time
        return Task.cont


Maze = StudyMaze()

rootNode.clearModelNodes()
rootNode.flattenStrong() 

# Some text for entry field.
bk_text = ""
textObject = OnscreenText(text = bk_text, pos = (0.95,-0.95), scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=1)

run()

