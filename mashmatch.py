from math import sqrt

rowoffset = [0.5,0.3,0.5] #accounting for keyboards not being a grid
rowdistance = 2.0
coldistance = 0.5

def readMapFile(filename):
    layouts = {}
    fileobj = open(filename)
    layoutname = False
    for line in fileobj.readlines():
        line = line.strip()
        if line[0] == '~':
            if layoutname:
                layouts[layoutname] = layout
            spline = line.split('~')
            layoutname = spline[1]
            line = '~'.join(spline[2:])
            row = -1
            layout = {}
        keys = line.split(' ')
        for col,key in enumerate(keys):
            mapto = [col,row]
            for k in key:
                layout[k] = mapto
        row += 1            
    fileobj.close()
    layouts[layoutname] = layout
    return layouts

def indPos(col, row):
    return [col*coldistance + sum(rowoffset[:row]), row*rowdistance]

def pythagoreanFunction(p1, p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def keyDistance(layout, k1, k2):
    pos1 = indPos(*keymaps[layout][k1])
    pos2 = indPos(*keymaps[layout][k2])
    return pythagoreanFunction(pos1, pos2)

def mashDistance(string, layout, alt):
    return sum([keyDistance(layout,mash[i],mash[i+1+alt]) for i in range(len(mash)-(alt+1))])

def mashMatch(string, layout):
    #TODO: remove strings that don't map to anything
    total = 0
    for i in range(len(string)-3):
        total += min(keyDistance(layout,string[i],string[i+1]),
                     keyDistance(layout,string[i],string[i+2]))
    return total

keymaps = readMapFile("keymaps.cfg")

print ("Welcome to keyboard mashing.")
print ("Currently supported layouts: %s" % (', '.join(keymaps.keys())))
print ("Type 'quit' to quit.\n")

mash = input("Mash your keyboard: ").replace(' ','')
while mash != "quit":
    best = 3**3**3 #sufficiently big
    bestName = ""
    for m in keymaps:
        score = mashMatch(mash, m)
        if score < best:
            best = score
            bestName = m
    print ("I think that you're using %s" % (bestName))

    mash = input("Mash your keyboard: ").replace(' ','')
