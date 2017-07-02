from collections import OrderedDict
from datetime import datetime


class Packet(object):
    """
    Represents a captured packet. Contains packet data and protocols.
    """
    def __init__(self, index, ts, data, manager):
        """
        Create a new Packet.

        :type index: int
        :param index: Packet's index in the capture.
        :type ts: int
        :param ts: Timestamp.
        :type data: buffer
        :param data: The raw data of the packet.
        :type manager: PacketManager
        :param manager: The Packet Manager. Used for detecting conversations & general capture info.
        """
        self.layers = []
        self.index = index
        self.raw_data = str(data)
        self.size = 0
        self.ts = ts
        self.time = (datetime.fromtimestamp(ts) - manager.capture_start).total_seconds()
        p = manager.protocols['ethernet']
        res = None

        ###################################################################
        while p:
            self.layers.append(p['id'])
            res = p.parse_main(data, self.size, res)
            setattr(self, p['id'], res)
            self.size += res.size

            if hasattr(res, 'endpoints'):
                self.src, self.dst = res.value['src'], res.value['dst']
                if p['id'] == 'tcp' or p['id'] == 'udp':
                    src, dst = res.endpoints
                    e = frozenset([(src, self.ipv4.src), (dst, self.ipv4.dst)])
                else: e = frozenset(res.endpoints)

                if p['id'] not in manager.conversations:
                    manager.conversations[p['id']] = OrderedDict()
                c = manager.conversations[p['id']]
                if e not in c: c[e] = []
                c[e].append(res)
                res.conversation_id = manager.conversations[p['id']].keys().index(e)
                res.conversation = manager.conversations[p['id']][e]

            p = res.get_payload()
            if isinstance(p, unicode): p = manager.protocols[p]
        ####################################################################

        self.protocol = res.name

    def getattr(self, name):
        """
        Used to access protocols and fields.

        :type name: str
        :param name: The name of the required protocol. To access protocol fields, use: "<protocol-name>.<field-name>"
        :return: The value of the field, or the protocol's Header object.
        """
        t = self
        for i in name.split('.'):
            if not hasattr(t, i): return None
            t = getattr(t, i)
        return t

    def matches(self, filter):
        """
        Check if Packet matches this filter.

        :type filter: str
        :param filter: The filter to check.
        :rtype: bool
        :return: whether the packet matched the filter.
        """
        return eval(filter) if filter else True
