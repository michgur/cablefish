import Tkinter as tk
import tkFileDialog
import ttk


class CaptureMenu(tk.Frame):
    def __init__(self, root, command_new, command_open, command_save, command_stop, command_filter, command_import, command_export):
        tk.Frame.__init__(self, root, bg='#7F7F7F')
        self.root = root
        self.app = root.app
        self.frame = tk.Frame(self, bg='#D9D9D9', height=35)

        def open_cmd():
            filename = tkFileDialog.askopenfilename(title='Open', **self.filedialog_opts)
            if filename:
                self.root.clear_packets()
                command_open(filename)

        def save_cmd():
            filename = tkFileDialog.asksaveasfilename(title='Save As', **self.filedialog_opts)
            if filename: command_save(filename)

        def import_cmd():
            filename = tkFileDialog.askopenfilename(title='Import PCAP Files', **self.filedialog_opts_pcap)
            if filename:
                self.root.clear_packets()
                command_import(filename)

        def export_cmd():
            filename = tkFileDialog.asksaveasfilename(title='Export To PCAP', **self.filedialog_opts_pcap)
            if filename: command_export(filename)

        self.capture = tk.Button(self.frame, takefocus=False, bg='#D9D9D9', relief=tk.FLAT, command=command_new)
        self.capture.icon = tk.PhotoImage(file='new.ppm')
        self.capture.config(image=self.capture.icon)

        self.stop = tk.Button(self.frame, takefocus=False, bg='#D9D9D9', relief=tk.FLAT, command=command_stop)
        self.stop.icon = tk.PhotoImage(file='stop.ppm')
        self.stop.config(image=self.stop.icon)

        self.open = tk.Button(self.frame, takefocus=False, bg='#D9D9D9', command=open_cmd, relief=tk.FLAT)
        self.open.icon = tk.PhotoImage(file='open.ppm')#.subsample(2, 2)
        self.open.config(image=self.open.icon)

        self.save = tk.Button(self.frame, takefocus=False, bg='#D9D9D9', command=save_cmd, relief=tk.FLAT)
        self.save.icon = tk.PhotoImage(file='save.ppm')#.subsample(2, 2)
        self.save.config(image=self.save.icon)

        self.pcap = tk.Button(self.frame, takefocus=False, bg='#D9D9D9', relief=tk.FLAT, command=import_cmd)
        self.pcap.icon = tk.PhotoImage(file='import.ppm')  # .subsample(2, 2)
        self.pcap.config(image=self.pcap.icon)

        self.export = tk.Button(self.frame, takefocus=False, bg='#D9D9D9', relief=tk.FLAT, command=export_cmd)
        self.export.icon = tk.PhotoImage(file='export.ppm')  # .subsample(2, 2)
        self.export.config(image=self.export.icon)

        self.filedialog_opts = {
            'parent': root,
            'filetypes': [('cablefish files', '.cf'), ('all files', '.*')], 'initialdir': 'C:/Users/',
            'defaultextension': '.banana'
        }
        self.filedialog_opts_pcap = {
            'parent': root,
            'filetypes': [('libpcap files', '.pcap'), ('all files', '.*')], 'initialdir': 'C:/Users/',
            'defaultextension': '.banana'
        }

        self.command_filter = command_filter

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

        self.buttons = [self.capture, self.stop, self.open, self.save, self.pcap, self.export]

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

        if callable(self.command_filter): self.command_filter('')

    def apply_search(self, _):
        if not self.search.clear and callable(self.command_filter):
            self.command_filter(self.search.get())

    def focus_in(self, _):
        if not self.search.clear: return
        self.search.clear = False
        self.search.delete(0, tk.END)
        self.search.config(fg='#000000')

    def focus_out(self, _):
        if not self.search.get():
            self.clear_search()
        else:
            self.apply_search(_)

    def pack(self, **kwargs):
        tk.Frame.pack(self, **kwargs)
        self.frame.pack(fill=tk.BOTH, anchor=tk.CENTER, expand=True, pady=(0, 1))
        self.capture.pack(side=tk.LEFT, padx=(6, 3))
        self.stop.pack(side=tk.LEFT, padx=3)
        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=3)

        self.open.pack(side=tk.LEFT, padx=3)
        self.save.pack(side=tk.LEFT, padx=3)
        self.pcap.pack(side=tk.LEFT, padx=3)
        self.export.pack(side=tk.LEFT, padx=3, pady=1)
        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=3)

        self.search.pack(side=tk.LEFT, fill=tk.BOTH, padx=(3, 15), pady=3, expand=True)
        self.apply.pack(side=tk.LEFT, anchor=tk.E)
        self.clear.pack(side=tk.LEFT, anchor=tk.E, expand=False, padx=15)

    def update(self):
        """
        disabled

        r = self.app.packets.running
        s = self.app.packets.saved
        self.stop['state'] = tk.NORMAL if r else tk.DISABLED
        self.export['state'] = tk.NORMAL if r or not s else tk.DISABLED
        self.save['state'] = tk.NORMAL if r or not s else tk.DISABLED
        self.capture['state'] = tk.NORMAL if not r else tk.DISABLED
        self.pcap['state'] = tk.NORMAL if not r else tk.DISABLED
        self.open['state'] = tk.NORMAL if not r else tk.DISABLED
        """
        pass

    def enable(self, *args):
        for i in args:
            self.buttons[i].config(state=tk.NORMAL)

    def disable(self, *args):
        for i in args:
            self.buttons[i].config(state=tk.DISABLED)
