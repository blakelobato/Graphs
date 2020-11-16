"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # creates queue, adds start node to queue
        queue = Queue()
        queue.enqueue(starting_vertex)

        # check if visited
        visited = set()
        path = []

        while queue.size() > 0:
            current = queue.dequeue()
            path.append(current)
            # if not in visited, add to visited
            if current not in visited:
                visited.add(current)
                # get current's neighbors and add to queue
                neighbors = self.get_neighbors(current)
                for neighbor in neighbors:
                    queue.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        #create stack, add start node to stack
        stack = Stack()
        stack.push(starting_vertex)

        #check if visited
        visited = set()
        path = []

        while stack.size() > 0:
            current = stack.pop()
            #if not visited, add to visited
            path.append(current)
            if current not in visited:
                visited.add(current)
                # get current's neighbors and add to queue
                neighbors = self.get_neighbors(current)
                for neighbor in neighbors:
                    stack.push(neighbor)



    def dft_recursive(self, starting_vertex, visited=set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if starting_vertex in visited:
            return
        else:
            visited.add(starting_vertex)
            neighbors = self.get_neighbors(starting_vertex)

            if len(neighbors) == 0:
                return None

            for neighbor in neighbors:
                self.dft_recursive(neighbor,visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # similar to bft, traverse queue, add the path to queue
        q = Queue()
        # add initial vertex path add path to queue
        visited = set()
        q.enqueue([starting_vertex])
        #check curr vertex neighbor for neighbor
        while q.size() > 0:
            current_path = q.dequeue() #list of verticies
            current_node = current_path[-1]

            if current_node == destination_vertex:
                return current_path

            if current_node not in visited:
                visited.add(current_node)

                for neighbor in self.get_neighbors(current_node):
                    new_path = current_path.copy()
                    new_path.append(neighbor)
                    q.enqueue(new_path)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        visited = set()
        s.push([starting_vertex])
        while s.size() > 0:
            current_path = s.pop()
            current_node = current_path[-1]

            if current_node == destination_vertex:
                return current_path
            if current_node not in visited:
                visited.add(current_node)

                for neighbor in self.get_neighbors(current_node):
                    new_path = current_path.copy()
                    new_path.append(neighbor)
                    s.push(new_path)

        

    def dfs_recursive(self, starting_vertex, destination_vertex, visited = set(), path=[]):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if len(path) == 0:
            path.append(starting_vertex)

        if starting_vertex == destination_vertex:
            return path

        visited.add(starting_vertex)

        neighbors = self.get_neighbors(starting_vertex)

        if len(neighbors) == 0:
            return None
        
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = path + [neighbor]
                result = self.dfs_recursive(neighbor, destination_vertex, visited, new_path)
                if result is not None:
                    return result

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
