import numpy as np
import sys,ast,itertools,math

import simlist

pth="./wmat/"

key=simlist.KEY
adj=simlist.ADJ
near=simlist.NEAR
dist=simlist.DIST

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)


fp=open(sys.argv[1],"r")
index=ast.literal_eval(fp.readline())

#make W(adj,near and dist) matrix for set each n length words
lastl=0
cl=0
weq=np.zeros(0,dtype='int')
wadj=np.zeros(0,dtype='int')
wnear=np.zeros(0,dtype='int')
wdist=np.zeros(0,dtype='int')
fw=open(pth+"dummy","w")
for j,line in enumerate(fp):
    #taking \n to account
    line=line.replace("\n","")
    l=len(line)
    if(l!=lastl and l>=2):
        np.save(fw,weq)
        np.save(fw,wadj)
        np.save(fw,wnear)
        np.save(fw,wdist)
        fw.close()
        fw=open(pth+"wmat_"+str(l),"w")
        lastl=l
        coll=index[l][1]-index[l][0]+1
        weq=np.zeros((nCr(l,2),coll),dtype='int')
        wadj=np.zeros((nCr(l,2),coll),dtype='int')
        wnear=np.zeros((nCr(l,2),coll),dtype='int')
        wdist=np.zeros((nCr(l,2),coll),dtype='int')
        cl=0
#print "cl init",coll

    comb=list(itertools.combinations(line,2))
    
    for i,tup in enumerate(comb):
#print l,i,cl,line
        if ( tup[0].upper() in key and  tup[1].upper() in key):
            if (tup[1].upper() ==  tup[0].upper()):
                weq[i][cl]=1

            if tup[1].upper() in adj[tup[0].upper()]:
                wadj[i][cl]=1
        
            if tup[1].upper() in near[tup[0].upper()]:
                wnear[i][cl]=1

            if tup[1].upper() in dist[tup[0].upper()]:
                wdist[i][cl]=1
    cl=cl+1
#if line=='dove':
#print cl-1,weq[:,cl-1],"\n",wadj[:,cl-1],"\n",wnear[:,cl-1],"\n",wdist[:,cl-1]

print "Matrix creation done"
fp.close()

