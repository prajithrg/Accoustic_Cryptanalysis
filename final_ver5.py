import numpy as np
import scipy as sp
import scipy.signal as sg
import matplotlib.pyplot as plt

import ast,random,sys


#sample_rate=44100
pth="./wmat/"
sample_rate=48000
stroke_period=.002

div=int(sample_rate*stroke_period)

data=np.fromfile(sys.argv[1],dtype="float32")
#print len(data)
dl=data.tolist()
plt.figure(0)
t=np.arange(0,len(dl),1)
plt.plot(t,dl)



fft_d=np.fft.fft(dl)
l=len(fft_d)
#plt.figure(1)
#t=np.arange(0,len(dl),1)
#plt.plot(t,abs(fft_d))
abs_fft=abs(fft_d)
#print len(abs_fft)
sum_lst=[]

for i in range(0,l/div):
    fft_v=np.fft.fft(dl[i*div:(i+1)*div])
    dummy=np.sum(abs(fft_v))
    sum_lst.append(dummy)

#nomalize the values
sum_lst=np.array(sum_lst)/max(sum_lst)


#new code to find a key press and release.
press_pos=[]
release_pos=[]
energythresh=0.22
glitchwin=5
pressrelwin=20
twokeysep=100

#find postions where energy is greater than a threshold
key_pos=np.array([i for i,x in enumerate(sum_lst) if x >energythresh])

#split the array for different key-strokes
keyslots=key_pos[np.diff(key_pos)>=twokeysep]
keyslotindex=[np.where(key_pos==j)[0][0]+1 for i,j in np.ndenumerate(keyslots)]
keyseparate=np.split(key_pos,keyslotindex)

#split each key to find press postion and release position
pressrelslots=[val[np.diff(val)>=pressrelwin] for val in keyseparate]
prerelslotindex=[] 
for k,arr in enumerate(pressrelslots):
    inter=[]
    for i,j in np.ndenumerate(arr):
        inter.append(np.where(keyseparate[k]==j)[0][0]+1)
#print inter
    prerelslotindex.append(inter)    

prerelseparate=[np.split(val,prerelslotindex[i]) for i,val in enumerate(keyseparate)]

press_pos=[val[0].tolist() for i,val in enumerate(prerelseparate)]
for i,val in enumerate(prerelseparate):
    if len(val)>1:
        release_pos.append(val[1].tolist())
    else:
        release_pos.append([])

#print "key",keyslots,keyslotindex,keyseparate
#print
#print "pressrelslots",pressrelslots
#print
#print "pressrelslotindex",prerelslotindex
#print
#print "prerelseparate",prerelseparate
#print
print "--"*70
print "Press position matrix:\n",np.matrix(press_pos)
print "--"*70
print "Release position matrix\n",np.matrix(release_pos)
print "--"*70


#create key-similarity matrices
def simmat(posarr,dl):
#count=4
    retmat=[]
    for row,val in enumerate(posarr):
        if posarr[row]!=[]:
            corrstart=posarr[row][0]*div
#corrend=(posarr[row][-1]+1)*div
            corrend=(posarr[row][0]+25)*div
            res=[]
            for r,c in enumerate(posarr):
                if posarr[r]!=[]:
                    cs=posarr[r][0]*div
#ce=(posarr[r][-1]+1)*div
                    ce=(posarr[r][0]+25)*div
#print "correlationpoints",corrstart,corrend,cs,ce
                    mid=(len(dl[corrstart:corrend])+len(dl[cs:ce]))/2.0
                    first=dl[corrstart:corrend]
                    second=dl[cs:ce]
#l=np.correlate(dl[corrstart:corrend],dl[cs:ce],'full').tolist()
                    l=np.correlate(first,second,'full').tolist()
#plt.figure(count)
#t=np.arange(0,len(l),1)
#plt.title("fig"+str(count))
#plt.plot(t,abs(np.array(l)))
#count=count+1
                    res.append(abs(mid-l.index(max(l))))
#res.append(l.index(max(l)))
                else:
                    res.append([])
#checkarr=list(res)
#checkarr.remove(1.0)
#print "arrmin",np.array(checkarr)-min(checkarr)
#print "arrmax",np.array(checkarr)-max(checkarr)
            retmat.append(res)
        else:
            retmat.append([])
    return retmat

dl=np.array(dl)/max(dl)
dl=dl.tolist()
presssim_mat=simmat(press_pos,dl)
#releasesim_mat=simmat(release_pos,dl)
#mean will not work change later
releasesim_mat=simmat(release_pos,dl)


print "Press correlation matrix\n",np.matrix(presssim_mat)
print "--"*70
print "Release correlation matrix\n",releasesim_mat
print "--"*70

#finding the mean matrix between press and relase sim matrices
simmeanmat=[]
for i,val in enumerate(presssim_mat):
    if releasesim_mat[i] !=[]:
        inter=[]
        for j,el in enumerate(val):
            if releasesim_mat[i][j]!=[]:
                inter.append((el+releasesim_mat[i][j])/2.0)
            else:
                inter.append(el)
        simmeanmat.append(inter)
    else:
        simmeanmat.append(val)


print "Mean correlation matrix\n",np.matrix(simmeanmat)
print "--"*70

def rankmat_justsorted(simmat):
    retmat=[]
    for row,val in enumerate(simmat):
        rowd=np.delete(val,row)
        s=sorted(rowd)
#print "s,rowd",s,rowd
        res=[s.index(i) for i in rowd]
        res.insert(row,-1)
        retmat.append(res)
    return retmat


