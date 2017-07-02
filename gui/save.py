import Tkinter as tk
import tkFileDialog
import tkMessageBox
import ttk


def asktosave(root):
    s = tkMessageBox.askyesnocancel('Unsaved Packets...',
                                    'Do You Want to Save Your Packets?\n  If You Won\'t, They\'ll be Really Sad',
                                    parent=root)
    if not s: return s  # s can be None (for 'Cancel') or False (for 'No')
    filename = tkFileDialog.asksaveasfilename(title='Save As',
                                              parent=root,
                                              filetypes=[('cablefish files', '.cf'), ('all files', '.*')],
                                              initialdir='C:/Users/',
                                              defaultextension='.cf'
                                              )
    return filename


class SaveDialog(object):
    OK = 'ok'
    SAVE = 'save'
    CANCEL = 'cancel'

    def __new__(cls, master, cmd_ok, cmd_save, cmd_cancel):
        w = tk.Toplevel(master)
        w.master = master
        w.title('Unsaved Packets...')
        w.geometry('360x120+%i+%i' % (master.winfo_rootx() + master.winfo_width() / 2 - 180,
                                      master.winfo_rooty() + master.winfo_height() / 2 - 120))
        w.resizable(False, False)
        icon = tk.PhotoImage(file='../CF_small.gif')
        w.tk.call('wm', 'iconphoto', w._w, icon)
        w.protocol('WM_DELETE_WINDOW', w.destroy)

        CODE = 0

        def ok(_=None):
            w.master.focus_set()
            w.destroy()
            cmd_ok()

        def cancel(_=None):
            w.master.focus_set()
            w.destroy()
            cmd_cancel()

        def save():
            filename = tkFileDialog.asksaveasfilename(title='Save As', **w.filedialog_opts)
            if filename:
                w.master.focus_set()
                w.destroy()
                cmd_save(filename)

        def quit(code):
            master.focus_set()
            w.destroy()

        tk.Label(w, text='If You Don\'t Save, Your Capture Data Will Be Lost.\n   Discard Unsaved Packets?',
                 justify=tk.LEFT).pack(pady=15)
        ttk.Separator(w, orient=tk.HORIZONTAL).pack(fill=tk.X)
        frame = tk.Frame(w, bg='#D9D9D9')
        frame.pack(side=tk.BOTTOM, fill=tk.BOTH)
        tk.Button(frame, text=' Cancel ', command=cancel, bg='#D9D9D9') \
            .pack(anchor=tk.S, side=tk.RIGHT, padx=(2, 4), pady=5)
        tk.Button(frame, text=' Save Packets ', bg='#D9D9D9', command=save) \
            .pack(anchor=tk.S, side=tk.RIGHT, padx=2, pady=5)
        tk.Button(frame, text='  OK  ', bg='#D9D9D9', command=ok) \
            .pack(anchor=tk.S, side=tk.RIGHT, padx=2, pady=5)

        w.focus_set()
        w.grab_set()

        w.filedialog_opts = {
            'parent': master,
            'filetypes': [('cablefish files', '.cf'), ('all files', '.*')], 'initialdir': 'C:/Users/',
            'defaultextension': '.banana'
        }

        master.wait_window(w)
