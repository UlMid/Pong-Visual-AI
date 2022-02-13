import pygame 
from data import Database, decodeCommand

class Node:
    def __init__(self, id, x, y, type, color, label = "", index=0):
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.label = label
        self.index = index

    def draw_node(self, best):
        colorScheme = self.getNodeColors(best)

        pygame.draw.circle(best.win, colorScheme[0], (self.x,self.y), Database.NODE_RADIUS)
        pygame.draw.circle(best.win, colorScheme[1], (self.x,self.y), Database.NODE_RADIUS-2)

        #draw labels
        if self.type != Database.MIDDLE:
            text = Database.NODE_FONT.render(self.label, 1, Database.GRAY)
            best.win.blit(text, 
                        (self.x + (self.type-1) * ((text.get_width() if not self.type else 0) + Database.NODE_RADIUS + 5), 
                        self.y - text.get_height()/2))

    def getNodeColors(self, best):
        if self.type == Database.INPUT:
            ratio = best.bestInputs[self.index]
        elif self.type == Database.OUTPUT:
            ratio = 1 if decodeCommand(best.bestCommands, self.index) else 0 
        else:
            ratio = 0

        col = [[0,0,0], [0,0,0]]
        for i in range(3):
            col[0][i] = int(ratio * (self.color[1][i]-self.color[3][i]) + self.color[3][i])
            col[1][i] = int(ratio * (self.color[0][i]-self.color[2][i]) + self.color[2][i])
        return col
        
class Connection:
    def __init__(self, input, output, wt):
        self.input = input
        self.output = output
        self.wt = wt

    def drawConnection(self, best):
        color = Database.GREEN if self.wt >= 0 else Database.RED
        width = int(abs(self.wt * Database.CONNECTION_WIDTH))
        pygame.draw.line(best.win, 
                        color, 
                        (self.input.x + Database.NODE_RADIUS, self.input.y), 
                        (self.output.x - Database.NODE_RADIUS, self.output.y), 
                        width)
