from collections import OrderedDict
from math import ceil
import protocols


class Parser(object):
    """
    Used to parse a specific Header or Field from raw packet data.
    """
    def __init__(self, **kwargs):
        """
        Create a new parser.

        :param kwargs: Parsing options
        """
        self.args = kwargs
        functions = {}
        for k in kwargs.keys():
            if k.endswith('_func'):
                functions[k[:-5]] = self.args[k]
                del self.args[k]
        self.args['functions'] = functions

        parents = []
        if 'parent' in self.args:
            parents.append(protocols.protocols[self['parent']])
        elif 'parents' in self.args:
            for p in self.args['parents']:
                parents.append(p)
        for p in parents:
            if not hasattr(p, 'children'):
                setattr(p, 'children', [])
            p.children.append(self)

    # REMOVE THIS POOP ########
    def __getitem__(self, item):
        return self.args[item]

    def __setitem__(self, key, value):
        print key, value
        self.args[key] = value
    ###########################

    def parse_main(self, data, offset, packet):  # TODO: rename
        """
        Parse raw packet data using Parser's arguments.

        :type data: buffer
        :param data: The raw packet data.
        :type offset: int
        :param offset: The offset of the relevant data in the packet.
        :type packet: Packet
        :param packet: The Packet object.
        :rtype: Field|Header
        :return: The parsed data, in a Field object that contains additional info.
        """
        res_dict = self.args.copy()

        if 'functions' in self.args:
            res_dict.pop('functions')
            for f in self.args['functions']:
                res_dict[f] = self.args['functions'][f](packet)

        res_dict['offset'], res_dict['parent'] = offset, packet

        if 'header' in self.args:
            res_dict['parser'] = self
            res = Header(res_dict, data)
            delattr(res, 'header')

            if 'endpoints' in self.args:
                res.endpoints = (getattr(res, 'src'), getattr(res, 'dst'))

        else: res = Field(res_dict, data)

        return res


class Field(object):
    """
    Represents a field of a protocol in the Packet.
    """
    def __init__(self, args, data):
        """
        Create a new Field, using raw data and info from the Parser.
        Hilariously enough, the actual parsing is not done inside Parser (FIX THAT!!!).

        :type args: dict
        :param args: Information about the Field.
        :param data: The raw packet data.
        """
        self.__dict__ = args
        self.value = self.parse(self, data)
        delattr(self, 'parse')

    def __repr__(self):
        """
        Represent the field as str. What this function does changes per Field.

        :return: The textual representation of the Field.
        """
        return self.str(self.value)


class Header(Field):
    """
    Represents the header of a protocol in the Packet.
    """
    def __getattr__(self, item):
        """
        Enables access to the values of this Header's Fields.

        :type item: name
        :param item: The name of the field.
        :return: The value of the field.
        :raise AttributeError: If item is not an attribute of the header or a Field.
        """
        if 'value' in self.__dict__ and item in self.value:
            return self.value[item].value
        raise AttributeError(repr(item))

    def __repr__(self):
        """
        Represent the header as str. Requires an additional function since an f_str is not defined for headers.
        Unused.

        :rtype: str
        :return: The textual representation of the Header and its Fields.
        """
        return '{\n\t%s\n}' % \
        (',\n\t'.join('%s: %s' % (f.name, repr(f).replace('\n', '\n\t')) for f in self.value.values() if repr(f)))

    def get_payload(self):
        """
        Gets the type of this protocol's payload, if found.

        :rtype: str
        :return: The ID of the next protocol in the Packet (if exists).
        """
        if not hasattr(self, 'payload'): return None
        # Convert self.payload from a Parser object to the ID (str) of the payload.
        self.payload.args['parent'] = self
        self.payload = self.payload.args['func'](self.payload)
        return self.payload


def parse_header(header, data):
    """
    Used to parse Headers (or Fields that have Fields of their own (treats them as Headers)).

    :type header: Field
    :param header: The Field object containing the parsing information.
    :type data: buffer
    :param data: The raw packet data.
    :rtype: OrderedDict[str, Field]
    :return: The list of Fields in the Header (can also be accessed using IDs).
    """
    header.value = OrderedDict()
    # Parse all Fields in the Header. f is the current Field's Parser.
    for f in header.header.values():
        # Bit offsets are represented by 0.125 per bit.
        # If the field doesn't support bit offsets, move to the next byte.
        if not f['bit_value']: header.size = int(ceil(header.size))
        # Generate a Field object using f.
        v = f.parse_main(data, header.offset + header.size, header)
        # Put the Field object in the header, and increase its size
        header.value[f['id']] = v
        header.size += v.size
    return header.value
