import pandas as pd
import os
import networkx as nx
from GenerateNetwork import getTopologyNetwork
from Graph import Graph
from Graph import Node
from TopologyLink import TopologyLink

def main():
    # 拓扑连接的文件路径
    pathOfCollection = '..\\data\\test.csv'

    # 第一步，读取赛题数据，创建网络拓扑

    # 第二步，预测每个城市的未来10天网络拓扑

    # 第三步，优化网络结构

def test():
    pathOfCollection = '..\\data\\test.csv'

    # 解析文件
    # 读取csv文件,转为二维数组
    collection = pd.read_csv(pathOfCollection)
    collectionList = collection.values.tolist()

    # 对图上的点和边进行插入
    graph = Graph()
    for i in range(len(collectionList)):
        node_A = Node(collectionList[i][0], collectionList[i][1], collectionList[i][2])
        if collectionList[i][0] in graph.G_node_dict:
            node_A = graph.G_node_dict[collectionList[i][0]]
        elif collectionList[i][0] in graph.H_node_dict:
            node_A = graph.H_node_dict[collectionList[i][0]]
        elif collectionList[i][0] in graph.J_node_dict:
            node_A = graph.J_node_dict[collectionList[i][0]]

        node_B = Node(collectionList[i][3], collectionList[i][4], collectionList[i][5])
        if collectionList[i][3] in graph.G_node_dict:
            node_B = graph.G_node_dict[collectionList[i][3]]
        elif collectionList[i][3] in graph.H_node_dict:
            node_B = graph.H_node_dict[collectionList[i][3]]
        elif collectionList[i][3] in graph.J_node_dict:
            node_B = graph.J_node_dict[collectionList[i][3]]

        graph.insert_node(node_A)
        graph.insert_node(node_B)
        graph.add_edge(node_A, node_B)

    print(len(graph.G_node_dict))
    print(len(graph.H_node_dict))
    print(len(graph.J_node_dict))
    print("文件阅读完毕。。。")

    # 生成所有的链路
    topology_link_dict = graph.gen_all_topology_link()
    print(len(topology_link_dict))
    print("带有主链路的链路解析完毕。。。")

    topology_link_list = list(topology_link_dict.values())

    # 展示一个链路
    topology_link_list[0].show_main_link()



    print(1)

if __name__ == '__main__':
    # main()
    test()
