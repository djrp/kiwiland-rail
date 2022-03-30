import unittest
from kiwiland import Kiwiland

class KiwilandTests(unittest.TestCase):
    def setUp(self):
        self.kwl = Kiwiland(nodes=['A','B','C','D', 'E'],
                            arcs=[('A','B', 5), 
                                  ('B','C', 4), 
                                  ('C','D', 8), 
                                  ('D','C', 8), 
                                  ('D','E', 6), 
                                  ('A','D', 5), 
                                  ('C','E', 2), 
                                  ('E','B', 3), 
                                  ('A','E', 7)])

    # 1. The distance of the route A-B-C.
    def test_case01(self):
        self.assertEqual(self.kwl.route_distance(route=['A','B','C']), 9)

    # 2. The distance of the route A-D.
    def test_case02(self):
        self.assertEqual(self.kwl.route_distance(route=['A','D']), 5)

    # 3. The distance of the route A-D-C.
    def test_case03(self):
        self.assertEqual(self.kwl.route_distance(route=['A','D','C']), 13)

    # 4. The distance of the route A-E-B-C-D.
    def test_case04(self):
        self.assertEqual(self.kwl.route_distance(route=['A','E','B','C','D']), 22)

    # 5. The distance of the route A-E-D.
    def test_case05(self):
        self.assertEqual(self.kwl.route_distance(route=['A','E','D']), 'NO SUCH ROUTE')

    # 6. The number of trips starting at C and ending at C with a maximum of 3 stops. 
    # In the sample data below, there are two such trips: C-D-C (2 stops). and C-E-B-C (3 stops).
    def test_case06(self):
        self.assertEqual(self.kwl.number_of_trips(start_node='C',end_node='C', max_stops=3), 2)

    # 7. The number of trips starting at A and ending at C with exactly 4 stops. In the sample data below,
    # there are three such trips: A to C (via B,C,D); A to C (via D,C,D); and A to C (via D,E,B).
    def test_case07(self):
        self.assertEqual(self.kwl.number_of_trips(start_node='A',end_node='C', max_stops=4), 3)

    # 8. The length of the shortest route (in terms of distance to travel) from A to C.
    def test_case08(self):
        self.assertEqual(self.kwl.shortest_path(start_node='A',end_node='C'), 9)

    # 9. The length of the shortest route (in terms of distance to travel) from B to B.
    def test_case09(self):
        self.assertEqual(self.kwl.shortest_path(start_node='B',end_node='B'), 9)

    # 10. The number of different routes from C to C with a distance of less than 30. 
    # In the sample data, the trips are: CDC, CEBC, CEBCDC, CDCEBC, CDEBC, CEBCEBC, CEBCEBCEBC.
    def test_case10(self):
        self.assertEqual(self.kwl.number_of_trips_max_distance(start_node='C',end_node='C',max_distance=30), 7)


if __name__ == '__main__':
    unittest.main()
