from math import sqrt

import logging


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


def readfile(filename):
    lines = [line for line in file(filename)]
    # First line is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def pearson(v1, v2):
    common_len = len(v1) if len(v1) < len(v2) else len(v2)

    # Simple sums
    sum1 = sum(v1[i] for i in range(common_len))
    sum2 = sum(v2[i] for i in range(common_len))
    # Sums of the squares
    sum1Sq = sum([pow(v1[i], 2) for i in range(common_len)])
    sum2Sq = sum([pow(v2[i], 2) for i in range(common_len)])
    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(common_len)])
    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / common_len)
    den = sqrt((sum1Sq - pow(sum1, 2) / common_len) * (sum2Sq - pow(sum2, 2) / common_len))
    if den == 0: return 0
    return 1.0 - num / den


def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1
    # Clusters are initially just the rows
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    if len(clust[i].vec) != len(clust[j].vec):
                        logging.error("clust[%d]=%d, clust[%d]=%d" \
                                      % (i, len(clust[i].vec), j, len(clust[j].vec)))
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                d = distances[(clust[i].id, clust[j].id)]
                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # calculate the average of the two clusters
        mergevec = [
            (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0
            for i in range(len(clust[0].vec))]

        # create the new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]],
                               distance=closest, id=currentclustid)

        # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)
    return clust[0]


def printclust(clust, labels=None, n=0):
    # indent to make a hierarchy layout
    for i in range(n): print ' ',
    if clust.id < 0:
        # negative id means that this is branch
        print '-'
    else:
        # positive id means that this is an endpoint
        if labels == None:
            print clust.id
        else:
            print labels[clust.id]

    # now print the right and left branches
    if clust.left != None: printclust(clust.left, labels=labels, n=n + 1)
    if clust.right != None: printclust(clust.right, labels=labels, n=n + 1)
