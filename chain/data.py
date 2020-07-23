import pandas as pd
import numpy as np

class Node():
    def __init__(self,NodeID,type,A,longitude,latitude,D,fx_val:np.ndarray):
        self.NodeID = int(NodeID)
        self.type =str(type)
        self.A = float(A)
        self.longitude = float(longitude) if longitude!=' ' else None
        self.latitude = float(latitude) if latitude!=' ' else None
        self.D = int(D)
        self.fx_val = [float(val) if val != ' ' else None for val in fx_val]

    def __repr__(self):
        return '(ID:{} type:{} A:{} longitude:{} latitude:{} D:{} fx_val:{})'.format(self.NodeID,self.type,self.A,self.longitude,self.latitude,self.D,self.fx_val)


class Edge():
    def __init__(self,NodeA,NodeB,A,NE):
        self.NodeA = int(NodeA)
        self.NodeB = int(NodeB)
        self.A =float(A)
        self.NE = int(NE)

    def __repr__(self):
        return '(NodeA:{} NodeB:{} A:{} NE:{})'.format(self.NodeA,self.NodeB,self.A,self.NE)


class CityData():
    def __init__(self,attributes_file:str,topology_file:str):
        if attributes_file.endswith('csv'):
            nodes_info = pd.read_csv(attributes_file).values
        elif attributes_file.endswith('xlsx'):
            nodes_info = pd.read_excel(attributes_file).values
        else:
            raise ValueError('attributes_file must be csv or xlsx')
        self.nodes = {}
        for node in nodes_info:
            NodeID, type, A, longitude, latitude, D, fx_val = int(node[0]),node[1],node[2],node[3],node[4],node[5],node[6:]
            self.nodes[NodeID] = Node(NodeID, type, A, longitude, latitude, D, fx_val)
        topology_info = pd.read_csv(topology_file).values
        self.topology = {}
        for k in self.nodes.keys():
            self.topology[k]= {}

        self.max_NE=0
        for topology in topology_info:
            NodeA,NodeB,A,NE = int(topology[0]),int(topology[4]),float(topology[8]),int(topology[9])
            self.topology[NodeA][NodeB]=Edge(NodeA,NodeB,A,NE)
            self.topology[NodeB][NodeA]=Edge(NodeB,NodeA,A,NE)
            self.max_NE = self.max_NE if self.max_NE>NE else NE

        self.g_ids = []
        self.h_ids = []
        self.j_ids = []
        for node in self.nodes.values():
            if node.type == 'G':
                self.g_ids.append(node.NodeID)
            if node.type == 'H':
                self.h_ids.append(node.NodeID)
            if node.type == 'J':
                self.j_ids.append(node.NodeID)
    '''
    param:
        nodeA:id of NodeA
        nodeB:id of NodeB
    return:
        None if  longitude or latitude is None,else distance (meters)
    '''
    def distance(self,nodeA:int,nodeB:int)->float:
        raise NotImplementedError('there is some problem with latitude')
        # nodeA,nodeB = self.nodes[nodeA],self.nodes[nodeB]
        # if nodeA.longitude is None or nodeA.latitude is None or nodeB.longitude is None or nodeB.latitude is None :
        #     return None
        # else:
        #     return np.arccos(np.sin(nodeA.latitude/180*np.pi)*np.sin(nodeB.latitude/180*np.pi)+np.cos(nodeA.latitude/180*np.pi)*np.cos(nodeB.latitude/180*np.pi)*np.cos(nodeA.longitude/180*np.pi -nodeB.longitude/180*np.pi))*6371004

    ''' 
    return:
        list[int]id of all nodes
    '''
    def get_ids(self)->list:
        return list(self.nodes.keys())
    ''' 
    :parameter:
        type,str,['G','H','J']
    return:
        list[int],id of all nodes with specified type 
    '''
    def get_ids_by_type(self,type:str)->list:
        if type == 'G':
            return self.g_ids
        if type == 'H':
            return self.h_ids
        if type == 'J':
            return self.j_ids
        raise ValueError('type must be in G,H,J not {}'.format(type))

    ''' 
    param:
        nodeID:id of Node
    return:
        Node,info of the node
        None,if nodeID not in attributes_file
    '''
    def get_node(self,nodeID:int)->Node:
        return self.nodes[nodeID] if nodeID in self.nodes else None

    '''
    param:
        nodeA:id of NodeA
        nodeB:id of NodeB
    return:
        Edge,info of the Edge between NodeA and NodeB
        None,if edge do not exists
    '''
    def get_edge(self,nodeA:int,nodeB:int)->Edge:
        return self.topology[nodeA][nodeB] if nodeB in self.topology[nodeA] else None

    '''
    param:
        nodeA:id of NodeA
        nodeB:id of NodeB
        A : A of edge
    return:
        None
    '''
    def add_edge(self,nodeA:int,nodeB:int,A:float)->None:
        self.max_NE = self.max_NE+1
        self.topology[nodeA][nodeB]=Edge(nodeA,nodeB,A,self.max_NE)
        self.topology[nodeB][nodeA]=Edge(nodeB,nodeA,A,self.max_NE)

    '''
    param:
        nodeA:id of NodeA
        nodeB:id of NodeB
    return:
        None
    '''
    def remove_edge(self,nodeA:int,nodeB:int):
        if nodeB in self.topology[nodeA]:
            self.topology[nodeA].pop(nodeB)
            self.topology[nodeB].pop(nodeA)

    '''
    param:
        nodeID:id of Node  
    return:
        list(Edge)
    '''
    def get_connected_edges(self,nodeID:int):
        edges = list(self.topology[nodeID].values())
        return edges
    '''
    param:
        nodeID:id of Node  
    return:
        list(Node)
    '''
    def get_connected_nodes(self,nodeID:int):
        edges = list(self.topology[nodeID].values())
        ids = [e.NodeB for e in edges]
        return ids

def test():
    data = CityData('data/Data_attributes_A_20200301.csv','data/Data_topology_A.csv')
    ids = data.get_ids()
    print('ids\n',ids)
    print('----------------------')
    print('get_node\n',data.get_node(ids[0]))
    print('get_node\n',data.get_node(ids[1]))
    print('----------------------')
    print('distance\n',data.distance(ids[0],ids[1]))#!!!!
    print('----------------------')
    print('get_edge\n',data.get_edge(ids[0],ids[1]))
    print('----------------------')
    print('add_edge\n',data.add_edge(ids[0],ids[1],10))
    print('----------------------')
    print('get_edge\n',data.get_edge(ids[0],ids[1]))
    print('----------------------')
    print('remove_edge\n',data.remove_edge(ids[0],ids[1]))
    print('----------------------')
    print('get_edge\n',data.get_edge(ids[0],ids[1]))
    print('----------------------')
    print('get_connected_edges\n',data.get_connected_edges(ids[0] ))
    edges =data.get_connected_edges(ids[1] )
    for e in edges:
        print(data.distance(e.NodeA,e.NodeB))
    print('----------------------')
    print('get nodes by type\n',data.get_ids_by_type('G'),data.get_ids_by_type('H'),data.get_ids_by_type('J'))

if __name__ == '__main__':
    test()