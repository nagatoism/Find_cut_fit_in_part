def dist(p1,p2):
    return (p1[0]-p2[0])**2 +(p1[1]-p2[1])**2


def squash(pair_list):
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    n  = len(pair_list)
    for pair in pair_list:
        x1 += pair[0][0]
        x2 += pair[1][0]
        y1 += pair[0][1]
        y2 += pair[1][1]

    x1 = int(x1/n)
    x2 = int(x2/n)
    y1 = int(y1/n)
    y2 = int(y2/n)
    pt1 =(x1,y1)
    pt2 = (x2,y2)
    pair = (pt1,pt2)
    return pair

def merge_check_pair(pair_1,pair_2,BOUND=16):
    d1 = (dist(pair_1[0],pair_2[0]))
    d2 = (dist(pair_1[1],pair_2[1]))
    d3 = (dist(pair_1[0],pair_2[1]))
    d4 = (dist(pair_1[1],pair_2[0]))
    if(d1<=BOUND and d2<=BOUND):
        return False, True

    # if(d3<=BOUND and d4 <= BOUND):
    #     return True, True

    return False, False

def merge_check_point(p1,p2,BOUND=16):
    if(dist(p1,p2)<=BOUND):
        return True
    else:
        return False
def check_point_to_pair(p1,p2,BOUND=400):
    d = dist(p1,p2)
    if(200<d<=BOUND):
        # print('good pair',p1,p2,d)

        return True

    else:

        return False



def merge_points(point_list,BOUND =16):
    merging_list = []
    points_counter = []

    is_merged = [False] *len(point_list)
    for i in  range(len(point_list)):
        p1 = point_list[i]
        if(merging_list == None):
            neibour = []
            neibour.append(p1)
            is_merged[i] = True
            merging_list.append(neibour)

        else:
            for j in range(len(merging_list)):

                for p2 in merging_list[i]:

                    if(dist(p1,p2)<=BOUND):
                        merging_list[j].append(p1)
                        is_merged[i] = True
                        break
                    else:
                        pass
                if(is_merged[i] == True):
                    break
                else:
                    pass

            if(is_merge[i] == False):
                neibour = []
                neibour.append(p1)
                merging_list.append(neibour)
                is_merged[i] = True
                continue



    for merged_point in merging_list:
        points_counter.apppend[len(merged_point)]

    return points_counter,merging_list

def merge_pairs(pair_list):
    merging_list = []
    pairs_counter = []

    is_merged = [False] *len(pair_list)
    for i in  range(len(pair_list)):
        pair_1 = pair_list[i]
        if(merging_list == None):
            neibour = []
            neibour.append(pair_1)
            is_merged[i] = True
            merging_list.append(neibour)

        else:
            for j in range(len(merging_list)):

                for pair_2 in merging_list[j]:
                    is_swap,is_merge = merge_check_pair(pair_1,pair_2)
                    # if(is_swap == True):
                    #     pair_1 = (pair_1[1],pair_1[0])
                    #
                    # else:
                    #     pass

                    if(is_merge == True):
                        merging_list[j].append(pair_1)
                        is_merged[i] = True
                        break
                    else:
                        pass
                if(is_merged[i] == True):
                    break
                else:
                    pass
            if(is_merged[i] == False):
                neibour = []
                neibour.append(pair_1)
                merging_list.append(neibour)
                is_merged[i] = True
                continue

    for pairs in merging_list:
        pairs_counter.append(len(pairs))

    return pairs_counter,merging_list







if(__name__== '__main__'):
    print('this is the algorithm module')
