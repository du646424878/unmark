# coding:utf-8

from PIL import Image
import sys


def get_data(height, width, interval, datalen, start):
    # first line: 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0 ...
    data = []
    raw_line = [0] * interval
    raw_line.extend([1] * datalen)
    packlen = interval + datalen
    raw = raw_line * (int(width / packlen) + 2)
    start = packlen - start
    for i in xrange(height):
        if start > packlen:
            start = (start % packlen)
        data.extend(raw[start:start + width])
        start += 1
    return data



def transparent(point):
    if point[3] != 255 and (66 < point[0] < 70) and (66 < point[1] < 70) \
            and (62 < point[2] < 66):
        return True
    return False


def rec(x, i):
    a, b, c, d = x
    a = int((a - 68 * i) / (1 - i))
    b = int((b - 68 * i) / (1 - i))
    c = int((c - 64 * i) / (1 - i))
    return (a, b, c, d)


def unmark(filename):
    im = Image.open(filename)
    im = im.convert("RGBA")
    kk = im.load()
    nodes = get_data(im.size[1],im.size[0],13,7,3)

    print "SIZE: ", im.size

    for index, node in enumerate(nodes):
        if node == 0:
            continue

        i = index % im.size[0]
        j = index / im.size[0]

        if transparent(kk[i, j]):
            kk[i, j] = (0, 0, 0, 0)
        else:
            if (i > 1 and nodes[index - 1] == 0) or (j < im.size[1] - 1 and nodes[index + 1] == 0):
                kk[i, j] = rec(kk[i, j], 0.015)
            elif (i > 2 and nodes[index - 2] == 0) or (j < im.size[1] - 2 and nodes[index + 2] == 0):
                kk[i, j] = rec(kk[i, j], 0.065)
            else:
                kk[i, j] = rec(kk[i, j], 0.073)

    new_name = filename.lower().replace(".png", ".new.png")

    print "NEW: ", new_name
    im.save(new_name, "PNG")


if __name__ == '__main__':
    unmark(sys.argv[1])



