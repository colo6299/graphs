

class Vertex:
    def __init__(self, data=None, edges=[]):
        self.edges = edges
        self.degree = len(edges)

    def add_edges(self, edges):
        self.edges.extend(edges)

    def get_neighbors(self):
        return self.edges

class ClownInterface:

    class PhonyVertex:

        def __init__(self, neighbor_list):
                self._neighbors = neighbor_list

        def get_neighbors(self):
            return self._neighbors


    def __init__(self, directed=True):
        self.directed = directed
        self._graph = CatchGraph(alpha=False)
        self._alpha_ord_dict = {}
        self._ord_alpha_list = []

    def _get_or_set_transdex(self, string):
        if self.string not in self._alpha_ord_dict:
            self._ord_alpha_list.append(string)
            self._alpha_ord_dict[string] = len(self._ord_alpha_list) - 1
            return len(self._ord_alpha_list) - 1
        else:
            return self._alpha_ord_dict[string]

    def add_vertex(self, vertex_name):  
        vertex_int = self._get_or_set_transdex(vertex_name)
        self._graph.add_vertex(vertex_int)
        return self._graph.array[vertex_int] # the "vertex"

    def add_edge(self, edge1, edge2):
        edge_pair = self._get_or_set_transdex(edge1), self._get_or_set_transdex(edge2)
        if self.directed:
            self._graph.add_edge(edge_pair)
        else:
            self._graph.add_neighbor(edge_pair)

    def get_vertex(self, string):
        ls = list(self._graph.array(self._alpha_ord_dict[string]).edges)
        for index, item in enumerate(ls):
            ls[index] = self._ord_alpha_list[item]
        return self.PhonyVertex(ls)


class CatchGraph:
    """
    Vertices should be treated as int id's as the end user.

    ew names no pls
    """

    def __init__(self, alpha=False):
        self.array = []
        self.size = 0
        self._empties = []  # Heads of empty space, can be size 1+ (update to heap!)
        self.alpha = alpha

    def _get_ord_if_alpha(self, char):

        if self.alpha is True and type(char) is str:
            return ord(char) - 65 # ish 
        elif self.alpha is False and type(char) is int:
            return char
        else:
            raise KeyError

    def _get_alpha_if_alpha(self, ndx):
        if self.alpha is False:
            return ndx
        else:
            return chr(ndx+65)
        
    def _next_empty(self):  # heads should be in descending order (insert @ ndx=0)
        if len(self._empties) is 0:
            return len(self.array)
        else:
            empty = self._empties[-1]
            if empty < (len(self.array)-1):
                if self.array[empty+1] is None:
                    self._empties[-1] = empty + 1
                else:
                    self._empties.pop() # IMPORTANT! prevent head collision
            else:                       # (somewhere around here)
                self._empties.pop()
            return empty

    def add_vertex(self, edges=[], data=None):
        self._catch_vertex(self._next_empty)
        self.array[self._next_empty()] = Vertex(edges, data)
        self.size += 1

    # funky interaction with _empties, may want to fix
    def set_vertex(self, vertex, edges=[], data=None):
        self._catch_vertex(vertex)
        self._catch_edges(edges)
        self.array[vertex] = Vertex(edges, data)

    def _validate_vertex(self, vertex):
        if vertex >= len(self.array):
            raise IndexError
        if self.array[vertex] is None:
            raise KeyError

    def has_vertex(self, vertex):
        if vertex >= len(self.array):
            raise False
        if self.array[vertex] is None:
            return False
        return True

    def get_edges(self, vertex):
        self._validate_vertex()
        return self.array[vertex].edges

    def has_edge(self, vertex, edge):  # sort the edge lists! (or add cleverly)
        self._validate_vertex()
        if edge in self.array[vertex].edges:
            return True
        else:
            return False
        
    # technically both _catchers are the same, the difference is semantics
    def _catch_edges(self, edges):
        for edge in edges:
            if edge >= len(self.array):
                self._empties.insert(0, len(self.array))
                self.array.extend([None] * (edge - len(self.array) + 1))

    # technically both _catchers are the same, the difference is semantics
    def _catch_vertex(self, vertex):
        if vertex >= len(self.array):
            self._empties.insert(0, len(self.array))
            self.array.extend([None] * (vertex - len(self.array) + 1))

    def add_edge(self, edge_pair):
        self._catch_edges(edge_pair)
        self.array[edge_pair[0]].edges.append(edge_pair[1])

    def add_edges(self, vertex, edges):
        self._catch_edges(edges)
        vertex.add_edges()

    def add_neighbor(self, edge_pair):
        self._catch_edges(edge_pair)
        self.array[edge_pair[0]].edges.append(edge_pair[1])
        self.array[edge_pair[1]].edges.append(edge_pair[0])

    def bfs_traversal(self, vertex=0):
        vertex = self._get_ord_if_alpha(vertex)
        retlist = []
        self._bfs_traversal_helper(vertex, retlist)
        for vertex in self.array:
            if vertex is not None:
                vertex.pop()
        return retlist
        
    def _bfs_traversal_helper(self, vertex_ndx, outlist=[]):
            vertex = self.array[vertex_ndx]
            if vertex is not None and vertex[-1] is not True:
                outlist.append(vertex_ndx)
                vertex.append(True)
                for neighbor in vertex:
                    self._bfs_traversal_helper(neighbor, outlist)
            
        
                


    
    
    

