# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from igraph import *
import matplotlib.pyplot as plt
import re

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    g = Graph(directed=True)
    state = 0

    f = open("fortigate.conf", "r")
    for x in f:
        if "config firewall address" in x:
            state = 1
        elif state == 1 and "edit" in x:
            g.add_vertex(re.findall(r'"([^"]*)"', x)[0])
            #print((g.vs.find(name=address)).index)
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
            #print(destination)
        elif state and x == "end\n":
            state = False

    print(g.vcount())
    print(g.ecount())

    print(g)

    g.vs["label"] = g.vs["name"]
    layout = g.layout("large")
    plot(g, layout=layout, bbox=(2048, 2048), margin=20)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
