from .data import CityData,Node,Edge
'''
:parameter
    beg,int, id of the start node
    end,int, id of the end node
    ids,list(int) or set(int),id of nodes can be visited,exclude beg and end 
    data,CityData 
return:
    list[int],id of nodes in path
'''
def fi_longest_path(beg:int,end:int,ids:set,data:CityData):
    def dfs(beg:int,end:int,ids:set,data:CityData,path:list):
        path.append(beg)
        if beg == end:
            res = path.copy()
        else:
            res = []
            beg_adjacent_ids = set(data.get_connected_nodes(beg))&ids
            novisited_beg_adjacent_ids = beg_adjacent_ids - set(path)
            for i in novisited_beg_adjacent_ids:
                p = dfs(i,end,ids,data,path)
                if len(p)>len(res):
                    res = p
        path.pop()
        return res
    ids.add(beg)
    ids.add(end)
    path = []
    return dfs(beg,end,ids,data,path)


'''
:parameter
    beg,int, id of the start node
    end,int, id of the end node
    ids,list(int) or set(int),id of nodes can be visited,exclude beg and end 
    data,CityData 
return:
    list[int],id of nodes in path
'''
def fi_shortest_path(beg:int,end:int,ids:set,data:CityData):
    ids.add(beg)
    ids.add(end)
    dis = {}
    pre = {}
    vis = set()
    dis[beg]=0
    pre[beg]=None
    while True:
        keys = dis.keys() - vis
        if len(keys)==0:
            break
        min_k = -1
        for k in keys:
            min_k = k if (min_k==-1 or dis[k]<dis[min_k]) else min_k
        vis.add(min_k)
        if min_k== end:
            break
        adjacent_ids = (set(data.get_connected_nodes(min_k)) & ids)-vis
        new_dis = dis[min_k]+1
        for i in adjacent_ids:
            if i not in dis or dis[i]>new_dis:
                dis[i]=new_dis
                pre[i] = min_k
    if end not in pre:
        return None
    else:
        now = end
        path = [end]
        while now !=beg:
            now = pre[now]
            path.append(now)
        path = path[::-1]
        return path
'''
:parameter 
    data,CityData 
    visited,set,id of nodes that have visited
return:
    list[list[int]],id of nodes in paths
'''
def cal_G_H_G_chain(data:CityData,visited:set)->list:
    g_ids = set(data.get_ids_by_type('G'))
    h_ids = set(data.get_ids_by_type('H'))
    result = []
    for i,beg in enumerate(g_ids):
        for j,end in enumerate(g_ids):
            if j>=i:
                break
            while True:
                ids = h_ids - visited
                res=fi_longest_path(beg,end,ids,data)
                if len(res)>=3:
                    result.append(res)
                    for id in res:
                        visited.add(id)
                else:
                    break
    return result


def cal_GH_J_GH_chain(data:CityData,visited:set):
    g_ids = data.get_ids_by_type('G')
    h_ids = data.get_ids_by_type('H')
    j_ids = data.get_ids_by_type('J')
    j_ids = set(j_ids)-visited
    gh_ids = set(g_ids)|set(h_ids)
    result = []

    for i,beg in enumerate(gh_ids):
        for j,end in enumerate(gh_ids):
            if j>=i:
                break
            beg_connected_ids = data.get_connected_nodes(beg)
            end_connected_ids = data.get_connected_nodes(end)
            for b in beg_connected_ids:
                if b not in j_ids:
                    continue
                for e in end_connected_ids:
                    if e not in j_ids :
                        continue
                    nodeb = data.get_node(b)
                    nodee = data.get_node(e)
                    if nodeb.A != nodee.A:
                        continue
                    ids = set([i for i in j_ids if data.get_node(i).A==nodeb.A ])
                    path = fi_shortest_path(b,e,ids,data)
                    if path is None or len(path)<=0:
                        continue
                    for i in path: visited.add(i)

                    path.insert(0,beg)
                    path.append(end)
                    result.append(path)
                    j_ids = j_ids-set(path)
    return result

def cal_J_J_GHJ_chain(data:CityData,visited:set,main_chain_nodes:set):
    g_ids = set(data.get_ids_by_type('G'))
    h_ids = set(data.get_ids_by_type('H'))
    j_ids = set(data.get_ids_by_type('J'))
    beg_ids = j_ids&main_chain_nodes
    end_ids = main_chain_nodes
    unvisited_j_ids = j_ids-visited
    result = []
    for i, beg in enumerate(beg_ids):
        for j, end in enumerate(end_ids):
            if beg == end:
                continue
            beg_connected_ids = data.get_connected_nodes(beg)
            end_connected_ids = data.get_connected_nodes(end)
            for b in beg_connected_ids:
                if b not in unvisited_j_ids:
                    continue
                for e in end_connected_ids:
                    if e not in unvisited_j_ids:
                        continue
                    nodeb = data.get_node(b)
                    nodee = data.get_node(e)
                    if nodeb.A != nodee.A:
                        continue
                    ids = set([i for i in unvisited_j_ids if data.get_node(i).A == nodeb.A])
                    path = fi_shortest_path(b, e, ids, data)
                    if path is None or len(path) <= 0:
                        continue
                    for i in path: visited.add(i)

                    path.insert(0, beg)
                    path.append(end)
                    result.append(path)
                    unvisited_j_ids = unvisited_j_ids - set(path)
    return result

def cal_hang_node(data:CityData,visited:set ):
    ids =set(data.get_ids())
    no_visited = ids - visited
    result= {}
    for i in no_visited:
        connected_ids = data.get_connected_nodes(i)
        result[i] = connected_ids[0]
        visited.add(i)
    return result
'''
:parameter
    attr_file,str
    topo_file,str
return:
    main_chains,list[list[int]],list of chains,
    associate_chains,list[list[int]],list of chains,
    hang_points,dict[int,int],dict[child_node]=parent_node
'''
def cal_chains(attr_file:str,topo_file:str):
    data  = CityData(attr_file,topo_file)
    visited = set()

    G_H_G_chain=cal_G_H_G_chain(data,visited)
    GH_J_GH_chain = cal_GH_J_GH_chain(data,visited)
    main_chains = G_H_G_chain+GH_J_GH_chain

    J_J_GHJ_chain = cal_J_J_GHJ_chain(data,visited,visited.copy())
    associate_chains = J_J_GHJ_chain

    hang_points = cal_hang_node(data,visited)
    return main_chains,associate_chains,hang_points

if __name__ == '__main__':
    main_chains,associate_chains,hang_points=cal_chains('chain/attr_test.csv','chain/topo_test.csv')
    print(main_chains)
    print(associate_chains)
    print(hang_points)