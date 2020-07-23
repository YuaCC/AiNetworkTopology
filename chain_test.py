from chain import cal_chains

# main_chains, associate_chains, hang_points = cal_chains('data/Data_attributes_A_20200301.csv', 'data/Data_topology_A.csv')
main_chains, associate_chains, hang_points = cal_chains('data/Data_attributes_B_20200301.xlsx', 'data/Data_topology_B.csv')
# main_chains, associate_chains, hang_points = cal_chains('data/Data_attributes_C_20200301.csv', 'data/Data_topology_C.csv')
print(main_chains)
print(associate_chains)
print(hang_points)