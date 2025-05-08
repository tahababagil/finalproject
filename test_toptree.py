import unittest
from toptree import Vertex, Arc, Cluster, ClusterType, Data, Tree

class TestVertex(unittest.TestCase):
    def test_vertex_creation(self):
        v = Vertex(1)
        self.assertEqual(v.name, 1)
        self.assertIsNone(v.handle)
        self.assertIsNone(v.first_internal_cluster)
    
    def test_vertex_equality(self):
        v1 = Vertex(1)
        v2 = Vertex(1)
        v3 = Vertex(7)
        self.assertEqual(v1, v2)
        self.assertNotEqual(v1, v3)
    
    def test_vertex_copy(self):
        v = Vertex(10)
        v_copy = v.copy()
        self.assertEqual(v.name, v_copy.name)
        self.assertIsNot(v, v_copy)


class TestArc(unittest.TestCase):
    def test_arc_creation(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        c = Cluster(v1, v2)
        self.assertEqual(c.arc1.head, v1)
        self.assertEqual(c.arc2.head, v2)
    
    def test_get_twin(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        c = Cluster(v1, v2)
        self.assertEqual(c.arc1.get_twin(), c.arc2)
        self.assertEqual(c.arc2.get_twin(), c.arc1)
    
    def test_get_tail(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        c = Cluster(v1, v2)
        self.assertEqual(c.arc1.get_tail(), v2)
        self.assertEqual(c.arc2.get_tail(), v1)
    
    def test_can_rake(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        c = Cluster(v1, v2)
        c.arc1.prev = c.arc2
        c.arc2.prev = c.arc1
        self.assertTrue(c.arc1.can_rake())


class TestClusterType(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(ClusterType.RAKE.value, 1)
        self.assertEqual(ClusterType.COMPRESS.value, 2)
        self.assertEqual(ClusterType.DUMMY.value, 3)
        self.assertEqual(ClusterType.LEAF.value, 4)
        self.assertEqual(ClusterType.INVALID.value, 5)


class TestCluster(unittest.TestCase):
    def test_cluster_creation(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        c = Cluster(v1, v2)
        self.assertEqual(c.arc1.head, v1)
        self.assertEqual(c.arc2.head, v2)
        self.assertFalse(c.in_list)
        self.assertFalse(c.marked)
    
    def test_get_type_leaf(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        c = Cluster(v1, v2)
        self.assertEqual(c.get_type(), ClusterType.LEAF)
    
    def test_get_type_dummy(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        c1 = Cluster(v1, v2)
        c2 = Cluster(v1, v2, left=c1)
        self.assertEqual(c2.get_type(), ClusterType.DUMMY)
    
    def test_is_root(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        c = Cluster(v1, v2)
        c.arc1.next = c.arc2
        c.arc2.next = c.arc1
        self.assertTrue(c.is_root())


class TestData(unittest.TestCase):
    def test_data_creation(self):
        d = Data(max_cost=10)
        self.assertEqual(d.max_cost, 10)
        self.assertIsNone(d.ptr)


class TestTree(unittest.TestCase):
    def test_tree_creation(self):
        tree = Tree()
        self.assertEqual(len(tree.roots), 0)
    
    def test_link_and_cut(self):
        tree = Tree()
        v1 = Vertex(1)
        v2 = Vertex(2)
        
        tree.link(v1, v2, 5)
        self.assertEqual(len(tree.roots), 1)
        
        tree.cut(tree.roots[0])
        self.assertEqual(len(tree.roots), 0)
    
    def test_expose(self):
        tree = Tree()
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)
        
        tree.link(v1, v2, 5)
        tree.link(v2, v3, 7)
        
        exposed = tree.expose(v1, v3)
        self.assertIsNotNone(exposed)
        
        self.assertEqual(exposed.arc1.head.name, v1.name)
        self.assertEqual(exposed.arc2.head.name, v3.name)


if __name__ == '__main__':
    unittest.main()