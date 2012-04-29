# Wall module for VPyMaze by Kile Deal

from visual import box, color, materials

class Wall(box):
    def __init__(self, color=color.white, material=materials.wood,
                 length=1, width=10, height=10, visible=True,
                 pos=(0,0,0)):

        box.__init__(self) # super constructor

        self.color    = color
        self.material = material
        self.length   = length
        self.width    = width
        self.height   = height
        self.visible  = visible
        self.pos      = pos

    def knockdown(self):
        self.visible = False