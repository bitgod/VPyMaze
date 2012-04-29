# Maze module for VPyMaze by Kile Deal

from wall import *
from cell import *
from visual import rate, scene
from visual import text as VText
from random import choice as randselect

class Maze():
    # Start and Finish must be Cells
    # xlen and ylen describe the dimensions of the maze in terms
        # of cells which are 10x10
    def __init__(self, start = None, finish = None,
                 xlen=10, ylen=10, animateGen=False,
                 animateAutoSolve=False, showCoordinates=False):

        self.start  = start  # The cell where the maze begins
        self.finish = finish # The cell where the maze ends
        self.xlen   = xlen
        self.ylen   = ylen
        self.cells  = []     # Will be 2-dimensional upon call to makegrid()
        self.corners = []    # Corners of the grid. Start and Finish will
                                 # will be taken from this list
        self.solvePath = []

        self.animateGen = animateGen
        self.animateAutoSolve = animateAutoSolve
        self.showCoordinates = showCoordinates

    # Create the back of the maze
    def makefloor(self):
        self.floor = Wall(length=self.xlen*10,
                          height=self.ylen*10,
                          width=10, pos=(0,0,-10))

    # Generate the grid for the maze
    def makegrid(self):
        xref = self.xlen*10
        yref = self.ylen*10

        y = 0

        # Generate cells and walls from top-left corner down
        for row in range(self.ylen):
            self.cells.append([]) # add new row
            for col in range(self.xlen):
                newCell = Cell( pos=(-(xref/2.0)+5, (yref/2.0)-5, 0),
                                mazePos=[col,row] )

                newCell.northWall = Wall( pos=(newCell.x, newCell.y+4.5, 0),
                                          length=10, width=10, height=1)
                newCell.southWall = Wall( pos=(newCell.x, newCell.y-4.5, 0),
                                          length=10, width=10, height=1)
                newCell.westWall = Wall( pos=(newCell.x-4.5, newCell.y, 0) )
                newCell.eastWall = Wall( pos=(newCell.x+4.5, newCell.y, 0) )

                self.cells[y].append(newCell) # add cell (column) to current row

                xref-=20

            yref -= 20
            xref = self.xlen*10
            y += 1

        # Show Coordinate Axes
        if self.showCoordinates:
            # Top Row
            for i in range(len(self.cells[0])):
                VText(text=str(i),align='center', depth=1,
                         color=color.white, height=5,width=5,
                         pos=(self.cells[0][i].x,self.cells[0][0].y+7.5))
            # Side Column
            for i in range(len(self.cells)):
                VText(text=str(i),align='center', depth=1,
                         color=color.white, height=5,width=5,
                         pos=(self.cells[0][0].x-10,self.cells[i][0].y-2))

    def setcorners(self):
        # Upper left corner
        self.cells[0][0].iscorner = True
        self.corners.append(self.cells[0][0])

        # Upper right corner
        self.cells[0][self.xlen-1].iscorner = True
        self.corners.append(self.cells[0][self.xlen-1])

        # Lower left corner
        self.cells[self.ylen-1][0].iscorner = True
        self.corners.append(self.cells[self.ylen-1][0])

        # Lower right corner
        self.cells[self.ylen-1][self.xlen-1].iscorner = True
        self.corners.append(self.cells[self.ylen-1][self.xlen-1])

    def setCellAssociations(self):
        for y in range(self.ylen):
            for x in range(self.xlen):
                current = self.cells[y][x]

                # Get North Cell
                if y == 0: # if currently iterating top row
                    n = None
                else:
                    n = self.cells[y-1][x]

                # Get South Cell
                if y == self.ylen-1: # if currently iterating bottom row
                    s = None
                else:
                    s = self.cells[y+1][x]

                # Get West Cell
                if x == 0:
                    w = None
                else:
                    w = self.cells[y][x-1]

                # Get East Cell
                if x == self.xlen-1:
                    e = None
                else:
                    e = self.cells[y][x+1]

                # Set Cell Associations

                current.northCell = n
                current.southCell = s
                current.westCell  = w
                current.eastCell  = e

    def setStartandFinish(self):
        self.start = randselect(self.corners)
        if self.corners.index(self.start) == 0: self.finish = self.corners[3]
        if self.corners.index(self.start) == 1: self.finish = self.corners[2]
        if self.corners.index(self.start) == 2: self.finish = self.corners[1]
        if self.corners.index(self.start) == 3: self.finish = self.corners[0]

        self.start.color = color.green
        self.finish.color = color.blue
        self.start.highlight()
        self.finish.highlight()

    # Necessary for generate() method
    # Chooses a random direction to move in
        # Returns -1 if no direction is available
    def selectNext(self, possibilities):
        dirs = []
        for i in possibilities: dirs.append(i)

        while len(dirs) != 0:
            select = randselect(dirs)
            if select == None:
                del dirs[dirs.index(select)]
            else:
                if not select.visited:
                    return select
                else:
                    del dirs[dirs.index(select)]
        return -1

    # Generate the maze using DFS algorithm
    def generate(self):
        unvisited = []
        history = []

        for row in self.cells:
            for cell in row:
                unvisited.append(cell)

        current = randselect(unvisited)
        current.visited = True

        speed = 0.075 * len(unvisited)
        while len(unvisited) > 0:
            history.append(current)
            if self.animateGen: # So we can watch the generation
                rate(speed)
            nextCell = None

            backbuffer = -1
            while nextCell == None :
                directions = [ current.northCell,
                           current.southCell,
                           current.westCell,
                           current.eastCell ]
                nextCell = self.selectNext(directions)
                if nextCell == -1:
                    if backbuffer == -len(history):
                        history[-2].unhighlight()
                        # Set all cells back to visited = False
                        # Also find all pivot points of the maze
                        for row in self.cells:
                            for c in row:
                                c.visited = False
                                if len(c.openPaths) > 2:
                                    c.pivot = True
                        # Exit Generation
                        return
                    current = history[backbuffer]
                    unvisited.append(current)
                    backbuffer -= 1
                    nextCell = None

            # Going North
            if nextCell == current.northCell:
                current.northWall.knockdown()
                current.openPath("North")
                current.northCell.southWall.knockdown()
                current.northCell.openPath("South")
                del unvisited[unvisited.index(current)]
                current = current.northCell
            # Going South
            if nextCell == current.southCell:
                current.southWall.knockdown()
                current.openPath("South")
                current.southCell.northWall.knockdown()
                current.southCell.openPath("North")
                del unvisited[unvisited.index(current)]
                current = current.southCell
            # Going West
            if nextCell == current.westCell:
                current.westWall.knockdown()
                current.openPath("West")
                current.westCell.eastWall.knockdown()
                current.westCell.openPath("East")
                del unvisited[unvisited.index(current)]
                current = current.westCell
            # Going East
            if nextCell == current.eastCell:
                current.eastWall.knockdown()
                current.openPath("East")
                current.eastCell.westWall.knockdown()
                current.eastCell.openPath("West")
                del unvisited[unvisited.index(current)]
                current = current.eastCell

            current.visited = True
            history[-1].highlight()
            if len(history) >= 2: history[-2].unhighlight()


    # Solve the maze automatically
    # Uses essentially the same algorithm used to generate the maze
    def solve(self):
        path = []
        current = self.start
        path.append(current)

        while current != self.finish:
            if self.animateAutoSolve:
                rate(15)
            if self.finish in current.openPaths:
                current = self.finish
                path.append(current)
            else:
                nextCell = self.selectNext(current.openPaths)
                if nextCell == -1:
                    # Backtrack through the path until a pivot is found
                    for cell in path:
                        if self.animateAutoSolve:
                            rate(15)
                        if current.pivot:
                            if self.selectNext(current.openPaths) != -1:
                                break
                            else:
                                # Delete the most recent cell from path
                                # Then set current to the last cell in path
                                path[-1].unhighlight()
                                del path[-1]
                                current = path[-1]
                        else:
                            path[-1].unhighlight()
                            del path[-1]
                            current = path[-1]
                else:
                    current = nextCell
                    current.visited = True
                    path.append(current)

            for each in path:
                each.highlight()

            if current == self.finish:
                self.solvePath = path
                print "-------------SOLVED!-------------"
                VText(text='SOLVED!',align='center', depth=5,
                     color=color.white, height=20, width=20, pos=(0,0,7.5))

    # Gives user the ability to navigate the maze manually
    def solveManually(self, scene):
        print "Begin!"
        current = self.start
        current.visited = True
        history = []
        history.append(current)
        while current != self.finish:
            key = scene.kb.getkey()
            # First check if the direction that the user is trying to go
            # is blocked by a wall
            if key == "up" and not current.northOpen:
                print "The North path is blocked."
            elif key == "down" and not current.southOpen:
                print "The South path is blocked."
            elif key == "left" and not current.westOpen:
                print "The West path is blocked."
            elif key == "right" and not current.eastOpen:
                print "The East path is blocked."
            else:
                # Change current to the cell in corresponding direction
                if key == "up":
                    current = current.northCell
                    if current not in history:
                        history.append(current)
                    elif current == history[-2]:
                        history[-1].unhighlight()
                        del history[-1]
                elif key == "down":
                    current = current.southCell
                    if current not in history:
                        history.append(current)
                    elif current == history[-2]:
                        history[-1].unhighlight()
                        del history[-1]
                elif key == "left":
                    current = current.westCell
                    if current not in history:
                        history.append(current)
                    elif current == history[-2]:
                        history[-1].unhighlight()
                        del history[-1]
                elif key == "right":
                    current = current.eastCell
                    if current not in history:
                        history.append(current)
                    elif current == history[-2]:
                        history[-1].unhighlight()
                        del history[-1]

            if current == self.finish:
                self.solvePath = history
                print "-------------SOLVED!-------------"
                VText(text='SOLVED!',align='center', depth=5,
                     color=color.white, height=20, width=20, pos=(0,0,7.5))

            # Highlight current solve path
            for each in history:
                each.highlight()
