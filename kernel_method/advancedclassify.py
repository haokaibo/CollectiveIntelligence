import os

from matplotlib.pyplot import plot

from xml.dom.minidom import parseString
from urllib import urlopen, quote_plus



class matchrow:
    def __init__(self, row, allnum=False):
        row_len = len(row)
        if allnum:
            self.data = [float(row[i]) for i in range(row_len - 1)]
        else:
            self.data = row[0:row_len - 1]

        self.match = int(row[row_len - 1])


def loadmatch(file_path, allnum=False):
    rows = []
    if not os.path.exists(file_path):
        return None
    f = open(file_path, 'r')
    for line in f:
        rows.append(matchrow(line.split(','), allnum))

    return rows


def plot_age_matches(rows):
    xdm, ydm = [r.data[0] for r in rows if r.match == 1], \
               [r.data[1] for r in rows if r.match == 1]

    xdn, ydn = [r.data[0] for r in rows if r.match == 0], \
               [r.data[1] for r in rows if r.match == 0]

    plot(xdm, ydm, 'go')
    plot(xdn, ydn, 'ro')


def lineartrain(rows):
    averages = {}
    counts = {}
    for row in rows:
        # Get the class of this point
        cl = row.match
        averages.setdefault(cl, [0.0] * (len(row.data)))
        counts.setdefault(cl, 0)

        # Add this point to the averages
        for i in range(len(row.data)):
            averages[cl][i] += float(row.data[i])

        # Keep track of how many points in each class
        counts[cl] += 1

    # Divide sums by counts to get the averages
    for cl, avg in averages.items():
        for i in range(len(avg)):
            avg[i] /= counts[cl]

    return averages


def dotproduct(v1, v2):
    return sum([v1[i] * v2[i] for i in range(len(v1))])


def dpclassify(point, avgs):
    '''
    :param point:
    :param avgs:
    :return:
    '''
    b = (dotproduct(avgs[1], avgs[1]) - dotproduct(avgs[0], avgs[0])) / 2
    y = dotproduct(point, avgs[0]) - dotproduct(point, avgs[1]) + b
    if y > 0:
        return 0
    else:
        return 1


def yesno(v):
    if v == 'yes':
        return 1
    elif v == 'no':
        return -1
    else:
        return 0


def matchcount(interest1, interest2):
    l1 = interest1.split(':')
    l2 = interest2.split(':')
    x = 0
    for v in l1:
        if v in l2: x += 1
    return x


def milesdistance(a1, a2):
    return 0


loc_cache = {}


def getlocation(address, bing_map_key):
    # read the bing map key
    if address in loc_cache:
        return loc_cache[address]
    q = 'http://dev.virtualearth.net/REST/v1/Locations/%s?o=xml&key=%s' % (quote_plus(address), bing_map_key)

    data = urlopen(q).read()
    data = data[data.find('\r\n') + 2:]
    data = data[0:data.find('\r\n')]
    doc = parseString(data)
    lat = doc.getElementsByTagName('Latitude')[0].firstChild.nodeValue
    long = doc.getElementsByTagName('Longitude')[0].firstChild.nodeValue
    loc_cache[address] = (float(lat), float(long))
    return loc_cache[address]


def milesdistance(a1, a2):
    lat1, long1 = getlocation(a1)
    lat2, long2 = getlocation(a2)
    latdif = 69.1 * (lat2 - lat1)
    longdif = 53.0 * (long2 - long1)
    return (latdif ** 2 + longdif ** 2) ** .5

def scaledata(rows):
    low = [999999999.0] * len(rows[0].data)
    high = [-999999999.0] * len(rows[0].data)
    # Find the lowest and highest values
    for row in rows:
        d = row.data
        for i in range(len(d)):
            if d[i] < low[i]: low[i] = d[i]
            if d[i] > high[i]: high[i] = d[i]

    # Create a function that scales data
    def scaleinput(d):
        return [(d.data[i] - low[i]) / (high[i] - low[i])
                for i in range(len(low))]

    # Scale all the data
    newrows = [matchrow(scaleinput(row.data) + [row.match])
               for row in rows]
    # Return the new data and the function
    return newrows, scaleinput