'''
定义一个城市的拓扑连接无向图结构；
图的数据结构为无向邻接图，通过一个点的ID和点的映射的字典实现；
'''

from TopologyLink import TopologyLink

# 定义图结构
class Graph:
    # 图初始化一个点的字典
    def __init__(self):
        # G节点字典
        self.G_node_dict = dict()
        # H节点字典
        self.H_node_dict = dict()
        # J节点字典
        self.J_node_dict = dict()


    # 往图中加点
    def insert_node(self, node):
        if node is None or node.NodeID is None:
            return False
        elif node.type == 'G':
            self.G_node_dict[node.NodeID] = node
        elif node.type == 'H':
            self.H_node_dict[node.NodeID] = node
        elif node.type == 'J':
            self.J_node_dict[node.NodeID] = node

    # 往图中加边
    def add_edge(self, node_A, node_B):
        # 先判断两个点不存在则不能加边
        if node_A is None or node_B is None:
            return False
        # 两点存在则加入图
        else:
            # 两个点连接起来,注意是添加的图的字典中的点，保证点的唯一性
            node_A.neighbor_dict[node_B.NodeID] = node_B
            node_B.neighbor_dict[node_A.NodeID] = node_A

    # 生成所有的主链路，因为一个主链路定义一个链路，同时确定了每一个链路
    def gen_all_topology_link(self):
        # 先找到所有的对
        couple_list = self.find_couple_list()

        # 找到所有对的路径,符合条件就是主链路，所以直接生成主链路集合--链路集合，确定所有的链路
        topology_link_dict = self.find_topology_link_dict(couple_list)

        return topology_link_dict


    # 找到所有的G/H节点对，前提是A值相同
    def find_couple_list(self):
        couple_list = []

        # 先把字典转列表
        G_node_list = list(self.G_node_dict.values())
        H_node_list = list(self.H_node_dict.values())

        # 找到所有的G的对
        for i in range(0, len(G_node_list)):
            node_A = G_node_list[i]
            for j in range(i+1, len(G_node_list)):
                node_B = G_node_list[j]
                # 两个点A值相同则加入到列表
                if node_A.A == node_B.A:
                    couple = Couple(node_A, node_B)
                    couple_list.append(couple)

        # 找到所有的H的对
        for i in range(0, len(H_node_list)):
            node_A = H_node_list[i]
            for j in range(i+1, len(H_node_list)):
                node_B = H_node_list[j]
                # 两个点A值相同则加入到列表
                if node_A.A == node_B.A:
                    couple = Couple(node_A, node_B)
                    couple_list.append(couple)
        # 找到所有的G/H对
        for i in range(0, len(G_node_list)):
            node_A = G_node_list[i]
            for j in range(0, len(H_node_list)):
                node_B = H_node_list[j]
                # 两个点A值相同则加入到列表
                if node_A.A == node_B.A:
                    couple = Couple(node_A, node_B)
                    couple_list.append(couple)

        for coup in couple_list:
            print(str(coup.node_A.NodeID)+":"+str(coup.node_A.A))
            print(str(coup.node_B.NodeID) + ":" + str(coup.node_B.A))
            print(".............")
        return couple_list

    # 找到所有点对之间的路径，然后判断是否符合主链路的要求,符合的就生成一个主链路
    def find_topology_link_dict(self, couple_list):
        # 链路字典集合
        topology_link_dict = dict()
        # 链路的id从0开始计数
        topology_link_id = 0
        for couple in couple_list:
            # 存储所有链路集合
            couple_link_list = []
            # 起始点为A，终点为B
            stack_list = []
            # 找到A点的所有邻居,转为list
            node_A_neighbors = list(couple.node_A.neighbor_dict.values())
            # 处理起始点，起始点设置为已访问，防止回环到起始点
            couple.node_A.isVisited = True
            print("start dfs head:"+str(couple.node_A.NodeID))
            # 搜索每个邻居能到达的可能链路集合
            for node_A_neighbor in node_A_neighbors:
                # 将端点的第一个邻居设置为已访问，加入到栈

                # 中间节点不能是G节点
                if node_A_neighbor.type == 'G':
                    continue
                node_A_neighbor.isVisited = True
                stack_list.append(node_A_neighbor)
                print("dfs continue go:" + str(node_A_neighbor.NodeID))
                # DFS递归深搜
                self.dfs(stack_list, couple_link_list, couple.node_B, node_A_neighbor.A, node_A_neighbor.type)
            # 恢复未访问状态
            couple.node_A.isVisited = False
            # 转为主链路结构
            for couple_link in couple_link_list:
                # 得到一个链路
                # 链路至少有三个点，即两个端点，一个中间节点
                if len(couple_link) == 0:
                    continue
                topology_link = TopologyLink(couple.node_A, couple_link, couple.node_B, topology_link_id)
                # 加入链路集合或者说加入主链路集合的条件是一定是不附属于一个链路
                if self.check_topology_link(topology_link_dict, topology_link):
                    topology_link_dict[topology_link_id] = topology_link
                topology_link_id += 1
        return topology_link_dict

    # 对新的链路（只包含了主链路)进行主链路的hash值比对，保证这个链路不附属于某个链路
    # ！！！！！！！未考虑两个主链路如果有中间节点部分重叠部分的情况,只考虑完全重叠，即一个链路包含另一个链路
    def check_topology_link(self, topology_link_dict, topology_link):
        # 新的主链路hash值
        hashcode_1_from_node = topology_link.main_link.hashcode_1
        hashcode_2_from_node = topology_link.main_link.hashcode_2
        result = True
        keys = list(topology_link_dict.keys())
        for key in keys:
            # 结果集合中主链路的hash值
            hashcode_1_from_dict = topology_link_dict[key].main_link.hashcode_1
            hashcode_2_from_dict = topology_link_dict[key].main_link.hashcode_2

            # 这个新链路附属于某个链路，不加入结果集合
            if hashcode_1_from_node in hashcode_1_from_dict or hashcode_1_from_node in hashcode_2_from_dict:
                return False

            # 如果这个新链路包含某个结果集合的链路，则需要移除被包含链路，然后继续搜索，看有没有链路附属于这个新链路，然后继续删除
            if hashcode_1_from_dict in hashcode_1_from_node or hashcode_1_from_dict in hashcode_2_from_node:
                topology_link_dict.pop(key)

        # 如果既不附属于某个结果集合中的主链路，也没有其他的结果集合中的点附属于这个主链路，则加入这个链路
        return result










    # DFS深度搜索所有可能的链路,value_A表示后面所有的A值必须与这个A值一致
    def dfs(self, stack_list, couple_link_list, end_node, value_A, type):
        # 判断是否是终点
        if stack_list[-1].NodeID == end_node.NodeID:
            # 将终点弹出,设置为未访问节点，后复制列表到结果中
            node_B = stack_list.pop()
            node_B.isVisited = False
            print("stop dfs end:" + str(node_B.NodeID))
            stack_copy_list = stack_list[:]
            couple_link_list.append(stack_copy_list)
        # 看是否是符合条件的点，是否是已经访问过的点
        else:
            node_neighbors = list(stack_list[-1].neighbor_dict.values())
            for node_neighbor in node_neighbors:
                print(str(node_neighbor.NodeID)+":"+node_neighbor.type+":"+str(node_neighbor.A))
                # 要保证下一个点未访问过，且A值要与所有中间点的值一致,或者找到了
                if (not node_neighbor.isVisited and node_neighbor.A == value_A  and node_neighbor.type == type) or node_neighbor.NodeID == end_node.NodeID:
                    node_neighbor.isVisited = True
                    stack_list.append(node_neighbor)
                    print("dfs continue go:" + str(node_neighbor.NodeID))
                    # DFS递归深搜
                    self.dfs(stack_list, couple_link_list, end_node, value_A, type)

            # 没有找到对应邻居或者遍历结束,将此点退栈,同时恢复其未访问状态
            node = stack_list.pop()
            print("dfs continue back:" + str(node.NodeID))
            node.isVisited = False


# 定义点结构
class Node:
    # 通过点的属性初始化一个点
    def __init__(self, NodeID, type, A):
        self.NodeID = NodeID
        self.type = type
        self.A = A
        self.topology_id = -1
        self.is_end_node = False

        # 存储了所有邻居点集合
        self.neighbor_dict = dict()

        # 是否访问过
        self.isVisited = False

# 两个端点组成的对
class Couple:
    def __init__(self, node_A, node_B):
        self.node_A = node_A
        self.node_B = node_B











