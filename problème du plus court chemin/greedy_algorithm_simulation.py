from collections import namedtuple
import matplotlib.pyplot as plt 
import numpy as np 

# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
    return Edge(start, end, cost)

def G_cost(point,dest,source=(0,0)):
    if point == source :
        return 0 
    return (dest[0]-point[0])**2 + (dest[1]-point[1])**2

class Graph:
    def __init__(self, edges, obstacles=[]):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges if edge.start not in obstacles and edge.end not in obstacles ]
        self.obstacles = obstacles 
        
    @property
    def vertices(self):
        return set(
            # this piece of magic turns ([1,2], [3,4]) into [1, 2, 3, 4]
            # the set above makes it's elements unique.
            sum(    
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )
        
    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))
    
    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices }
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def Greedy_algo(self, source, dest): 
        assert source in self.vertices, 'Such source node doesn\'t exist'
        plt.text(dest[0],dest[1],'dest',fontsize=12)
        obs_x=[]
        obs_y=[]
        for obs in self.obstacles :
            obs_x += [obs[0]]
            obs_y += [obs[1]]
            plt.scatter(obs[0],obs[1],c='black')
        plt.plot(obs_x,obs_y,c='black',linewidth=3)
            
        # 1. Mark all nodes unvisited and store them.
        # 2. Set the distance to zero for our initial node 
        # and to infinity for other nodes.
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        openset = [source] 
        neighbours = self.neighbours 
        k=1
        while openset:
            plt.scatter(dest[0],dest[1],c='g')
            # 3. Select the unvisited node with the smallest distance, 
            # it's current node now.
            current_vertex = min(openset, key = lambda vertex: distances[vertex])  
            # 6. Stop, if the smallest distance 
            # among the unvisited nodes is infinity.
            if distances[current_vertex] == inf:
                break
            plt.scatter(current_vertex[0],current_vertex[1],c='r')
            # 4. Find unvisited neighbors for the current node 
            # and calculate their distances through the current node.
            for neighbour, cost in neighbours[current_vertex]:
                alternative_route = G_cost(neighbour,dest) 

                # Compare the newly calculated distance to the assigned 
                # and save the smaller one.
                if alternative_route < distances[neighbour]:
                    plt.scatter(neighbour[0],neighbour[1],c='b')
                    distances[neighbour] = alternative_route
                    openset.append(neighbour) 
                    previous_vertices[neighbour] = current_vertex

            # 5. Mark the current node as visited 
            # and remove it from the unvisited set.
            openset.remove(current_vertex)
            if current_vertex == dest :
                break
            k+=1
            plt.pause(1.0/(x*10**k))  


        path, current_vertex = [], dest
        while previous_vertices[current_vertex] is not None:
            path = [current_vertex] + path 
            current_vertex = previous_vertices[current_vertex]
        if path:
            path = [current_vertex] + path
        a_x=[]
        a_y=[]
        for v in path :
            a_x += [v[0]]
            a_y += [v[1]]
        plt.plot(a_x,a_y,c='g')
        return path
        
plt.ion() 
def grid(x,y):
    plt.grid()
    axe_x = [i for i in range(x+1)]
    for j in range(y+1):
        axe_y = [j for _ in range(y+1)]
        plt.scatter(axe_x,axe_y,c='grey')
        plt.axis([-0.01*x,x*1.01,-0.01*y,y*1.01])
    plt.show() 

def edges_1(a,b):
    ''' create edges for x*y vertices, each vertice has 3 edges 1 to the right ,1 up and 1 to up-right '''
    edges=[] 
    for x in range(a+1):
        for y in range(b+1):
            edges+=[make_edge((x,y),(x+1,y)),
            make_edge((x,y),(x,y+1)),
            make_edge((x,y),(x+1,y+1),1.4)] 
    return edges 

def create_obstacles(point1,point2):
    ''' create a list containing points representing a line that point1 and point2 defines '''
    obstacles=[] 
    if point1[0] == point2[0]:
        for i in range(point1[1],point2[1]+1):
            obstacles+=[(point1[0],i)] 
    else: 
        a = (point2[1]-point1[1])/float(point2[0]-point1[0])
        b = -point1[0]*a + point1[1] 
        for x in range(point1[0],point2[0]+1):
            obstacles+=[(x,a*x+b)] 
    return obstacles 

##an example : 
x = 10 #dimension du graph (longueur de l'axes des x)
y = 10 #dimension du graph (longueur de l'axes des y)

grid(x,y) 
G = Graph(edges_1(x,y),create_obstacles((4,1),(4,7)))

source = (0,0) # point depart 
dest = (5,6) # destination needs to be up-right the source ie dest[0]>source[0] and dest[1]>source[1] 

print(G.Greedy_algo(source,dest))







































































































































































































