from typing import Optional
from collections import deque
from enum import Enum
from dataclasses import dataclass
from collections import deque
@dataclass()
class Vertex:
    """
    Represents a vertex in a graph structure.
    Attributes:f
        name (str): The unique identifier for the vertex.
        handle (Optional[Arc]): A reference to an associated incoming arc, if any.
        first_internal_cluster (Optional[Cluster]): A reference to the first internal cluster,
        this is the cluster where the vertex becomes an internal vertex and no longer exists in the top tree
    Methods:
        __repr__():
            Returns theg = nx.DiGraph()
for i in range(len(adj)):
    for j in adj[i]:
        g.add_edge(i,j[0],capacity=j[1])
 string representation of the vertex (its name).
        __eq__(value):
            Compares this vertex with another vertex based on their names.
        copy():
            Creates and returns a copy of the vertex with the same name.
    """
    name : int = -1
    handle : Optional['Arc'] = None
    first_internal_cluster : Optional['Cluster'] = None

    def __repr__(self):
        return str(self.name) 
    
    def __eq__(self, value):
        return self.name == value.name

    def copy(self):
        return Vertex(self.name)
    
    def get_internal_clusters(self):
        if not self.first_internal_cluster: 
            return []
        
        assert self.first_internal_cluster.get_type != ClusterType.LEAF, "Leaf cluster cannot be the internal cluster"
        internal_clusters = []
        ptr = self.first_internal_cluster
        while ptr is not None:
            if ptr.marked:
                break
            internal_clusters.append(ptr)
            ptr.marked = True
            ptr = ptr.par
        return internal_clusters
    
    def get_root(self):
        assert self.handle is not None, "Vertex has no handle"
        
        ptr = self.handle.cluster
        while ptr.par:
            ptr = ptr.par
        return ptr
class Arc:
    """
    Represents an arc in the euler tour of a level for the top tree. An arc is like a node of a 
    doubly linked list.
    Attributes:
        cluster (Cluster): The cluster that contains this arc. A cluster has two arcs, with their
        heads representing endpoints of the cluster
        head (Vertex): The vertex that this arc points to, acting as the 'head' of the arc.
        next (Arc): The next arc in the Euler tour.
        prev (Arc): The previous arc in the Euler tour.
    Methods:
        __init__(cluster: Cluster, head: Vertex, next: Arc, prev: Arc):
            Initializes an Arc instance with the given cluster, head, next arc, and previous arc.
        get_twin() -> Arc:
            Returns the twin arc from the cluster. The twin arc is the other arc of the cluster.
        get_tail() -> Vertex:
            Retrieves the tail vertex of the arc, defined as the head vertex of the twin arc.
        __repr__() -> str:
            Returns a string representation of the Arc, displaying the tail and head vertices 
            in the format '<tail, head>'.
        can_rake() -> bool:
            Determines if the arc is eligible for a "rake" operation with its successor. 
        can_compress() -> bool:
            Checks if the arc can perform a "compress" operation with its successor.
    """
    
    def __init__(self,cluster : 'Cluster' = None, head : Vertex = None, next : 'Arc' = None, prev : 'Arc' = None):
        self.cluster : Cluster = cluster
        self.head : Vertex = head
        self.next : Arc = next
        self.prev : Arc = prev
        
    def get_twin(self):
        if self.cluster.arc1 is self:
            return self.cluster.arc2
        else:
            return self.cluster.arc1
        
    def get_tail(self):
        if self.cluster.arc1 is self:
            return self.cluster.arc2.head
        else:
            return self.cluster.arc1.head

    def __repr__(self):
        return f'<{self.get_tail()}, {str(self.head)}>'

    def can_rake(self):
        return self.prev is self.get_twin()
    
    def can_compress(self):
        return self.next.get_twin().next is self.get_twin()

