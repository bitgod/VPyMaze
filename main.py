# VPyMaze by Kile Deal
# CSCI 3232 Final Project

from visual import display
from maze import *
from time import sleep, time
from random import randint, random
from settings import *

# Re-highlight path forwards and backwards until user closes window
def victory(maze):
    colors = [color.red, color.blue, color.magenta, color.blue, color.cyan,
              color. orange, color.yellow, color.green, color.black, color.white]
    lastColor = None
    reverse = False

    while True:
        newColor = randselect(colors)
        if newColor == lastColor:
            newColor = colors[colors.index(newColor)-1]
        lastColor = newColor
        if reverse:
            for each in reversed(maze.solvePath):
                rate(50)
                each.color = newColor
            reverse = False
        else:
            for each in maze.solvePath:
                rate(50)
                each.color = newColor
            reverse = True

def main():
    scene = display(title=WINDOW_TITLE, width=WINDOW_WIDTH,
                    height=WINDOW_HEIGHT)

    if RANDOM_SIZE:
        maze = Maze(xlen=randint(MIN_SIZE, MAX_SIZE), ylen=randint(MIN_SIZE, MAX_SIZE))
    else:
        maze = Maze(xlen=FIXED_X, ylen=FIXED_Y)

    print "SIZE: {X}x{Y}".format(X = maze.xlen, Y = maze.ylen)
    print "DIFFICULTY: ",int((maze.xlen * maze.ylen)/100.0)

    if ANIMATE_GENERATION:
        maze.animateGen = True

    if ANIMATE_AUTO_SOLVE:
        maze.animateAutoSolve = True

    if SHOW_COORDINATES:
        maze.showCoordinates = True

    maze.makefloor()
    maze.makegrid()
    maze.setcorners()
    maze.setCellAssociations()

    maze.generate()
    maze.setStartandFinish()

    if SHOW_PIVOTS:
        # Test: Highlight all pivot points ~ This is for debugging purposes
        for row in maze.cells:
            for c in row:
                if c.pivot:
                    c.color = (1, 1, 0)
                    #c.highlight()
                    fstring = "Pivot: ({COL},{ROW}) - "
                    print fstring.format(ROW=c.mazePos[1], COL=c.mazePos[0]),
                    for path in c.openPaths:
                        print "({COL},{ROW})".format(ROW=path.mazePos[1], COL=path.mazePos[0]),
                    print

    if MANUAL_SOLVE:
        print "Use the arrow keys to navigate the maze."
        startTime = time()
        maze.solveManually(scene)
        finishTime = time()
        print "Completed in",int(finishTime-startTime),"seconds"
        victory(maze)
    else:
        countdown = label(text="",align='center', depth=5,
                         color=color.red, height=maze.floor.height,
                         pos=(0, 0, 10))
        for count in reversed(range(3)):
            countdown.text=str(count+1)
            sleep(1)
        countdown.visible = False
        print "Solving..."
        startTime = time()
        maze.solve()
        finishTime = time()
        print "Completed in",int(finishTime-startTime),"seconds"
        victory(maze)

if __name__ == "__main__":
    main()
