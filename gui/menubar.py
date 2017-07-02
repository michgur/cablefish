import Tkinter as tk
import ttk


class Menubar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg='#F2F2F2')

        ttk.Style().layout('TMenubutton',
                           [('Menubutton.button', {'children':[('Menubutton.padding', {'children': [('Menubutton.label', {'sticky': ''})], 'expand': '1', 'sticky': 'we'})], 'expand': '1', 'sticky': 'nswe'})])

        self.file = ttk.Menubutton(self, text='File')
        self.file.menu = tk.Menu(self.file, tearoff=False)
        self.file.menu.add_command(label='New Capture', command=master.quit, accelerator='Ctrl+Enter')
        self.file.menu.add_command(label='Open', command=master.quit, accelerator='Ctrl+O')
        self.file.menu.add_command(label='Save', command=lambda: None)
        self.file.menu.add_command(label='Import', command=master.quit)
        self.file.menu.add_command(label='Export', command=master.quit)
        self.file.menu.add_separator()
        self.file.menu.add_command(label='Exit', command=master.app.quit, accelerator='Alt+F4')
        self.file['menu'] = self.file.menu

        self.edit = ttk.Menubutton(self, text='Edit')

        self.view = ttk.Menubutton(self, text='View')
        self.view.menu = tk.Menu(self.view, tearoff=False)
        self.view.menu.add_checkbutton(label='Rainbow', command=master.packets_panel.packets.toggle_rb)
        self.view.menu.add_checkbutton(label='Filter Hints', command=master.toggle_hints)
        self.view['menu'] = self.view.menu

        # self.poop = ttk.Menubutton(self, text='Poop')

    def pack(self, **kwargs):
        pass
        # disabled
        #
        # tk.Frame.pack(self, **kwargs)
        #
        # self.file.pack(side=tk.LEFT, fill=tk.BOTH)
        # self.edit.pack(side=tk.LEFT, fill=tk.BOTH)
        # self.view.pack(side=tk.LEFT, fill=tk.BOTH)
        # self.poop.pack(side=tk.LEFT, fill=tk.BOTH)
