class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self,value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

class Graph():
    def __init__(self):
        self.nodes = {}
    def add_node(self, value):
        self.nodes[value] = set()
    def add_edge(self, p1, p2):
        self.nodes[p1].add(p2)
    def get_parents(self,node):
        return self.nodes[node]

def earliest_ancestor(ancestors, starting_node):
    g = Graph()
    
    for parent, child in ancestors:
        if child not in g.nodes:
            g.add_node(child)
        g.add_edge(child,parent)
    print(g.nodes)

    q = Queue()
    q.enqueue(starting_node)

    visited = set()
    path = []

    while q.size() > 0:
        current = q.dequeue()
        if current not in visited:
            visited.add(current)
            path.append(current)

            if current in g.nodes:
                parents = g.get_parents(current)
                for parent in parents:
                    q.enqueue(parent)
            else:
                pass
    print(path)
    return path[-1] if len(path) > 1 else -1 
