import Tkinter as tk
from packet_info import PacketInfo
from packets_list import PacketsList


class SearchBar(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, bg='#7F7F7F', height=3)
        self.frame = tk.Frame(self, bg='#D9D9D9')

        self.command = None

        self.search = tk.Entry(self.frame, bg='#FFFFFF', width=60)
        self.search.clear = True
        self.search.bind('<FocusIn>', self.focus_in)
        self.search.bind('<FocusOut>', self.focus_out)
        self.search.bind('<Return>', lambda _: self.focus_force())
        self.clear_search()

        self.apply = tk.Label(self.frame, text='Apply', bg='#D9D9D9')
        self.apply.bind('<Button-1>', self.apply_search)
        self.clear = tk.Label(self.frame, text='Clear', bg='#D9D9D9')
        self.clear.bind('<Button-1>', self.clear_search)

    def setCommand(self, cmd):
        print '>:(', cmd
        self.command = cmd
        print self.command

    def insert(self, text):
        if self.search.clear: self.focus_in(None)
        self.search.insert(tk.END, text)
        self.search.focus_force()

    def clear_search(self, _=None):
        self.search.delete(0, tk.END)
        self.search.insert(0, 'filter...')
        self.search.config(fg='#777777')
        self.search.clear = True
        self.focus_force()

        if callable(self.command): self.command('')

    def apply_search(self, _):
        if not self.search.clear and callable(self.command):
            self.command(self.search.get())

    def focus_in(self, _):
        if not self.search.clear: return
        self.search.clear = False
        self.search.delete(0, tk.END)
        self.search.config(fg='#000000')

    def focus_out(self, _):
        if not self.search.get(): self.clear_search()
        else: self.apply_search(_)

    def pack(self, **kwargs):
        tk.Frame.pack(self, **kwargs)
        self.frame.pack(fill=tk.BOTH, anchor=tk.CENTER, expand=True, pady=1)
        self.search.pack(side=tk.LEFT, fill=tk.Y, padx=3, pady=3, expand=True)
        self.apply.pack(side=tk.LEFT, anchor=tk.W, padx=10)
        self.clear.pack(side=tk.LEFT, anchor=tk.W, expand=False)


class PacketsPanel(tk.PanedWindow):
    def __init__(self, root):
        tk.PanedWindow.__init__(self, root, orient=tk.VERTICAL, sashpad=0, sashwidth=4, bd=0, bg='#7F7F7F')

        self.top = tk.Frame(root, bg='#FEF9F4')
        self.searchbar = SearchBar(self.top)
        self.packets = PacketsList(self.top)
        self.add(self.top, height=350)

        self.packet_info = PacketInfo(root)
        self.add(self.packet_info, height=250, minsize=35)

        self.top.bind_class('Entry', '<Control-a>', lambda e: e.widget.select_range(0, tk.END))
        self.packet_info.tree.bind('<Button-3>', lambda _: self.searchbar.insert('banana'))
        self.packets.tree.bind('<<TreeviewSelect>>', lambda _: self.packet_info.set_packet(self.packets.selected()))

    def pack(self):
        self.packets.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.packet_info.pack()
