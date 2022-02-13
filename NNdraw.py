from data import Database
from node import Node, Connection

class NN:
    def __init__(self, config, genome, pos):
        self.input_nodes = []
        self.output_nodes = []
        self.nodes = []
        self.genome = genome
        self.pos = (int(pos[0]+ Database.NODE_RADIUS), int(pos[1]))
        middle_nodes = [n for n in genome.nodes.keys()]
        nodeIdList = []

        #nodes
        h = (Database.INPUT_NEURONS-1)*(Database.NODE_RADIUS*2 + Database.NODE_SPACING)
        for i, input in enumerate(config.genome_config.input_keys):
            n = Node(input, 
                    pos[0], 
                    pos[1]+int(-h/2 + i*(Database.NODE_RADIUS*2 + Database.NODE_SPACING)), 
                    Database.INPUT, 
                    [Database.GREEN_PALE, Database.GREEN, Database.DARK_GREEN_PALE, Database.DARK_GREEN], 
                    Database.INPUT_NAMES[i], 
                    i)

            self.nodes.append(n)
            nodeIdList.append(input)

        h = (Database.OUTPUT_NEURONS-1)*( Database.NODE_RADIUS*2 + Database.NODE_SPACING)
        for i,out in enumerate(config.genome_config.output_keys):
            n = Node(out+Database.INPUT_NEURONS, 
            pos[0] + 2*(Database.LAYER_SPACING+2* Database.NODE_RADIUS), 
            pos[1]+int(-h/2 + i*( Database.NODE_RADIUS*2 + Database.NODE_SPACING)), 
            Database.OUTPUT, 
            [Database.RED_PALE, Database.RED, Database.DARK_RED_PALE, Database.DARK_RED], 
            Database.OUTPUT_NAMES[i], 
            i)

            self.nodes.append(n)
            middle_nodes.remove(out)
            nodeIdList.append(out)

        h = (len(middle_nodes)-1)*( Database.NODE_RADIUS*2 + Database.NODE_SPACING)
        for i, m in enumerate(middle_nodes):
            n = Node(m, 
                    self.pos[0] + (Database.LAYER_SPACING+2* Database.NODE_RADIUS), 
                    self.pos[1]+int(-h/2 + i*( Database.NODE_RADIUS*2 + Database.NODE_SPACING)), 
                    Database.MIDDLE, 
                    [Database.BLUE_PALE, Database.DARK_BLUE, Database.BLUE_PALE, Database.DARK_BLUE])
            self.nodes.append(n)
            nodeIdList.append(m)

        #connections
        self.connections = []
        for c in genome.connections.values():
            if c.enabled:
                input, output = c.key
                self.connections.append(Connection(self.nodes[nodeIdList.index(input)],
                                                self.nodes[nodeIdList.index(output)], 
                                                c.weight))

    def draw(self, screen):
        for c in self.connections:
            c.drawConnection(screen)
        for node in self.nodes:
            node.draw_node(screen)