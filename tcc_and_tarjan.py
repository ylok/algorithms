# preferences start at 1 not 0, but array indices start at 0
# https://en.wikipedia.org/wiki/Top_trading_cycle
def toptradingcycle(m):
   global nVert
   global edges
   global foundTCC
   nVert=len(m)
   foundTCC=[0 for i in range(nVert)]
   highestRemaining=[0 for i in range(nVert)]
   trades=[]
   finalgifts=[i+1 for i in range(nVert)]
   for i in range(nVert):
      if foundTCC[i]:
         continue
      # Identify edges for next step in the top trading cycle algorithm
      edges=[]
      for j in range(nVert):
         if foundTCC[j]:
            continue
         for k in range(highestRemaining[j],nVert):
            if m[j][k]!=-1:
               highestRemaining[j]=k
               break
         edges+=[[j+1,m[j][highestRemaining[j]]]]
      # identify SCCs from those above units
      TarjanSCC()
      # for each SCC (special case for SCC of size 1), add those
      # to the trades and remove them from future passes of the algorithm
      update=[]
      for comp in SCC:
         if len(comp)==1:
            continue
         for a in comp:
            trades+=[[a,m[a-1][highestRemaining[a-1]]]]
            finalgifts[a-1]=m[a-1][highestRemaining[a-1]]
            foundTCC[a-1]=1
            update+=[a]
      for a in update:
         for j in range(nVert):
            m[j][m[j].index(a)]=-1
   return trades,finalgifts

# and m[comp[0]-1][highestRemaining[comp[0]-1]]!=comp[0]:
m=[[2,4,3,1],
[1,2,3,4],
[1,3,2,4],
[1,2,3,4]]
toptradingcycle(m)

m=[[4, 2, 1, 7, 3, 6, 5, 8],
[7, 2, 5, 3, 6, 1, 8, 4],
[6, 7, 1, 3, 5, 2, 8, 4],
[6, 2, 7, 4, 1, 3, 8, 5],
[1, 8, 2, 7, 4, 5, 6, 3],
[8, 7, 6, 1, 3, 4, 2, 5],
[2, 7, 3, 8, 4, 6, 5, 1],
[1, 8, 4, 7, 2, 3, 5, 6]]
toptradingcycle(m)



foundTCC=[]
nVert=0
edges=[]
soNum=[]
soCounter=0
lowlink=[]
onStack=[]
stack=[]
SCC=[]
# Tarjan's SCC algorithm
# https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
def TarjanSCC():
   global soNum
   global soCounter
   global lowlink
   global onStack
   global stack
   global SCC
   global foundTCC
   soNum  =[-1 for i in range(nVert+1)] 
   for i in range(len(foundTCC)):
      if foundTCC[i]:
         soNum[i+1]=nVert+1
   soCounter=1
   lowlink=[nVert for i in range(nVert+1)]
   onStack=[0 for i in range(nVert+1)]
   stack=[]
   SCC=[]
   for v in range(1,nVert+1):
      if soNum[v]==-1:
         strongconnect(v)
   return

def strongconnect(v):
   # Initializations
   global soNum
   global soCounter
   global lowlink
   global onStack
   global stack
   global SCC
   soNum[v]=soCounter
   lowlink[v]=soCounter
   soCounter+=1
   onStack[v]=1
   stack+=[v]
   for e in edges:
      # must be an edge from current vertex
      if e[0]!=v: 
         continue
      # if vertex hasn't been explored, recurse
      # set lowlink to the lowest search order found by either vertex
      if soNum[e[1]]==-1: 
         strongconnect(e[1])
         lowlink[v]=min(lowlink[v],lowlink[e[1]])
      # if already has been visited, sets lowlink to the lowest
      # search order number
      elif onStack[e[1]]: #
         lowlink[v]=min(lowlink[v],soNum[e[1]])
      # if it has a search order number and its not on the stack, 
      # that means its already in SCC therefore ignore
      else:
         pass
   # At this point, algorithm has visited all vertices
   # that are reachable by vertex v. This is a SCC if this
   # vertex v is the "lowest" vertex in the SCC. If it isn't
   # then another vertex visited earlier is also a part of the
   # SCC. Do nothing until we reach that vertex
   # Once we reach that vertex, all later vertices on the
   # stack equal the SCC
   if soNum[v]==lowlink[v]:
      comp=stack[stack.index(v):]
      stack=stack[:stack.index(v)]
      for a in comp:
         onStack[a]=0
      SCC+=[comp]
   return

nVert=17
edges=[[10,9],[9,8],[8,10],[8,1],[1,2],[2,3],[3,4],[4,1],
[1,11],[11,12],[12,13],[13,12],[1,5],[5,6],[6,7],[7,1],
[6,14],[14,15],[15,16],[15,17],[16,17],[17,14]]
TarjanSCC()

Test Cases:
nVert=4
edges=[[1,2],[2,3],[3,4],[4,2]]
nVert=4
edges=[[1,2],[2,3],[3,4],[3,2],[2,4]]
nVert=17
edges=[[10,9],[9,8],[8,10],[8,1],[1,2],[2,3],[3,4],[4,1],
[1,11],[11,12],[12,13],[13,12],[1,5],[5,6],[6,7],[7,1],
[6,14],[14,15],[15,16],[15,17],[16,17],[17,14]]
* add [12,10] to above


