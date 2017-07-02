from threading import Thread
from cf import protocols
from cf.packet_manager import PacketManager
from gui.gui import CFGUI


class CableFish(object):
    """The CableFish application."""
    def __init__(self):
        """
        Create and run a new application.
        """
        self.protocols = protocols.import_from('./protocols/')
        self.packets = PacketManager(self)
        self.sniffer = None
        self.session_running = False

        self.root = CFGUI(self)
        self.root.mainloop()

    def new_session(self, action):
        """
        Start a new capture session on a Thread.

        :type action: function
        :param action: The function to execute on the Thread.
        """
        if self.sniffer and self.sniffer.isAlive():
            self.session_running = False
            self.packets.running = False
            while self.sniffer.isAlive(): pass
        self.sniffer = Thread(target=action)
        self.sniffer.start()
        self.session_running = True
        self.root.capture_menu.update()
        self.root.after(1, lambda: self.root.update_packets(self.packets.queue))

    def update_filter(self, filter):
        """
        Change the display filter.

        :type filter: str
        :param filter: The new display filter
        """
        self.packets.set_filter(filter)
        self.root.clear_packets()

    def quit(self):
        """
        Ask user to save the capture, then close everything and quit safely.
        """
        if self.packets.saved or not self.packets.packets:
            self.root.quit()
            self.packets.stop()
            return
        self.root.asksave()
        self.packets.stop()

# run the application
if __name__ == '__main__': app = CableFish()
