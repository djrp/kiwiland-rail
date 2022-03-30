"""kiwiland.py: Attempt to solve the kiwiland railroad assignemtn set by neo4j as part of recruitment process."""

__author__ = "Daniel Reader-Powell"

import logging
log = logging.getLogger(__name__)

class Kiwiland():
    def __init__(self, nodes, arcs):
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.getLogger().setLevel("INFO")
        self.nodes = nodes
        self.arcs= arcs
        log.debug(nodes)
        log.debug(arcs)
        self.graph = {}
        for source, dest, distance in self.arcs:
            log.debug(f"processing arc: {source}, {dest}, {distance}")
            try:
                destinations = self.graph[source]
                log.debug(f"current destinations for {source}: {destinations}")
                log.debug(f"adding destination, distance to node {source}")
                destinations[dest] = distance
                log.debug(f"new destinations for {source}: {destinations}")
                self.graph[source] = destinations
            except KeyError:
                self.graph[source] = { dest: distance}
                log.debug(f"node {source} is now {self.graph[source]}")
        log.debug(f"full graph is now: {self.graph}")

    def route_distance(self,route):
        count = 0
        for i, v in enumerate(route):
            try: 
                count += self.graph[v][route[i+1]]
            except IndexError:
                if count == 0:
                    return 'NO SUCH ROUTE'
                else:
                    return count
            except KeyError:
                return 'NO SUCH ROUTE'

    def number_of_trips(self, start_node, end_node,max_stops=None):
        paths = self.find_all_paths(start_node=start_node, end_node=end_node, path=[],max_stops=max_stops)
        return len(paths)

    def number_of_trips_max_distance(self, start_node, end_node,max_distance=None):
        paths = self.find_all_paths(start_node=start_node, end_node=end_node, max_stops=1000)
        log.debug(f"paths found: {paths}")
        limited_paths = []
        for path in paths:
            if path['distance'] <= max_distance:
                limited_paths.append(path)
        return len(limited_paths)

    def shortest_path(self,start_node,end_node):
        paths = self.find_all_paths(start_node=start_node, end_node=end_node, max_stops=1000)
        distance = None
        for path in paths:
          if distance == None:
              distance = path['distance']
          elif path['distance'] < distance:
              distance = path['distance']
        return distance

    def find_all_paths(self, start_node, end_node, path=[],stops=None,max_stops=None,distance=None):
        """ find all paths from start_node to 
            end_node in graph """
        if stops == None:
            stops = 0
        if distance == None:
            distance = 0
        graph = self.graph 
        path = path + [start_node]
        if ( start_node == end_node ) and ( stops != 0):
            return [{'route': path, 'distance': distance}]
        if start_node not in graph:
            return []
        paths = []
        for node in graph[start_node]:
            distance += graph[start_node][node]
            if ( node == end_node ) and ( stops != 0):
                return [{'route': path, 'distance': distance}]
            if stops > max_stops:
                break
            stops += 1
            if node not in path:
                extended_paths = self.find_all_paths(node, 
                                                     end_node, 
                                                     path,
                                                     stops,
                                                     max_stops,
                                                     distance)
                for p in extended_paths: 
                    paths.append(p)
        return paths

