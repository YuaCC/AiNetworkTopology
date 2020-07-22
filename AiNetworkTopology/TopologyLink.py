'''
定义一个拓扑连接结构，包括一个主链路，多个副链路，还有若干下挂点；
因为它本身已经定义了链路结构，所以我们需要做的是先区分链路中的主副链路和下挂，然后才能继续进行优化
链路：包含主副节点和下挂点，对应一个NE编号
主链路：在这个链路中，两头为G/H节点，中间是全H或者全J节点，两头组合可以是G/G,G/H,H/H
副链路：附属于主链路，两头为G/H/J，但是两头不能同时是G或者同时是H节点，就是两头的组合可以是G/H,G/J,H/J,J/J
下挂点：附属于一个点，我觉得一般是H/J

链路解析实现思路：
前提，已经构好图G，然后得到了一个链路的所有点集合S
（1）第一步是找主链路，先找到所有的G/H对，保证两两之间的A值相同，则可以继续第二步
（2）第二步是搜索每个G/H对的所有可能路径，找到中间节点的值相同的路径，然后确定为主链路，严格来说没有说中间节点的值一定要大于端点，这一步确定所有的主链路
（3）第三步就是根据主链路找副链路，后续再想
'''

import networkx as nx
import matplotlib.pyplot as plt

# 定义一个链路
class TopologyLink:
    # 初始化函数中，节点A是起始点，中间节点列表由A连接，节点B是终点
    def __init__(self, node_A, mid_node_list, node_B, topology_link_id):
        self.topology_link_id = topology_link_id
        self.main_link = MainLink(node_A, mid_node_list, node_B)

    # 可视化主链路
    def show_main_link(self):
        self.main_link.show_main_link()








# 定义一个主链路，附属于一个链路结构
class MainLink:
    def __init__(self, node_A, mid_node_list, node_B):
        self.node_A = node_A
        self.node_B = node_B
        self.mid_node_list = mid_node_list
        self.hashcode_1,self.hashcode_2 = self.gen_hashcode()

    # 可视化主链路
    def show_main_link(self):
        graph = nx.Graph()
        node_list = self.mid_node_list[:]
        node_list.insert(0, self.node_A)
        node_list.append(self.node_B)

        first_node = node_list[0]
        for second_node in node_list(1, len(node_list)):
            graph.add_edge(first_node.NodeID, second_node.NodeID)
            first_node = second_node
        nx.draw_networkx(graph)
        plt.show()

    # 生成链路的HASH值
    def gen_hashcode(self):
        node_list = self.mid_node_list[:]
        node_list.insert(0, self.node_A)
        node_list.append(self.node_B)
        hashcode_1 = ""
        hashcode_2 = ""
        # 正序遍历列表为一个hash值

        for node in node_list:
            hashcode_1 = hashcode_1 + str(node.NodeID)

        # 逆序遍历列表为一个hash值
        for node in reversed(node_list):
            hashcode_2 = hashcode_2 + str(node.NodeID)

        return hashcode_1,hashcode_2















