import re
from igraph import *


class FromPolicyToGraph:

    @staticmethod
    def info_prog(filename, firewall, algorithm):
        info = "" + \
               "filename: " + filename + \
               " firewall: " + firewall + \
               " algorithm: " + algorithm
        return info

    @staticmethod
    def fromPolicyToGraph(filename, firewall, algorithm):
        g = Graph(directed=True)
        state = 0

        if filename and algorithm and firewall:
            f = open(filename, "r")
            # f = open("conf/FGT3HD3917803825_6-4_1803_202204010809.conf", "r")
            for x in f:
                if "config firewall address" in x:
                    state = 1
                elif state == 1 and "edit" in x:
                    g.add_vertex(re.findall(r'"([^"]*)"', x)[0])
                    # print((g.vs.find(name=address)).index)
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
                    print(source)
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
                    print(destination)
                    print(edge)
                    # print(destination)
                elif state and x == "end\n":
                    state = False

            print(g.vcount())
            print(g.ecount())

            print(g)

            g.vs["label"] = g.vs["name"]
            layout = g.layout("large")
            plot(g, layout=layout, bbox=(2048, 2048), margin=20)
