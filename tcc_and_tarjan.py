# Written in Python 2.7.13
# Last updated by Ylok on 4/30/22
# For more information, see wiki page on ylok/algorithms

# Top trading cycles algorithm
# https://en.wikipedia.org/wiki/Top_trading_cycle
trades=[]
finalgifts=[]
def toptradingcycle(m):
   # Initializations
   global nVert
   global edges
   global foundTCC
   global trades
   global finalgifts
   nVert=len(m)
   foundTCC=[0 for i in range(nVert)]
   highestRemaining=[0 for i in range(nVert)]
   trades=[]
   finalgifts=[i+1 for i in range(nVert)]
   # Algorithm
   for i in range(nVert):
      # Part 1: Already found
      if foundTCC[i]:
         continue
      # Part 2: Identify edges
      edges=[]
      for j in range(nVert):
         if foundTCC[j]:
            continue
         for k in range(highestRemaining[j],nVert):
            if m[j][k]!=-1:
               highestRemaining[j]=k
               break
         edges+=[[j+1,m[j][highestRemaining[j]]]]
      # Part 3: Tarjan's SCC algorithm
      TarjanSCC()
      # Part 4: Bookkeeping
      update=[]
      for comp in SCC:
         if len(comp)==1 and m[comp[0]-1][highestRemaining[comp[0]-1]]!=comp[0]:
            continue
         elif len(comp)==1:
            foundTCC[comp[0]-1]=1
            update+=[comp[0]]
         else:
            for a in comp:
               trades+=[[a,m[a-1][highestRemaining[a-1]]]]
               finalgifts[a-1]=m[a-1][highestRemaining[a-1]]
               foundTCC[a-1]=1
               update+=[a]
      for a in update:
         for j in range(nVert):
            m[j][m[j].index(a)]=-1
   return

# Tarjan's stongly connected components (SCC) algorithm
# https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
foundTCC=[]
nVert=0
edges=[]
soNum=[]
soCounter=0
lowlink=[]
onStack=[]
stack=[]
SCC=[]
def TarjanSCC():
   # Initializations
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
   # Algorithm 
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
   # Algorithm 
   for e in edges:
      # Part 1: Valid edge
      if e[0]!=v: 
         continue
      # Part 2: Unvisited vertex
      if soNum[e[1]]==-1: 
         strongconnect(e[1])
         lowlink[v]=min(lowlink[v],lowlink[e[1]])
      # Part 3: Already visited, still on stack
      elif onStack[e[1]]:
         lowlink[v]=min(lowlink[v],soNum[e[1]])
      # Part 4: Already visited, no longer on stack
      else:
         pass
   # Conclusion (Part 5)
   if soNum[v]==lowlink[v]:
      comp=stack[stack.index(v):]
      stack=stack[:stack.index(v)]
      for a in comp:
         onStack[a]=0
      SCC+=[comp]
   return
