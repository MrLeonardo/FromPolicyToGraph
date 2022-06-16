import re
from igraph import *


class FromPolicyToGraph:

    @staticmethod
    def fromPolicyToGraph(filename, firewall, algorithm, width, height):
        if filename and algorithm and firewall:
            if "fortigate" in firewall:
                print("start")
                g = FromPolicyToGraph.parseFortigate(filename)
                print(g)

            if g.vcount():
                FromPolicyToGraph.plotGraph(g, algorithm, width, height)

    @staticmethod
    def parseFortigate(filename):
        g = Graph(directed=True)
        source = []
        state = 0

        f = open(filename, "r")
        for x in f:
            if "config firewall address" in x:
                state = 1
            elif state == 1 and "edit" in x:
                g.add_vertex(re.findall(r'"([^"]*)"', x)[0])
            elif "config firewall policy" in x:
                state = 2
            elif state == 2 and "edit" in x:
                state = 3
            elif state == 3 and "set srcaddr" in x:
                source = []
                try:
                    for y in re.findall(r'"([^"]*)"', x):
                        source.append((g.vs.find(name=y)).index)
                except:
                    g.add_vertex(y)
                    source.append((g.vs.find(name=y)).index)
            elif state == 3 and "set dstaddr" in x:
                destination = []
                try:
                    for y in re.findall(r'"([^"]*)"', x):
                        destination.append((g.vs.find(name=y)).index)
                except:
                    g.add_vertex(y)
                    destination.append((g.vs.find(name=y)).index)

                edge = [(x, y) for x in source for y in destination]
                g.add_edges(edge)
            elif state and x == "end\n":
                state = False

        return g

    @staticmethod
    def plotGraph(g, algorithm, width, height):
        g.vs["label"] = g.vs["name"]
        plot(g, layout=g.layout(algorithm), bbox=(width, height), margin=20)