class ClusterType(Enum):
    """
    Enumeration of cluster types used in the TopTree algorithm.

    This enum defines the different types of clusters that can exist in a TopTree structure:

    Attributes:
        RAKE (1): A cluster that represents a rake operation in the TopTree.
        COMPRESS (2): A cluster that represents a compress operation in the TopTree.
        DUMMY (3): A placeholder or dummy cluster, typically used for internal operations.
        LEAF (4): A leaf cluster, representing a single vertex or endpoint in the tree.
        INVALID (5): An invalid or uninitialized cluster state.
    """
    RAKE = 1
    COMPRESS = 2
    DUMMY = 3
    LEAF = 4
    INVALID = 5

class Cluster:
    
    def __init__(self, head=None, tail=None, data=None, left=None, right=None, par=None,in_list=False):
        """
        Attributes:
            par (Optional[Cluster]): Parent cluster reference.
            left (Optional[Cluster]): Left child cluster reference.
            right (Optional[Cluster]): Right child cluster reference.
            data (Optional[Data]): Data stored in the cluster.
            arc1 (Arc): Arc instance initialized using the head parameter.
            arc2 (Arc): Arc instance initialized using the tail parameter.
            in_list (bool): Indicates if the cluster is in a list.
            marked (bool): A flag used for marking the cluster, this is used in the expose operation.
        """
        self.par : Optional[Cluster] = par
        self.left : Optional[Cluster] = left
        self.right : Optional[Cluster] = right
        self.data : Optional[Data] = data
        self.arc1 : Arc = Arc(cluster=self, head=head)
        self.arc2 : Arc = Arc(cluster=self, head=tail)
        self.in_list = in_list 
        self.marked = False

    def get_height(self):
        if self.left is None and self.right is None:
            return 1
        elif self.left is None:
            return 1 + self.right.get_height()
        elif self.right is None:
            return 1 + self.left.get_height()
        else:
            return 1 + max(self.left.get_height(), self.right.get_height())
        
    def get_levels(self):
        levels = []
        deq = deque([self])
        while deq:
            levels.append([])
            for _ in range(len(deq)):
                cur = deq.popleft()
                levels[-1].append(cur.arc1)

                if cur.left:
                    deq.append(cur.left)
                if cur.right:
                    deq.append(cur.right)
        return levels
    def print_tree(self, et = True):
        print(f'Printing Level Order Traversal for {self.arc1}')
        levels =  self.get_levels()
        for level in levels:
            print(level)

        if not et:
            return
        
        print(f'Euler Tour for the tree:')
        for i, level in enumerate(levels):
            print(f'Level {i}')
            tour_level = []
            cur = level[0]
            tour_level.append(cur)
            print('Euler Tour')
            # print(cur)
            while cur.next is not level[0]:
                cur = cur.next
                # print(cur)
                tour_level.append(cur)
            print(tour_level)
            print('Euler Tour in reverse')
            tour_level = []
            cur = level[0]
            tour_level.append(cur)
            # print(cur)
            while cur.prev is not level[0]:
                cur = cur.prev
                # print(cur)
                tour_level.append(cur)
            print(tour_level)

    def split(self):
        if self.left.arc1.head.first_internal_cluster is self:
            self.left.arc1.head.first_internal_cluster = None
        if self.left.arc2.head.first_internal_cluster is self:
            self.left.arc2.head.first_internal_cluster = None

        if self.left is not None:
            self.left.par = None
        if self.right is not None:
            self.right.par = None
        self.left = None
        self.right = None
        return self.left, self.right
    
    def join(self, cluster_to_join, join_type):
        # join data of children clusters
        move_arc = None
        if self.arc1.next is cluster_to_join.arc1 or self.arc1.next is cluster_to_join.arc2:
            move_arc = self.arc1
        elif self.arc2.next is cluster_to_join.arc1 or self.arc2.next is cluster_to_join.arc2:
            move_arc = self.arc2
        elif cluster_to_join.arc1.next is self.arc1 or cluster_to_join.arc1.next is self.arc2:
            move_arc = cluster_to_join.arc1
        elif cluster_to_join.arc2.next is self.arc1 or cluster_to_join.arc2.next is self.arc2:
            move_arc = cluster_to_join.arc2
        else: 
            raise Exception("Invalid join")
        if join_type == ClusterType.COMPRESS:
            if self.data.max_cost > cluster_to_join.data.max_cost:
                new_data = self.data
            else:
                new_data = cluster_to_join.data
            compressed_with = move_arc.next
            new_cluster = Cluster(compressed_with.get_twin().get_tail(), move_arc.get_twin().head, new_data, move_arc.cluster, compressed_with.cluster)
            move_arc.head.first_internal_cluster = new_cluster
        elif join_type == ClusterType.RAKE:
            # print('rake')
            raked_on_to = move_arc.next
            new_cluster = Cluster(raked_on_to.head, raked_on_to.get_tail(), raked_on_to.cluster.data, move_arc.cluster, raked_on_to.cluster)
            move_arc.get_tail().first_internal_cluster = new_cluster
        else:
            raise Exception("Invalid join type")
        return new_cluster
    
    def get_type(self):
        if self.left is None and self.right is None:
            return ClusterType.LEAF
        elif self.left is None or self.right is None:
            return ClusterType.DUMMY
        elif (
            (
                self.right.arc1.head == self.arc1.head
                and self.right.arc2.head == self.arc2.head
            ) or (
                self.right.arc1.head == self.arc2.head
                and self.right.arc2.head == self.arc1.head
            )
        ):
            return ClusterType.RAKE
        else:
            return ClusterType.COMPRESS
    
    def is_cluster_valid(self):
        assert self.get_type() != ClusterType.LEAF, "Leaf cluster found in wrong place"
        if self.get_type() == ClusterType.RAKE:
            return (
                (
                    self.left.arc1.can_rake()
                    and self.left.arc1.next.cluster is self.right #or self.left.arc1.prev.cluster is self.right)
                )
                or (
                    self.left.arc2.can_rake()
                    and self.left.arc2.next.cluster is self.right # or self.left.arc2.prev.cluster is self.right)
                )
            )
        elif self.get_type() == ClusterType.COMPRESS:
            return (
                (
                    self.left.arc1.can_compress()
                    and self.left.arc1.next.cluster is self.right
                )
                or 
                (
                    self.left.arc2.can_compress()
                    and self.left.arc2.next.cluster is self.right
                )
            )
        
        raise Exception("Invalid cluster cluster type")
    
    def is_free(self, delete_next : list['Cluster']):
        return ( 
            # if parent doesnt exist
            self.par is None 
            #  node is dummy
            or self.par.get_type() == ClusterType.DUMMY
            # if parent will be deleted
            or self.par in delete_next
        )

    def is_root(self):
        if self.arc1.next is self.arc2 and self.arc2.next is self.arc1:
            return True
        return False
    
    def add_neighbors(self, neighbors : list['Cluster']):
        if not self.arc1.next.cluster.in_list:
            neighbors.append(self.arc1.next.cluster)
            self.arc1.next.cluster.in_list = True
        if not self.arc1.prev.cluster.in_list:
            neighbors.append(self.arc1.prev.cluster)
            self.arc1.prev.cluster.in_list = True
        if not self.arc2.next.cluster.in_list:
            neighbors.append(self.arc2.next.cluster)
            self.arc2.next.cluster.in_list = True
        if not self.arc2.prev.cluster.in_list:
            neighbors.append(self.arc2.prev.cluster)
            self.arc2.prev.cluster.in_list = True

    def create_dummy(self):
        dummy = Cluster(self.arc1.head, self.arc2.head, self.data, self)
        return dummy

