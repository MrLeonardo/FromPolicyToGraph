from tkinter import *
from tkinter import ttk
from FromPolicyToGraph import *
from tkinterdnd2 import DND_FILES, TkinterDnD, tkdnd


class GUI:

    def __init__(self):
        self.algorithms = None
        self.init_algorithm()

        self.root = TkinterDnD.Tk()
        self.root.title("Hello TkInter!")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.filename = StringVar(value="")
        self.firewall = StringVar(value="")
        self.algorithm = StringVar(value="")

        self.mainframe = ttk.Frame(self.root, borderwidth=5, padding=(5, 5, 12, 12))
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_rowconfigure(3, weight=1)

        # drag and drop file
        self.lbFilename = Listbox(self.mainframe)
        self.lbFilename.insert(1, "drag files to here")
        self.lbFilename.drop_target_register(DND_FILES)
        self.lbFilename.dnd_bind('<<Drop>>', lambda e: self.lbFilenameDnD(e.data))

        # firewall
        self.radioFirewallFortigate = ttk.Radiobutton(self.mainframe, text='Fortigate', variable=self.firewall,
                                                      value='fortigate')

        # algoritmo
        self.comboAlgorithm = ttk.Combobox(self.mainframe, textvariable=self.algorithm)
        self.comboAlgorithm['values'] = tuple(self.algorithms.keys())

        # button
        self.btnOK = ttk.Button(self.mainframe, text="Okay", command=self.btnOKClick)

        self.lbFilename.grid(column=0, row=0, rowspan=6, padx=10)
        self.radioFirewallFortigate.grid(column=1, row=0, sticky=W, pady=(0, 10))
        self.comboAlgorithm.grid(column=1, row=1, pady=(0, 10))
        self.btnOK.grid(column=1, row=2, sticky=E)

    def run(self):
        self.root.mainloop()

    def btnOKClick(self):
        print("btnOKClick")
        print(FromPolicyToGraph.fromPolicyToGraph(str(self.filename.get()),
                                          str(self.firewall.get()),
                                          str(self.algorithms[self.algorithm.get()])))

    def lbFilenameDnD(self, string):
        print("lbFilenameDnD")
        self.filename.set(string)
        self.lbFilename.delete(0, END)
        self.lbFilename.insert(0, string)

    def init_algorithm(self):
        self.algorithms = {
            "layout_circle": "circle",
            "layout_drl": "drl",
            "layout_fruchterman_reingold": "fr",
            "layout_fruchterman_reingold_3d": "fr3d",
            "layout_kamada_kawai": "kk",
            "layout_kamada_kawai_3d": "kk3d",
            "layout_lgl": "large_graph",
            "layout_random": "random",
            "layout_random_3d": "random_3d",
            "layout_reingold_tilford": "rt",
            "layout_reingold_tilford_circular": "rt_circular",
            "layout_sphere": "sphere"
        }
