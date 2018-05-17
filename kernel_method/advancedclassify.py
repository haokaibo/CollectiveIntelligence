import os

from matplotlib.pyplot import plot


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
    for cl,avg in averages.items():
        for i in range(len(avg)):
            avg[i] /= counts[cl]

    return averages