import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random as rd


class Model:
    '''
    This class generate a grid model for evacuation planning
    '''
    def __init__(self):
        self.G = nx.DiGraph()
        self.edges = []
        self.generated = False
        self.list_thredhold = []
        self.scenarios = []
        self.solutions = []
    
    #This function generate the grid for the model
    def generate_grid(self):
        #This function generate edges pair for the grid
        def generate_adjacent_pairs(rows, cols):
            pairs = []
            for row in range(1, rows + 1):
                for col in range(1, cols + 1):
                    current_node = col + (row - 1) * cols
                    right_node = col + 1 + (row - 1) * cols
                    bottom_node = col + row * cols
                    if col == cols:
                        right_node = 0
                    if row == rows:
                        bottom_node = 0
                    if right_node != 0: 
                        pairs.append((current_node, right_node))
                    if bottom_node != 0:
                        pairs.append((current_node, bottom_node))
            return pairs
        
        #Initialize capacity and travel time in the grid
        pairs = generate_adjacent_pairs(5, 10)
        for i in range(len(pairs)):
            self.G.add_edge(*pairs[i], time_travel = rd.randrange(3,9), capacity = rd.randrange(10, 20))
        #Set demand in each node
        nodes_demand = {}
        nodes_demand[1] = 600
        nodes_demand[50] = -600
        for i in range(2, 50):
            nodes_demand[i] = 0
        nx.set_node_attributes(self.G, nodes_demand, name='demand')
        self.generated = True
        self.edges = pairs
    
    def drawing(self):
        if not self.generated:
            self.generate_grid()
        based_node_pos = {1 : (1, 5), 11 : (1, 4), 21 : (1, 3), 31 : (1, 2), 41 : (1, 1)}
        node_pos = dict(based_node_pos)
        for i in range(1, 10):
            for key in based_node_pos:
                x, y = based_node_pos[key]
                node_pos[key + i] = tuple((x + i, y))
        
        label1 = nx.get_edge_attributes(self.G, 'capacity')
        nx.draw(self.G, node_pos, with_labels = True, node_color = 'green', font_color= 'whitesmoke', font_size = 10)
        nx.draw_networkx_edge_labels(self.G, node_pos, edge_labels=label1)
        plt.show()

    def generate_scenario(self, num_scenario = 10):
        #This function generate 10 random scenario for the 2nd stage
        for i in range(num_scenario):
            random_scenario = np.random.randint(10, 20, size=85)
            self.scenarios.append(random_scenario)
        return
    
    def change_to_scenario(self, idx : int):
        if len(self.scenarios) == 0:
            self.generate_scenario()
        elif not self.generated:
            self.generate_grid()
        chosen_scenario = self.scenarios[idx]
        dictionary = dict({self.edges[i] : dict({"capacity" : chosen_scenario[i]}) for i in range(len(self.edges))})
        nx.set_edge_attributes(self.G, dictionary)

x = Model()
x.change_to_scenario(4)
x.drawing()