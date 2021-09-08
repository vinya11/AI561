import heapq
import collections
import time
class pathfinding(object):
    def __init__(self,graph,startX,startY,w,h,rockMaxHeight,settlements):
        self.graph = graph
        self.startX =startX
        self.startY=startY
        self.w = w
        self.h = h
        self.rockMaxHeight = rockMaxHeight
        self.settlements = settlements
    #A* algorithm
    def a(self):
        
        hn=list()
        path = collections.defaultdict(list)
        queue = list()
        heapq.heappush(queue, [0, (self.startX,self.startY)])
        visited= collections.defaultdict(list)
        visited[(self.startX,self.startY)] = 0
        path[(self.startX,self.startY)] =[]
        # X represents width, Y represents height
        #to access a graph it is graph[Y][X]
        while queue:
            # Dequeue a vertex from queue
            (vertexX,vertexY) = heapq.heappop(queue)[1]  
            pathcost = visited[(vertexX,vertexY)] 
            if (vertexX,vertexY) in self.settlements: 
                self.settlements.remove((vertexX,vertexY))
            if len(self.settlements) ==0:
                return self.settlements,path,visited
            for (neighbourX,neighbourY) in [(vertexX-1,vertexY-1),(vertexX-1,vertexY),(vertexX-1,vertexY+1),(vertexX,vertexY-1),(vertexX,vertexY+1),(vertexX+1,vertexY-1),(vertexX+1,vertexY),(vertexX+1,vertexY+1)]:
                rockHeight=0
                mudHeight =0
                
                if 0 <= neighbourX < self.w and 0 <=neighbourY < self.h:
                    if (self.graph[neighbourY][neighbourX]<0 and self.graph[vertexY][vertexX]<0):
                        rockHeight = max((self.graph[neighbourY][neighbourX])-self.graph[vertexY][vertexX],self.graph[vertexY][vertexX] - self.graph[neighbourY][neighbourX])
                    elif (self.graph[neighbourY][neighbourX]<0 or self.graph[vertexY][vertexX]<0):
                        rockHeight = abs(min((self.graph[neighbourY][neighbourX])-0,self.graph[vertexY][vertexX]-0))
                    if self.graph[neighbourY][neighbourX]>=0:
                        mudHeight = self.graph[neighbourY][neighbourX]
                    if (neighbourX,neighbourY) in [(vertexX-1,vertexY-1),(vertexX-1,vertexY+1),(vertexX+1,vertexY-1),(vertexX+1,vertexY+1)]:
                        cost = 14
                    else:
                        cost = 10

                    for site in self.settlements:
                        x,y = site
                        hn.append(abs(neighbourX-x) + abs(neighbourY-y))
                    totalcost = pathcost+cost + rockHeight + mudHeight #changed total cost
                    heuristicCost = totalcost+min(hn) #changed heuristic cost
                    hn=[]
                    if rockHeight <=self.rockMaxHeight:
                        if (neighbourX,neighbourY) not in visited or totalcost < visited[(neighbourX,neighbourY)]:
                            visited[(neighbourX,neighbourY)] = totalcost
                            path[(neighbourX,neighbourY)] = path[(vertexX,vertexY)] +[(vertexX,vertexY)] 
                            heapq.heappush(queue, (heuristicCost, (neighbourX,neighbourY))) #chnaged to heuristic cost
        return self.settlements,path,visited

    def ucs(self):
        
        path = collections.defaultdict(list)
        queue = list()
        heapq.heappush(queue, [0, (self.startX,self.startY)])
        visited= collections.defaultdict(list)
        visited[(self.startX,self.startY)] = 0
        path[(self.startX,self.startY)] =[]
        
        # X represents width, Y represents height
        #to access a graph it is graph[Y][X]

        while queue:
            
            # Dequeue a vertex from queue
            pathcost,(vertexX,vertexY) = heapq.heappop(queue)
            if (vertexX,vertexY) in self.settlements:
                self.settlements.remove((vertexX,vertexY))
            if len(self.settlements) ==0:
                return self.settlements,path,visited
            
            for (neighbourX,neighbourY) in [(vertexX-1,vertexY-1),(vertexX-1,vertexY),(vertexX-1,vertexY+1),(vertexX,vertexY-1),(vertexX,vertexY+1),(vertexX+1,vertexY-1),(vertexX+1,vertexY),(vertexX+1,vertexY+1)]:
                rockHeight=0
                if 0<= neighbourX < self.w and 0<=neighbourY < self.h:
                    if (neighbourX,neighbourY) in [(vertexX-1,vertexY-1),(vertexX-1,vertexY+1),(vertexX+1,vertexY-1),(vertexX+1,vertexY+1)]:
                        cost = 14
                    else:
                        cost = 10
                    if (neighbourX,neighbourY) not in visited or pathcost+cost < visited[(neighbourX,neighbourY)]:
                        if (self.graph[neighbourY][neighbourX]<0 and self.graph[vertexY][vertexX]<0):
                            rockHeight = max((self.graph[neighbourY][neighbourX])-self.graph[vertexY][vertexX],self.graph[vertexY][vertexX] - self.graph[neighbourY][neighbourX])
                        elif (self.graph[neighbourY][neighbourX]<0 or self.graph[vertexY][vertexX]<0):
                            rockHeight = abs(min((self.graph[neighbourY][neighbourX])-0,self.graph[vertexY][vertexX] - 0))
                        if rockHeight<=self.rockMaxHeight:
                            visited[(neighbourX,neighbourY)] = pathcost+cost
                            path[(neighbourX,neighbourY)] = path[(vertexX,vertexY)] +[(vertexX,vertexY)] 
                            heapq.heappush(queue, ((pathcost+cost), (neighbourX,neighbourY)))
            
        return self.settlements,path,visited
    # BFS algorithm
    def bfs(self):
        
        path = collections.defaultdict(list)
        visited, queue = dict(), collections.deque([(self.startX,self.startY)]) 
        for i in range(0,self.w): 
            for j in range(0,self.h): 
                visited[(i,j)] = False 
        visited[(self.startX,self.startY)] = True 
        
        path[(self.startX,self.startY)] =[]
        
        
        while queue:

            # Dequeue a vertex from queue
            vertexX,vertexY = queue.popleft()
            if (vertexX,vertexY) in self.settlements:
                self.settlements.remove((vertexX,vertexY))
            if len(self.settlements) ==0:
                return self.settlements,path,visited
                
            for (neighbourX,neighbourY) in [(vertexX-1,vertexY-1),(vertexX-1,vertexY),(vertexX-1,vertexY+1),(vertexX,vertexY-1),(vertexX,vertexY+1),(vertexX+1,vertexY-1),(vertexX+1,vertexY),(vertexX+1,vertexY+1)]:
                rockHeight=0
                if 0<= neighbourX < self.w and 0<=neighbourY < self.h and (neighbourX,neighbourY) and not visited[(neighbourX,neighbourY)]: #changed visited list to dict
                    
                    if (self.graph[neighbourY][neighbourX]<0 and self.graph[vertexY][vertexX]<0):
                        rockHeight = max((self.graph[neighbourY][neighbourX])-self.graph[vertexY][vertexX],self.graph[vertexY][vertexX] - self.graph[neighbourY][neighbourX])
                    elif (self.graph[neighbourY][neighbourX]<0 or self.graph[vertexY][vertexX]<0):
                        rockHeight = abs(min((self.graph[neighbourY][neighbourX])-0,self.graph[vertexY][vertexX] - 0))
                    if rockHeight<=self.rockMaxHeight:
                        
                        visited[(neighbourX,neighbourY)] = True # changed visited list to dict
                        path[(neighbourX,neighbourY)] = path[(vertexX,vertexY)] +[(vertexX,vertexY)]
                        queue.append((neighbourX,neighbourY))
                            
        return self.settlements,path,visited

