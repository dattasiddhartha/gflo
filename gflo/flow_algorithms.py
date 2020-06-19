import pandas as pd
import matplotlib.pyplot as plt
import itertools

import networkx as nx 
from networkx.algorithms.flow import ford_fulkerson
from networkx.algorithms.flow import shortest_augmenting_path


def CompleteGraph(node_values_1, node_values_2, weight=1, layout = 'circular'):
    G = nx.Graph() 
    for i in range(len(node_values_1)):
        G.add_edge(node_values_1[i],node_values_2[i], weight=weight, color='black')

    from matplotlib.pyplot import figure
    figure(num=None, figsize=(25, 25), dpi=120, facecolor='w', edgecolor='k')

    if layout == 'circular':
        pos = nx.circular_layout(G)
    if layout == 'spring':
        pos = nx.spring_layout(G, k=0.15,iterations=50)

    edges = G.edges()
    colors = [G[u][v]['color'] for u,v in edges]
    weights = [G[u][v]['weight'] for u,v in edges]

    nx.draw(G, pos=pos, with_labels=True, node_size = 10, font_size=5, edges=edges, edge_color=colors)
    plt.show()
    
    
def FlowGraph(node_values_1, node_values_2, weight=1, 
              flow_nodes = [], color_nodes = [], node_colors = [], edge_colors = []):
    
    # node_values_1 : list of node labels
    # node_values_2 : list of node labels
    # weight : weight of the edge between each pair in (node_values_1, node_values_2) 
    #          -- should be the *flow* in value between node1 and node2
    # flow_nodes : list of nodes that indicate that they are the "flow nodes" (nodes that receive flow in values from other nodes)
    # color_nodes : list of nodes that should be colored
    # node_colors : colors for respective nodes
    # edge_colors : colors of respective edges between nodes, if the node is a flow node

    
    # Potential improvements:
    # arguments: label text size, threshold requirements for flow, top N nodes by flow value to be plotted
    
    G = nx.Graph() 
    
    for j in range(len(flow_nodes)):
        for i in range(len(node_values_1)):
            if node_values_1[i] == flow_nodes[j] or node_values_2[i] in flow_nodes[j]:
                if len(edge_colors) == 0:
                    G.add_edge(node_values_1[i], node_values_2[i], weight=weight, color='black')
                else:
                    if node_values_1[i] in color_nodes or node_values_2[i] in color_nodes:
                        G.add_edge(node_values_1[i], node_values_2[i], weight=weight, color=edge_colors[j])

    from matplotlib.pyplot import figure
    figure(num=None, figsize=(25, 25), dpi=120, facecolor='w', edgecolor='k')

    color_map = []
    for node in G:
        color = 'grey'
        for j in range(len(flow_nodes)):
            if flow_nodes[j] in color_nodes:
                if flow_nodes[j] in node:
                    color = node_colors[j]
        color_map.append(color)

    pos = nx.circular_layout(G)

    edges = G.edges()
    colors = [G[u][v]['color'] for u,v in edges]
    weights = [G[u][v]['weight'] for u,v in edges]

    nx.draw(G, pos=pos, with_labels=True, node_size = 1000, font_size=30, edges=edges, edge_color=colors, node_color = color_map)
    plt.show()
    

def FordFulkerson(node_values_1, node_values_2, 
                  source_node, target_node, 
                  capacity='capacity', weight=1):
    
    # deprecated, issues with infinite capacity
    
    G = nx.DiGraph() # nx.Graph() 
    
    for i in range(len(node_values_1)):
        G.add_edge(node_values_1[i],node_values_2[i], capacity=weight, color='black')

    from matplotlib.pyplot import figure
    figure(num=None, figsize=(25, 25), dpi=120, facecolor='w', edgecolor='k')

    pos = nx.circular_layout(G)
    edges = G.edges()
    colors = [G[u][v]['color'] for u,v in edges]
    weights = [G[u][v]['capacity'] for u,v in edges]

#     R = ford_fulkerson(G, source_node, target_node, capacity)

    flow_value, flow_dict = nx.maximum_flow(G, source_node, target_node, capacity, flow_func=ford_fulkerson)
#     flow_value, flow_dict = nx.maximum_flow(G, source_node, target_node, capacity, flow_func=shortest_augmenting_path)
    
    

    