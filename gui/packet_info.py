import Tkinter as tk
import ttk


class PacketInfo(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, bg='#10253F')

        self.packet = None

        self.label_border = tk.Frame(self, bg='#7F7F7F', height=35)
        self.label_border.pack_propagate(False)
        self.label = tk.Label(self.label_border, bg='#a68c7a', fg='#10253F', anchor=tk.W, padx=10, font='TkDefaultFont 12 bold')

        self.scroll = ttk.Scrollbar(self, style='Vertical.TScrollbar', orient=tk.VERTICAL)

        ttk.Style().layout('Fields.Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])
        ttk.Style().configure('Fields.Treeview', background='#10253F', foreground='#FFFFFF')

        self.frame = tk.Frame(self, bg='#10253F')
        self.tree = ttk.Treeview(self.frame, show='tree', yscroll=self.scroll.set, style='Fields.Treeview')
        self.tree.tag_configure('layer', background='#20354F')
        self.scroll.config(command=self.tree.yview)

        self.opened_layers = set()

        self.tree.bind('<Control-c>', self.copy)

        # TODO
        # self.menu = tk.Menu(self)
        # self.menu.add_command(label='Insert As Filter', command=lambda: root.searchbar.insert(self.packet.getattr()))

    def pack(self):
        self.label_border.pack(fill=tk.X, side=tk.TOP, expand=False)
        self.label.pack(fill=tk.BOTH, anchor=tk.CENTER, expand=True, pady=(0, 1))
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP, anchor=tk.N)
        self.tree.pack(side=tk.TOP, expand=True, anchor=tk.N, fill=tk.BOTH, padx=4, pady=2)

    def copy(self, _):
        self.clipboard_clear()
        self.clipboard_append(self.tree.item(self.tree.selection()[0], 'text').split(': ', 1)[1])

    def set_packet(self, packet):
        for l in self.tree.get_children():
            name = self.tree.item(l, 'text')
            if self.tree.item(l, 'open'):
                self.opened_layers.add(name)
            elif name in self.opened_layers: self.opened_layers.remove(name)

        self.tree.delete(*self.tree.get_children())
        self.packet = packet

        if not packet:
            self.label.config(text='')
            return

        def insert(parent, fields):
            t = self.tree.insert(parent, tk.END, text=fields.name, tags=('layer',))
            for f in fields.value:
                if isinstance(fields.value[f].value, list):
                    l = self.tree.insert(t, tk.END, text=fields.value[f].name, tags=('layer',))
                    for i in fields.value[f].value: insert(l, i)
                else:
                    self.tree.insert(t, tk.END, text='%s: %s' % (fields.value[f].name, repr(fields.value[f])))
            return t

        for l in packet.layers:
            layer = insert('', getattr(packet, l))
            if self.tree.item(layer, 'text') in self.opened_layers:
                self.tree.item(layer, open=True)

        self.label.config(text='Packet %i: %i bytes (%i bits)' % (packet.index, len(packet.raw_data), len(packet.raw_data) * 8))