settlements = list()
inputGraph = list()

with open("input.txt",'r') as f:
    lines  = f.read().splitlines()
#type of algorithm from the first line
algo = lines[0]
#width and height of the input graph
w,h = [int(num) for num in lines[1].rstrip(' ').split(' ')] 
#start x and y coordinates
startX,startY = [int(num) for num in lines[2].rstrip(' ').split(' ')] 
#maximum rock height
rockMaxHeight = int(lines[3])
#number of target settlements
nSettlements = int(lines[4])
#get the target settlements locations
for i in range(0,nSettlements):
    settlements.append(tuple([int(n)for n in lines[i+5].rstrip(' ').split(' ')]))
#get the input graph
for j in range(nSettlements+5,nSettlements+h+5):
    inputGraph.append([int(n)for n in lines[j].rstrip(' ').split(' ')]) 
targets= settlements.copy()

graphObject = pathfinding(inputGraph,startX,startY,w,h,rockMaxHeight,settlements)
if algo.lower()=='bfs':
    settlements,path,visited = graphObject.bfs()
elif algo.lower()=='ucs':
    settlements,path,visited = graphObject.ucs()
else:
    settlements,path,visited = graphObject.a()
with open('output.txt','w') as f:
    for target in targets[:len(targets)-1]:
        print(visited[target])
        if target in settlements:
            f.write("FAIL\n")
        else:
            
            path[target].append(target)
            
            f.write(' '.join([(','.join(map(str, idx))) for idx in path[target]])+'\n')
    target = targets[len(targets)-1]
    if target in settlements:
        f.write("FAIL")
    else:
        
        path[target].append(target)
        
        f.write(' '.join([(','.join(map(str, idx))) for idx in path[target]]))


    

    