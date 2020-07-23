from chain import cal_chains

main_chains, associate_chains, hang_points = cal_chains('chain/attr_test.csv', 'chain/topo_test.csv')
print(main_chains)
print(associate_chains)
print(hang_points)