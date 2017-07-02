import Tkinter as tk
import ttk

colors_normal = ['#FCD5B5', '#FAC090']
colors_rainbow = ['#ffb3ba', '#ffc9ba', '#ffdfba', '#ffe8b3', '#ffffba', '#e2ffba',
                   '#baffc9', '#baffdc', '#bafeff', '#bad1ff', '#babdff', '#d9baff']


class PacketsList(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, bg='#FEF9F4', highlightthickness=0)

        ttk.Style().layout('Packets.Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])
        ttk.Style().configure('Packets.Treeview', foreground='#000000', background='#FEF9F4')

        self.packets = {}

        self.tree_frame = tk.Frame(self, bg='black')
        self.tree = ttk.Treeview(self.tree_frame, height=0, style='Packets.Treeview', show='headings')
        self.tree['columns'] = ['no', 'time', 'src', 'dst', 'protocol', 'length']
        cdata = [
            ('Index', False, 50, tk.E),
            ('Time', False, 100, tk.CENTER),
            ('Source', True, 120, tk.W),
            ('Destination', True, 120, tk.W),
            ('Protocol', True, 60, tk.CENTER),
            ('Length', False, 80, tk.E)
        ]
        self.size = 0
        for i, c in enumerate(cdata):
            cname = self.tree['columns'][i]
            self.tree.heading(cname, text=c[0])
            self.tree.column(cname, stretch=c[1], width=c[2], anchor=c[3])
        for i in range(12): self.tree.tag_configure('n%i' % i, background=colors_normal[i % 2])

        self.scroll = ttk.Scrollbar(self, style='Vertical.TScrollbar', orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll.set)

        self.img = tk.PhotoImage(file='CF_back.gif').subsample(2, 2)
        self.background = self.create_image((350, 160), image=self.img, anchor=tk.CENTER)

        self.bind('<Configure>', self.recenter_bg)
        self.rb = False

    def toggle_rb(self):
        self.rb = not self.rb
        c = colors_rainbow if self.rb else colors_normal; l = len(c)
        for i in range(12): self.tree.tag_configure('n%i' % i, background=c[i % l])

    def recenter_bg(self, *args):
        pos = self.coords(self.background)
        self.move(self.background, self.winfo_width() / 2 - pos[0],
                                   self.winfo_height() / 2 - pos[1])

    def pack(self, **kwargs):
        tk.Canvas.pack(self, **kwargs)
        self.tree_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, anchor=tk.N)
        self.tree.pack(expand=False, fill=tk.BOTH, side=tk.TOP, anchor=tk.N)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def add_packet(self, p):
        self.packets[
            self.tree.insert('', tk.END, values=(p.index, p.time, p.src, p.dst, p.protocol, len(p.raw_data)),
                             tags=('n%i' % (self.size % 12),))
        ] = p
        self.size += 1
        self.tree.config(height=self.size)

    def selected(self):
        selection = self.tree.selection()
        if selection: return self.packets[selection[0]]

    def clear(self):
        # self.packets = {}
        self.tree.delete(*self.tree.get_children())
        self.size = 0
        self.tree.config(height=0)
