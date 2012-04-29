# Cell module for VPyMaze by Kile Deal

from visual import box, color

class Cell(box):
    def __init__(self, color=color.red, opacity=0,
                 length=9, width=9, height=9,
                 pos=(0,0,0), northWall=None, southWall=None,
                 westWall=None, eastWall=None, northCell=None,
                 southCell=None, westCell=None, eastCell=None,
                 iscorner=False, mazePos = []):

        box.__init__(self) # super constructor

        self.color     = color
        self.opacity   = opacity
        self.length    = length
        self.width     = width
        self.height    = height
        self.pos       = pos

        self.mazePos = mazePos

        # The Walls of the cell (up, down, left, right)
        self.northWall = northWall
        self.southWall = southWall
        self.westWall  = westWall
        self.eastWall  = eastWall

		# Open Paths
        self.northOpen = False
        self.southOpen = False
        self.westOpen  = False
        self.eastOpen  = False

        self.northCell = northCell # Pointer to cell directly above
        self.southCell = southCell # Pointer to cell directly below
        self.westCell  = westCell  # Pointer to cell directly left
        self.eastCell  = eastCell  # Pointer to cell directly right

        self.openPaths = []

        self.iscorner  = iscorner

        self.visited = False
        self.pivot = False

    def openPath(self, direction):
        if direction == "North":
            self.northOpen = True
            self.openPaths.append(self.northCell)
        elif direction == "South":
            self.southOpen = True
            self.openPaths.append(self.southCell)
        elif direction == "West":
            self.westOpen = True
            self.openPaths.append(self.westCell)
        elif direction == "East":
            self.eastOpen = True
            self.openPaths.append(self.eastCell)
        else:
            raise "Invalid <direction> specified"

    def highlight(self):
        self.opacity=0.5

    def unhighlight(self):
        self.opacity=0