#find the rank matrices
def rankmat(simmat):
    retmat=[]
    for row,val in enumerate(simmat):
        rowd=np.delete(val,row)
        rowdl=rowd.tolist()
        s=sorted(rowd)
        d=np.array(s)
        diffth=min(np.diff(d))
        dummypos=[]
        pos1=d[d<=50]
        pos2=d[np.logical_and(d>50,d<=150)]
        pos3=d[np.logical_and(d>150,d<=250)]
        pos4=d[np.logical_and(d>250,d<=350)]
        pos5=d[np.logical_and(d>350,d<=500)]
        pos6=d[np.logical_and(d>500,d<=900)]
        pos7=d[d>900]
#print pos1,pos2,pos3,pos4,pos5,pos6,pos7
        if(len(pos1)):
            dummypos.append(pos1[-1])
        if(len(pos2)):
            dummypos.append(pos2[-1])
        if(len(pos3)):
            dummypos.append(pos3[-1])
        if(len(pos4)):
            dummypos.append(pos4[-1])
        if(len(pos5)):
            dummypos.append(pos5[-1])
        if(len(pos6)):
            dummypos.append(pos6[-1])
        if(len(pos7)):
            dummypos.append(pos7[-1])
#print "dummypos",dummypos
        pos=np.array(dummypos)
        posindex=[np.where(d==j)[0][0]+1 for i,j in np.ndenumerate(pos)]
#print "posindex",posindex
        grouped=np.split(d,posindex)
        res=[3]*len(s)
#print "grouped",diffth,grouped
        print np.matrix(grouped)
        for i,val in enumerate(grouped):
            for k,l in np.ndenumerate(val):
#print l,s.index(l)
                res[rowdl.index(l)]=i+1
        res.insert(row,-1)
        retmat.append(res)
    return retmat

#rmat=rankmat(presssim_mat)
#rmat=rankmat(simmeanmat)
print "Grouped Matrix"
rmat=rankmat(simmeanmat)
print "--"*70
print "Rank Matrix\n",rmat
print "--"*70


rule_4=[['EQ','EQ','ADJ','NEAR'],
        ['EQ','ADJ','NEAR','DIST'],
        ['ADJ','NEAR','NEAR','DIST'],
        ['NEAR','DIST','DIST','DIST']
        ]

#assuming wordlength
wl=len(rmat[0])
#prints rule list
rulemat=[]
for i in range(wl):
#res=[]
    for j in range(i,wl):
        if i!=j:
            if (rmat[i][j]<=3 and rmat[j][i]<=3):
                rulemat.append(rule_4[rmat[i][j]][rmat[j][i]]) 
            else:
                rulemat.append('DIST')
#res.insert(i,'EQ')
#rulemat.append(res)

#rulemat=['DIST', 'DIST', 'DIST', 'ADJ','ADJ','NEAR', 'DIST', 'NEAR', 'DIST', 'DIST']
print "Rule Matrix\n",rulemat
print "--"*70


#load wadj,wnear and wdist matrices and find the word
fp=open(pth+"wmat_"+str(wl),"r")
weq=np.load(fp)
wadj=np.load(fp)
wnear=np.load(fp)
wdist=np.load(fp)
fp.close()

#all constrains b/w two words 
allc=[]
for i,val in enumerate(rulemat):
    if val=='EQ':
        allc.append(weq[i])
    elif val=='ADJ':
        allc.append(wadj[i])
    elif val=='NEAR':
        allc.append(wnear[i])
    elif val=='DIST':
        allc.append(wdist[i])
#print i,len(allc)
fullcon=np.matrix(allc)
def all_indices_equal(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

indexcnt={}
tcsum=np.matrix(np.zeros(len(wadj[0])))
for i in range(50):
#conin=np.matrix(np.random.randint(2,size=len(rulemat)))
#conin=np.matrix(np.ones(len(rulemat)))
#random length
    tcl=len(rulemat)
    rlen=np.random.randint(int(tcl*0.8),tcl)
    a = np.arange(tcl)
    np.random.shuffle(a)
    oneindex=a[:rlen]
    con=np.zeros(tcl)
    con[oneindex]=1
    conin=np.matrix(con)

    csum=conin*fullcon
    tcsum=csum+tcsum
#print "csum",conin,csum.max(),csum[0,643]
    csum=csum.tolist()[0]
#indices=all_indices_equal(max(csum),csum)
#all indices greater than a value
    cmax=max(csum)
    mid=cmax/2
    indices=[ i for i,x in enumerate(csum) if x>=mid]
    for j in indices:
        if j in indexcnt.keys():
            indexcnt[j]=indexcnt[j]+1
        else:
            indexcnt[j]=1

ranklist=sorted([(value,key) for (key,value) in indexcnt.items()])[::-1]
topindex=[i[1] for i in ranklist]
tcsumlist=tcsum.tolist()[0]
#top25=[i  for i in topindex if i>=50]
valthresh=int(max(tcsumlist)*0.8)
ranklist=[i  for i,val in enumerate(tcsumlist) if val>=valthresh]
#top25=sorted(ranklist)[::-1][:150]
top25=ranklist[:150]
#print "tcsumdetails",len(top25),tcsum.max(),tcsum[0,484],len(top25),ranklist

count=0
print "Top word results"
#display words
fp=open("dict_sorted","r")
index=ast.literal_eval(fp.readline())
#print "index",index[wl]
#-2 added to count for file line numbering
npindices=np.array(top25)+index[wl][0]-2
#print "npindices",npindices
for lineno,line in enumerate(fp):
#line=line.replace("\n","")
#if line=='cloud':
#print "cloudline",lineno
    if lineno in npindices:
        print line.replace("\n",""),",  ",
        count=count+1

print 
print "--"*70
plt.figure(3)
t=np.arange(0,len(sum_lst),1)
#plt.plot(t,abs(np.array(sum_diff_lst)),'bo')
plt.plot(t,abs(np.array(sum_lst)))
plt.show()
