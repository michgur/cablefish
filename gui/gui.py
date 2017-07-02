import Tkinter as tk
import ttk

import save
from capture_menu import CaptureMenu
from filter_hints import FilterHints
from menubar import Menubar
from packets_panel import PacketsPanel


class CFGUI(tk.Tk):
    def __init__(self, app):
        tk.Tk.__init__(self)
        self.app = app
        # widgets are created after mainloop

    def mainloop(self, **kwargs):
        self.window = tk.PanedWindow(self, sashpad=0, sashwidth=4, bd=0, bg='#7F7F7F')

        self.show_hints = False
        self.hints = FilterHints(self)

        self.packets_panel = PacketsPanel(self)
        self.capture_menu = CaptureMenu(self, command_new=lambda: self.app.new_session(self.app.packets.sniff),
                                        command_open=lambda filename: self.app.new_session(
                                                lambda: self.app.packets.open(filename)),
                                        command_save=lambda filename: self.app.new_session(
                                                lambda: self.app.packets.save(filename)),
                                        command_stop=lambda: self.app.new_session(self.app.packets.stop),
                                        command_filter=self.app.update_filter,
                                        command_import=lambda filename: self.app.new_session(
                                            lambda: self.app.packets.import_pcap(filename)),
                                        command_export=lambda filename: self.app.new_session(
                                            lambda: self.app.packets.export_pcap(filename)))

        self.window.add(self.packets_panel, width=700)
        self.packets_panel.searchbar.search.focus_set()
        self.bind_all('<Control-f>', lambda _: self.capture_menu.search.focus())
        # self.menubar = Menubar(self)
        self.capture_menu.disable(1, 3, 5)

        self.pack()
        tk.Tk.mainloop(self, **kwargs)

    def clear_packets(self):
        self.packets_panel.packets.clear()

    def update_packets(self, queue):
        limit = 10
        while not queue.empty() and limit:
            self.packets_panel.packets.add_packet(queue.get())
            limit -= 1
        self.after(100, lambda: self.update_packets(queue))

    def pack(self):
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X)
        # self.menubar.pack(fill=tk.BOTH)
        self.capture_menu.pack(fill=tk.X, side=tk.TOP)
        self.window.pack(fill=tk.BOTH, expand=True)
        self.hints.pack()
        self.packets_panel.pack()

        self.title('Cablefish')
        icon = tk.PhotoImage(file='CF_small.gif')
        self.tk.call('wm', 'iconphoto', self._w, icon)
        self.geometry('1000x600')
        self.protocol('WM_DELETE_WINDOW', self.app.quit)

        self.update()

    def toggle_hints(self):
        self.show_hints = not self.show_hints
        if self.show_hints: self.window.add(self.hints, before=self.packets_panel, width=300)
        else: self.window.remove(self.hints)

    def asksave(self):
        s = save.asktosave(self)
        if s:
            self.app.packets.stop()
            self.app.packets.save(s)
        if s is None: return
        self.quit()
