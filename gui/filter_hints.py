import Tkinter as tk
import ttk


class FilterHints(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, bg='#7F7F7F')

        ttk.Style().layout('Filter.Treeview', [
            ('Treeview.entry', {
                'border': '1', 'children':
                    [('Treeview.padding', {
                        'children':
                            [('Treeview.treearea', {'sticky': 'nswe'})], 'sticky': 'nswe'
                    })],
                'sticky': 'nswe'
            })
        ])

        self.frame = tk.Frame(self)
        self.tree = ttk.Treeview(self.frame, show='tree', style='Filter.Treeview')

        # for p in root.app.protocols:
        #     print p

            # fixme

    def pack(self):
        self.frame.pack(fill=tk.BOTH, anchor=tk.CENTER, expand=True, pady=1)
        self.tree.pack(fill=tk.BOTH, expand=True)
