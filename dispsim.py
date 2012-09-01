import simlist
import sys,ast,itertools,math
    
key=simlist.KEY
adj=simlist.ADJ
near=simlist.NEAR
dist=simlist.DIST

comb=list(itertools.combinations(sys.argv[1],2))
ret=[]
for i,tup in enumerate(comb):
    inter=[]
    if ( tup[0].upper() in key and  tup[1].upper() in key):
        if tup[1].upper() ==  tup[0].upper():
            inter.append('EQ')
        if tup[1].upper() in adj[tup[0].upper()]:
            inter.append('ADJ')
        if tup[1].upper() in near[tup[0].upper()]:
            inter.append('NEAR')
        if tup[1].upper() in dist[tup[0].upper()]:
            inter.append('DIST')
        ret.append(tup[0]+tup[1]+"-->"+str(inter))

print ret