class Data:
    
    def __init__(self, max_cost=None, ptr=None):
        self.max_cost = max_cost
        self.ptr = ptr
    



class Tree:
    
    def __init__(self):
        self.roots : list[Cluster] = []
    
    def print_tree(self,et=True):
        for i,root in enumerate(self.roots):
            print(f'Root {i}')
            root.print_tree(et=et)
    
    def cut(self, cluster):
        cluster.in_list = True
        self.__update([], [cluster])

    def link(self, u,v,c):
        new_clus = Cluster(u,v,in_list=True)
        d = Data(c,new_clus)
        new_clus.data = d

        self.__update([new_clus], [])


    def __is_move_valid(self, a : Arc, exposed_u, exposed_v) -> ClusterType:
        b : Arc = a.next
        a_clus, b_clus = a.cluster, b.cluster
        if a_clus is b_clus:
            return ClusterType.INVALID
        
        if (
                (
                    exposed_u is None 
                    or
                    (
                        a.head != exposed_u
                        and b.get_tail() != exposed_u
                    )
                ) and (
                    exposed_v is None 
                    or
                    (
                        a.head != exposed_v
                        and b.get_tail() != exposed_v
                    )
                ) and (
                    a.can_compress()
                )
        ):
            return ClusterType.COMPRESS
        elif (
                (
                    exposed_u is None 
                    or
                    (
                        a.get_tail() != exposed_u
                    )
                ) and (
                    exposed_v is None 
                    or
                    (
                        a.get_tail() != exposed_v
                    )
                ) and (
                    a.can_rake()
                )            
        ): 
            return ClusterType.RAKE
        else:
            return ClusterType.INVALID
    def __remove_from_euler_tour(self, clusters: list[Cluster], neighbors: list[Cluster], delete_next: list[Cluster]):
        for cluster in clusters:
            a = cluster.arc1
            b = cluster.arc2
            if not a.next or  not b.next:
                continue
            cluster.add_neighbors(neighbors)
            
            if cluster in self.roots:
                self.roots.remove(cluster)
            a.prev.next = b.next
            b.next.prev = a.prev
            b.prev.next = a.next
            a.next.prev = b.prev
            if cluster.par is not None:
                if not cluster.par.in_list:
                    delete_next.append(cluster.par)
                    cluster.par.in_list = True
                cluster.par.split()
                if cluster.par in self.roots:
                    self.roots.append(cluster.left)
                    self.roots.append(cluster.right)
                

            # handle logic not tested
            if a.head.handle is a:
                if a.get_twin().prev is a:
                    a.head.handle = None
                else:
                    a.head.handle = a.get_twin().prev

            if b.head.handle is b:
                if b.get_twin().prev is b:
                    b.head.handle = None
                else:
                    b.head.handle = b.get_twin().prev

    def __insert_into_euler_tour(self, clusters, neighbors: list[Cluster], level:int):
        if level == 1:
            self.__insert_into_euler_tour_base(clusters, neighbors)
        else:
            self.__insert_into_euler_tour_rest(clusters, neighbors)

    def __add_arc_to_euler_tour(self, arc : Arc, predecessor : Arc, successor : Arc):
        arc.prev = predecessor
        arc.next = successor
        predecessor.next = arc
        successor.prev = arc

    def __insert_into_euler_tour_base(self, clusters: list[Cluster], neighbors: list[Cluster]):

        for cluster in clusters:
                arc1 = cluster.arc1 
                arc2 = cluster.arc2
                predecessor_arc1 = arc1.get_tail().handle
                predecessor_arc2 = arc2.get_tail().handle
                if predecessor_arc2 is not None:
                    successor_arc1 = predecessor_arc2.next
                else:
                    predecessor_arc2 = arc1
                    successor_arc1 = arc2
                
                if predecessor_arc1 is not None:
                    successor_arc2 = predecessor_arc1.next
                else:
                    predecessor_arc1 = arc2
                    successor_arc2 = arc1
                    
                self.__add_arc_to_euler_tour(arc1, predecessor_arc1, successor_arc1)
                self.__add_arc_to_euler_tour(arc2, predecessor_arc2, successor_arc2)
                cluster.add_neighbors(neighbors)
                
                arc1.head.handle = arc1
                arc2.head.handle = arc2
                

    def __find_arc_successor(self, arc: Arc) -> Arc:
        cluster = arc.cluster
        w : Vertex = arc.head
        v : Vertex = arc.get_tail()
        assert cluster.get_type() != ClusterType.LEAF, "Leaf cluster found in wrong place (successor)"
        if cluster.get_type() == ClusterType.RAKE:
            A =  cluster.right
        elif cluster.get_type() == ClusterType.DUMMY:
            A = cluster.left 
        elif cluster.get_type() == ClusterType.COMPRESS:
            if cluster.left.arc1.head == w or cluster.left.arc2.head == w:
                A = cluster.left
            else:
                A = cluster.right
        

        if A.arc1.head == w:
            a = A.arc1
        else:
            a = A.arc2
        b = a.next
        # while a.prev.cluster.par.get_type() == ClusterType.RAKE and b.cluster is a.prev.cluster.par.right:
            # b = b.next

        B = b.cluster
        P = B.par
        if w == P.arc1.get_tail():
            return P.arc1
        else:
            return P.arc2

    def __find_arc_predecessor(self, arc: Arc) -> Arc:
        cluster = arc.cluster
        w : Vertex = arc.head
        v : Vertex = arc.get_tail()

        assert cluster.get_type() != ClusterType.LEAF, "Leaf cluster found in wrong place (predecesor)"
        if cluster.get_type() == ClusterType.RAKE:
            A = cluster.right
        elif cluster.get_type() == ClusterType.DUMMY:
            A = cluster.left
        elif cluster.get_type() == ClusterType.COMPRESS:
            if cluster.left.arc1.get_tail() == v or cluster.left.arc2.get_tail() == v:
                A = cluster.left
            else:
                A = cluster.right
        if A.arc1.get_tail() == v:
            a = A.arc1
        else:
            a = A.arc2
        b = a.prev
        while cluster.get_type() == ClusterType.RAKE and b.cluster is cluster.left:
            b = b.prev
        B = b.cluster
        P = B.par
        if v == P.arc1.head:
            return P.arc1
        else:
            return P.arc2
    
    def __verify_moves(self, neighbors : list[Cluster], delete_next : list[Cluster]):
        matched_moves = []
        
        for cluster in neighbors:
            
            if cluster.par is None or cluster.par.get_type() == ClusterType.DUMMY:
                continue
            
            if not cluster.par.is_cluster_valid():
                if cluster.par.left is cluster:
                    if not cluster.par.right.in_list:
                        neighbors.append(cluster.par.right)
                        cluster.par.right.in_list = True
                else:
                    if not cluster.par.left.in_list:
                        neighbors.append(cluster.par.left)
                        cluster.par.left.in_list = True
                if not cluster.par.in_list:
                    delete_next.append(cluster.par)
                    cluster.par.in_list = True
            else:
                matched_moves.append(cluster)

        for cluster_to_remove in matched_moves:
            neighbors.remove(cluster_to_remove)
            cluster_to_remove.in_list = False

    def __insert_into_euler_tour_rest(self, clusters: list[Cluster], neighbors: list[Cluster]):
        for cluster in clusters:

            pred = self.__find_arc_predecessor(cluster.arc1)
            succ = self.__find_arc_successor(cluster.arc1)
            self.__add_arc_to_euler_tour(cluster.arc1, pred, succ)

            pred = self.__find_arc_predecessor(cluster.arc2)
            succ = self.__find_arc_successor(cluster.arc2)
            self.__add_arc_to_euler_tour(cluster.arc2, pred, succ)

            cluster.add_neighbors(neighbors)

    def  __perform_valid_move(self, a: Arc, delete_next: list[Cluster], insert_next: list[Cluster], performed_moves: list[Cluster], exposed_u=None, exposed_v=None) -> bool:
        cluster = a.cluster
        b = a.next
        b_clus = b.cluster
        if cluster.is_free(delete_next) and b_clus.is_free(delete_next):
            validity = self.__is_move_valid(a, exposed_u, exposed_v)
            if validity != ClusterType.INVALID:
                # if cluster in self.roots:
                #     self.roots.remove(cluster)
                # if b_clus in self.roots:
                #     self.roots.remove(b_clus)

                if cluster.par is not None and not cluster.par.in_list:
                    # if cluster.par.arc1.head == Vertex(5) or cluster.par.arc2.head == Vertex(5):
                    #     print('here')
                    delete_next.append(cluster.par)
                    cluster.par.in_list = True
                if b_clus.par is not None and not b_clus.par.in_list:
                    delete_next.append(b_clus.par)
                    b_clus.par.in_list = True
                # insert_next.append(cluster)

                new_cluster = cluster.join(b_clus, validity)
                
                if cluster in self.roots:
                    self.roots.remove(cluster)
                if b_clus in self.roots:
                    self.roots.remove(b_clus)
                cluster.par = new_cluster
                b_clus.par = new_cluster
                insert_next.append(new_cluster)
                new_cluster.in_list = True
                performed_moves.append(cluster)
                performed_moves.append(b_clus)
                
                return True
        
        return False
                
        
    def __new_moves(self,clusters: list[Cluster], neighbors : list[Cluster], delete_next: list[Cluster], insert_next: list[Cluster],exposed_u=None,exposed_v=None) -> bool:
        performed_moves = []
        
        for cluster in clusters + neighbors:
            if not self.__perform_valid_move(cluster.arc1, delete_next, insert_next, performed_moves,exposed_u,exposed_v):
                self.__perform_valid_move(cluster.arc2, delete_next, insert_next, performed_moves,exposed_u,exposed_v)
            
        for cluster in clusters + neighbors:
            if cluster in performed_moves: #or cluster.par is not None or cluster.par in delete_next:
                continue
            
            if cluster.is_root():
                self.roots.append(cluster)
                continue
            if cluster.par and not cluster.par.in_list:
                delete_next.append(cluster.par)
                cluster.par.in_list = True
            if cluster in self.roots: 
                self.roots.remove(cluster)
            dummy = cluster.create_dummy()
            cluster.par = dummy
            insert_next.append(dummy)
            dummy.in_list = True

        if len(performed_moves) == 0:
            return False
        return True
            
        
            
    def __update(self, insert : list[Cluster], delete : list[Cluster],exposed_u=None,exposed_v=None) -> None:

        current_level : int = 1

        while len(insert) > 0 or len(delete) > 0:
            insert_next : list[Cluster] = []
            delete_next : list[Cluster] = []
            neighbors : list[Cluster] = []
            self.__remove_from_euler_tour(delete, neighbors,delete_next)
            self.__insert_into_euler_tour(insert, neighbors, current_level)
            self.__verify_moves(neighbors, delete_next)
            self.__new_moves(insert, neighbors, delete_next, insert_next, exposed_u, exposed_v)
            current_level += 1
            for cluster in insert + delete + neighbors:
                cluster.in_list = False
            
            delete = delete_next
            insert = insert_next
            
    def expose(self, u : Vertex, v : Vertex):
        # print(f'Exposing {u} and {v} gives following clusters:')
        if not u.handle or not v.handle:             
            return None
        
        if u.get_root() is not v.get_root():
            # vertices belong to different trees
            return None
        
        u_internal = u.get_internal_clusters()
        v_internal = v.get_internal_clusters()
        # vertices belong to same tree
        
        to_insert = []
        internals = u_internal + v_internal
        if not internals:
            return u.get_root()
        
        for cluster in internals:
            if cluster.left is not None and not cluster.left.marked :
                to_insert.append(cluster.left)
                cluster.left.marked = True
                
            if cluster.right is not None and not cluster.right.marked:
                to_insert.append(cluster.right)
                cluster.right.marked = True
                
        for cluster in internals + to_insert:
            cluster.marked = False
        I = []
        new_vertices = {}
        for clus in to_insert:
            i = clus.arc1.head
            j = clus.arc2.head
            
            # print(i,j)
            if i.name not in new_vertices:
                new_vertices[i.name] = Vertex(i.name)
            if j.name not in new_vertices:
                new_vertices[j.name] = Vertex(j.name)
            I.append(Cluster(new_vertices[i.name], new_vertices[j.name], clus.data, in_list=True))
            
        temporary_tree = Tree()
        temporary_tree.__update(I, [], new_vertices[u.name], new_vertices[v.name])
        # assert temporary tree has one root
        assert len(temporary_tree.roots) == 1, "Temporary tree has more than one root"
        return temporary_tree.roots[-1]
   