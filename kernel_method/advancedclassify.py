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