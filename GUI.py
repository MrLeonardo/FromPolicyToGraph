from ManageError import *
from tkinter import *
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD, tkdnd
from FromPolicyToGraph import *


class GUI:

    def __init__(self):
        self.managererror = ManageError()

        self.algorithms = None
        self.init_algorithm()

        self.root = TkinterDnD.Tk()
        self.root.title("FromPolicyToGraph")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.filename = StringVar(value="")
        self.firewall = StringVar(value="fortigate")
        self.algorithm = StringVar(value="layout_lgl")
        self.width = StringVar(value="2048")
        self.height = StringVar(value="2048")
        self.msgError = StringVar(value="")

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

        # size
        self.labelWidth = ttk.Label(self.mainframe, text='width:')
        self.entryWidth = ttk.Entry(self.mainframe, textvariable=self.width)
        self.labelHeight = ttk.Label(self.mainframe, text='height:')
        self.entryHeight = ttk.Entry(self.mainframe, textvariable=self.height)

        # label error
        self.labelError = ttk.Label(self.mainframe, text='')
        self.labelError.config(textvariable=self.msgError)

        # button
        self.btnOK = ttk.Button(self.mainframe, text="Okay", command=self.btnOKClick)

        self.lbFilename.grid(column=0, row=0, rowspan=6, padx=10)
        self.radioFirewallFortigate.grid(column=1, row=0, sticky=W, pady=(0, 10))
        self.comboAlgorithm.grid(column=1, row=1, pady=(0, 10))
        self.labelWidth.grid(column=1, row=2, pady=(0, 0))
        self.entryWidth.grid(column=2, row=2, pady=(0, 5))
        self.labelHeight.grid(column=1, row=3, pady=(0, 0))
        self.entryHeight.grid(column=2, row=3, pady=(0, 5))
        self.labelError.grid(column=0, row=7, pady=(0, 5))
        self.btnOK.grid(column=1, row=7, sticky=E)

    def run(self):
        self.root.mainloop()

    def btnOKClick(self):
        try:
            self.msgError.set('')
            error = self.validateInput()
            if not error:
                FromPolicyToGraph.fromPolicyToGraph(str(self.filename.get()),
                                                    str(self.firewall.get()),
                                                    str(self.algorithms[self.algorithm.get()]),
                                                    int(self.width.get()),
                                                    int(self.height.get()))
            else:
                self.manageError(error)
        except:
            self.manageError(self.managererror.GENERIC_ERROR)

    def validateInput(self):
        error = 0
        if not self.filename.get():
            error = self.managererror.FILE_NOT_FOUND
        elif not self.firewall.get():
            error = self.managererror.FIREWALL_NOT_FOUND
        elif not self.algorithm.get():
            error = self.managererror.ALGORITHM_NOT_FOUND
        elif not self.width.get():
            error = self.managererror.EMPTY_WIDTH
        elif not self.height.get():
            error = self.managererror.EMPTY_HEIGHT
        return error

    def manageError(self, codeError):
        self.msgError.set(self.managererror.get(codeError))

    def lbFilenameDnD(self, string):
        print("lbFilenameDnD")
        self.filename.set(string)
        self.lbFilename.delete(0, END)
        self.lbFilename.insert(0, os.path.basename(string))

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
