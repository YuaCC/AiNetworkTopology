import pandas as pd
import numpy as np
import networkx as nx
import os
import matplotlib.pyplot as plt
import math

# 获取网络拓扑图和图中每个网元节点
def getTopologyNetwork(collectionPath):
    # 读取所有文件
    collectionFiles = os.listdir(collectionPath)

    # 三个城市的网络拓扑以及创建过程
    topologyNetwork_A = nx.Graph()
    topologyNetwork_B = nx.Graph()
    topologyNetwork_C = nx.Graph()
    for collectionFile in collectionFiles:
        # 创建城市A的网络拓扑
        if 'Data_topology_A' in collectionFile:
            createTopologyNetwork(collectionPath, collectionFile, topologyNetwork_A)

        # 创建城市B的网络拓扑
        #if 'Data_topology_B' in collectionFile:
            #createTopologyNetwork(collectionPath, collectionFile, topologyNetwork_B)
        # 创建城市C的网络拓扑
        #elif 'Data_topology_C' in collectionFile:
            #createTopologyNetwork(collectionPath, collectionFile, topologyNetwork_C)


    '''
    # 三个城市各自的网络拓扑映射的字典，每个字典存储了所有的网元节点的属性
    topologyNetworkElementDict_A = dict()
    topologyNetworkElementDict_B = dict()
    topologyNetworkElementDict_C = dict()
    for collectionFile in collectionFiles:
        # 增加城市A的网元属性
        if 'Data_attributes_A' in collectionFile:
            addNetworkElementAttribute(collectionPath, collectionFile, topologyNetwork_A, topologyNetworkElementDict_A)
        # 增加城市B的网元属性
        elif 'Data_attributes_B' in collectionFile:
            addNetworkElementAttribute(collectionPath, collectionFile, topologyNetwork_B, topologyNetworkElementDict_B)
        # 增加城市C的网元属性
        elif 'Data_attributes_C' in collectionFile:
            addNetworkElementAttribute(collectionPath, collectionFile, topologyNetwork_C, topologyNetworkElementDict_C)

    # 将三个城市的拓扑结构和网元节点属性分别放到一起
    topologyNetwork_ElementDict_A = TopologyNetwork_ElementDict(topologyNetwork_A, topologyNetworkElementDict_A)
    topologyNetwork_ElementDict_B = TopologyNetwork_ElementDict(topologyNetwork_B, topologyNetworkElementDict_B)
    topologyNetwork_ElementDict_C = TopologyNetwork_ElementDict(topologyNetwork_C, topologyNetworkElementDict_C)

    return topologyNetwork_ElementDict_A, topologyNetwork_ElementDict_B, topologyNetwork_ElementDict_C
    '''
# 创建网络拓扑
def createTopologyNetwork(collectionPath, collectionFile, topologyNetwork):
    pathOfCollection = os.path.join(collectionPath, collectionFile)
    # 读取csv文件,转为二维数组
    collection = pd.read_csv(pathOfCollection)
    collectionList = collection.values.tolist()
    print(collectionList)

    # 可视化的点坐标
    networkElementPositionDict = dict()


    # 各个节点颜色
    node_list = []
    # 为网络拓扑加边,name属性代表边的编号NE，weight属性代表边的容量值A
    for i in range(len(collectionList)):
        print(len(collectionList[i]))
        if collectionList[i][9] != 200356609:
            continue
        if collectionList[i][3] == 'G':
            topologyNetwork.add_node(collectionList[i][0], color = 'red')
        elif collectionList[i][3] == 'H':
            topologyNetwork.add_node(collectionList[i][0], color = 'blue')
        elif collectionList[i][3] == 'J':
            topologyNetwork.add_node(collectionList[i][0], color = 'yellow')
        if collectionList[i][7] == 'G':
            topologyNetwork.add_node(collectionList[i][4], color = 'red')
        elif collectionList[i][7] == 'H':
            topologyNetwork.add_node(collectionList[i][4], color = 'blue')
        elif collectionList[i][7] == 'J':
            topologyNetwork.add_node(collectionList[i][4], color = 'yellow')

        topologyNetwork.add_edge(collectionList[i][0], collectionList[i][4], name = collectionList[i][9], weight = collectionList[i][8])
        if math.isnan(float(collectionList[i][1].strip())) and math.isnan(float(collectionList[i][2].strip())):
            # 坐标值没有缺失则加入坐标,否则让networkx自动生成坐标
            networkElementPositionDict[collectionList[i][0]] = [collectionList[i][1], collectionList[i][2]]
        if math.isnan(float(collectionList[i][5].strip())) and math.isnan(float(collectionList[i][6].strip())):
            # 坐标值没有缺失则加入坐标,否则让networkx自动生成坐标
            networkElementPositionDict[collectionList[i][4]] = [collectionList[i][5], collectionList[i][6]]

    # 绘制图形
    #pos = nx.spring_layout(topologyNetwork, pos=networkElementPositionDict)
    # print(edge_labels)
    nx.write_gexf(topologyNetwork, '..\\data\\{}.gexf'.format(collectionFile))




# 将每个网元节点的属性放到一个字典中，通过ID来索引这个网元节点的值
def addNetworkElementAttribute(collectionPath, collectionFile, topologyNetwork, topologyNetworkElementDict):
    # 哪天的数据
    train_day = collectionFile[18, 26]
    flowList = []

    # 得到文件路径
    pathOfNetworkElement = os.path.join(collectionPath, collectionFile)


    # 读取csv文件，转为二维数组
    networkElement = pd.read_csv(pathOfNetworkElement)
    networkElementList = networkElement.values.tolist()

    # 遍历这个文件
    for i in range(len(networkElementList)):
        # 确认这个点有没有在网络拓扑中
        if topologyNetwork.has_node(networkElementList[i][0]):
            # 设置每个小时的流量
            for j in range(6, 30):
                flowList.append(networkElementList[i][j])
            # 字典已经存在这个网元节点，则加入当天的24小时流量数据
            if networkElementList[i][0] in topologyNetworkElementDict:
                topologyNetworkElementDict[networkElementList[i][0]][train_day] = flowList
            # 否则新建一个键值对,里面存有未来十天的数据的数组，可以进行填充
            else:
                topologyNetworkElementDict[networkElementList[i][0]] = {
                    'type':networkElementList[i][1],
                    'A':networkElementList[i][2],
                    'longititude':networkElementList[i][3],
                    'latitude':networkElementList[i][4],
                    'D':networkElementList[i][5],
                    train_day:flowList,
                    '20200321':[],
                    '20200322':[],
                    '20200323':[],
                    '20200324':[],
                    '20200325':[],
                    '20200326':[],
                    '20200327':[],
                    '20200328':[],
                    '20200329':[],
                    '20200330':[]
            }
















