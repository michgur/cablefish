import ast
import pickle
from Queue import Queue
from datetime import datetime
from pcap import pcap
from threading import Lock
from cf.filter import fix_filter
from packet import Packet
import export_pcap


class PacketManager(object):
    """
    Manages captured packets, and keeps track of conversations.
    Used to pass packets to the GUI.
    """

    def __init__(self, app):
        """
        Create a new PacketManager

        :type app: CableFish
        :param app: The application that controls this PacketManager.
        """

        self.app = app
        self.protocols = app.protocols
        self.conversations = {}
        self.capture_start = None

        self.packets = []
        self.queue = Queue()
        self.lock = Lock()
        self.thread = None

        self.filter = ''
        self.filter_valid = True

        self.saved = True
        self.running = False
        # pickle: packets, filter (if valid), capture start

    def add(self, p):
        """
        Add a Packet object to this PacketManager, and queues its display.

        :type p: Packet
        :param p: The Packet
        :rtype: Packet
        :return: The added Packet
        """
        with self.lock:
            self.packets.append(p)
            if p.matches(self.filter):
                self.queue.put(p)
        return p

    def set_filter(self, filter):
        """
        Set the display filter for the Packets.

        :type filter: str
        :param filter: The user-inputted filter
        """
        # Fix the user's input to be usable
        self.filter = fix_filter(filter)
        if self.filter == 'self.getattr("rainbow")':
            self.filter = ''
            self.filter_valid = False
            self.app.root.packets_panel.packets.toggle_rb()

        try:
            # Check if the filter is valid code. If it's not, ignore it.
            ast.parse(self.filter)
        except:
            self.filter_valid = False
            self.filter = ''
        else:
            self.filter_valid = True

        # Only display Packets that match the filter.
        with self.queue.mutex:
            self.queue.queue.clear()
        for p in self.packets:
            if p.matches(self.filter): self.queue.put(p)

    def sniff(self, name=None):
        """
        Sniff network traffic using PCAP, and organize captured data in Packet objects.

        :type name: str
        :param name: The id of the network interface, or the name of the .pcap file (defaults to None).
        """
        if self.packets:
            self.saved = True
            self.clear()
        self.running = True
        self.saved = False
        self.app.root.capture_menu.enable(1)
        self.app.root.capture_menu.disable(0, 2, 3, 4, 5)
        self.capture_start = datetime.now()
        for i, (timestamp, packet) in enumerate(pcap(name=name)):
            if not self.running: return
            self.add(Packet(i, timestamp, packet, self))

    def stop(self):
        """Stop the current capture."""
        self.running = False
        self.app.root.capture_menu.disable(1)
        self.app.root.capture_menu.enable(0, 2, 3, 4, 5)

    def save(self, filename):
        """
        Saves the Packets in a .cf, using Python's pickle format.

        :type filename: str
        :param filename: Name of the .cf file to save the data in.
        """
        self.running = False
        with self.lock:
            pickle.dump(self.packets, open(filename, 'wb'))
            self.saved = True
        print 'saved packets in', filename

    def open(self, filename):
        """
        Open a .cf file and add its content.

        :type filename: str
        :param filename: The name of the .cf file to open.
        :rtype: List[Packet]
        :return: The Packets from the opened .cf file.
        """
        self.app.root.capture_menu.enable(0, 2, 3, 4, 5)
        self.app.root.capture_menu.disable(1)
        if self.packets:
            self.clear()
            self.saved = True
        for p in pickle.load(open(filename, 'rb')): self.add(p)
        return self.packets

    def export_pcap(self, filename):
        """
        Export Packets to a .pcap file.

        :type filename: str
        :param filename: The name of the .pcap file to export data to.
        """
        self.app.root.capture_menu.enable(0)
        export_pcap.generatePCAP(self.packets, filename)

    def import_pcap(self, filename):
        """
        Import Packets from a .pcap file.

        :type filename: str
        :param filename: The name of the .pcap file to import data from.
        """
        try: self.sniff(filename)
        except TypeError: pass  # There's a bug in pypcap's code that raises an Exception for no reason

    def clear(self):
        """
        Delete all Packets in this PacketManager.
        """
        self.packets = []
        self.conversations = {}
        with self.queue.mutex:
            self.queue.queue.clear()
        self.app.root.clear_packets()
