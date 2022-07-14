import copy
def get_neighbours():
    
    f = open("tabu.txt", "r")
    dict_neighbours = {}

    for line in f:
        if line.split()[0] not in dict_neighbours:
            _list = list()
            _list.append([line.split()[1], line.split()[2]])
            dict_neighbours[line.split()[0]] = _list
        else:
            dict_neighbours[line.split()[0]].append([line.split()[1], line.split()[2]])
        if line.split()[1] not in dict_neighbours:
            _list = list()
            _list.append([line.split()[0], line.split()[2]])
            dict_neighbours[line.split()[1]] = _list
        else:
            dict_neighbours[line.split()[1]].append([line.split()[0], line.split()[2]])
    f.close()

    return dict_neighbours

def get_first_solution(dict_neighbours,node):
    
    startnode = node
    endnode = startnode

    firstsolution = []

    visiting = startnode

    distanceoffirstsolution = 0

    while visiting not in firstsolution:
        minim = 100
        for k in dict_neighbours[visiting]:
            if int(k[1]) < int(minim) and k[0] not in firstsolution:
                minim = k[1]
                bestnode = k[0]

        firstsolution.append(visiting)
        distanceoffirstsolution = distanceoffirstsolution + int(minim)
        visiting = bestnode

    firstsolution.append(endnode)

    position = 0
    for k in dict_neighbours[firstsolution[-2]]:
        if k[0] == startnode:
            break
        position += 1

    distanceoffirstsolution = distanceoffirstsolution + int(dict_neighbours[firstsolution[-2]][position][1]) - 100
    return firstsolution, distanceoffirstsolution

def get_neighborhood(solution, dict_neighbours):
    neighborhoodofsolution = []

    for n in solution[1:-1]:
        idx1 = solution.index(n)
        for kn in solution[1:-1]:
            idx2 = solution.index(kn)
            if n == kn:
                continue

            _tmp = copy.deepcopy(solution)
            _tmp[idx1] = kn
            _tmp[idx2] = n

            distance = 0

            for k in _tmp[:-1]:
                nextnode = _tmp[_tmp.index(k) + 1]
                for i in dict_neighbours[k]:
                    if i[0] == nextnode:
                        distance = distance + int(i[1])
            _tmp.append(distance)
            if _tmp not in neighborhoodofsolution:
                if _tmp!=[]:
                    neighborhoodofsolution.append(_tmp)    

    neighborhoodofsolution.sort(key=lambda x: x[-1])
    return neighborhoodofsolution



def tabu_search(firstsolution, distanceoffirstsolution, dict_neighbours, iters, size):
    count = 1
    solution = firstsolution
    tabulist = list()
    bestcost = distanceoffirstsolution
    bestsolutionever = solution
    firstexchangenode=''
    secondexchangenode=''
    while count <= iters:
        neighborhood = get_neighborhood(solution, dict_neighbours)
        print(neighborhood)
        indexofbestsolution =0
        bestsolution = neighborhood[indexofbestsolution]
        bestcostindex = len(bestsolution) - 1

        found = False
        while found is False:
            i = 0
            while i < len(bestsolution):

                if bestsolution[i] != solution[i]:
                    firstexchangenode = bestsolution[i]
                    secondexchangenode = solution[i]
                    break
                i = i + 1

            if [firstexchangenode, secondexchangenode] not in tabulist and [secondexchangenode,firstexchangenode] not in tabulist:
                tabulist.append([firstexchangenode, secondexchangenode])
                found = True
                solution = bestsolution[:-1]
                cost = neighborhood[indexofbestsolution][bestcostindex]
                if int(cost) < bestcost:
                    bestcost = cost
                    bestsolutionever = solution
            else:
                indexofbestsolution = indexofbestsolution + 1
                bestsolution = neighborhood[indexofbestsolution]


        if len(tabulist) >= size:
            tabulist.pop(0)

        count = count + 1

    return bestsolutionever, bestcost


print('************WATER OPTIMIZATION SYSTEM************')
d=get_neighbours()
print('Enter the node to start and end:')
n=input()
g,di=get_first_solution(d,n)
print('Enter the number of iterations:')
iters=int(input())
print('Enter the number of size:')
size=int(input())
print('The cost of the pipes with their diameters:')
print('************Diameter-------Cost In Rupees************')
print('1.          100 cm            1000            ')
print('2.          150 cm            1500            ')
print('3.          200 cm            2000            ')
print('Enter your choice')
n=int(input())
cost=0
if n==1:
    cost=1000
elif n==2:
    cost=1500
elif n==3:
    cost=2000
else:
    print('INVALID!!!')
    exit()
best_solution, best_l=tabu_search(g, di, d, iters, size)
print('The best solution is :')
print(best_solution)
print('The best solution distance is: ')
print(best_l)
print('Cost for the best solution:')
print(best_l*cost)



