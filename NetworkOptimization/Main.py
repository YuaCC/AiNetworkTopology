import pandas as pd
import os
import networkx as nx
from GenerateNetwork import getTopologyNetwork

def main():
    # 拓扑连接的文件路径
    pathOfCollection = '/mnt/4'

    # 第一步，读取赛题数据，创建网络拓扑
    topologyNetwork_ElementDict_A, topologyNetwork_ElementDict_B, topologyNetwork_ElementDict_C = getTopologyNetwork(pathOfCollection)

    # 第二步，预测每个城市的未来10天网络拓扑
        # 从topologyNetwork_ElementDict_A, topologyNetwork_ElementDict_B, topologyNetwork_ElementDict_C的字典中读取节点流量数据，然后处理

    # 第三步，优化网络结构

def test():
    print(1)

if __name__ == '__main__':
    main()
    # test()
