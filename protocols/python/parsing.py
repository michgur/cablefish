from math import ceil
import cf.fields


def read_int(data, offset, size):
    return reduce(lambda a, b: a | b, [ord(data[offset + size - 1 - i]) << (i * 8) for i in range(size)])


def parse_str(field, data):
    return data[field.offset:field.offset + field.size]


def parse_int(field, data):
    return read_int(data, field.offset, field.size)


def parse_bitfield(field, data):
    size = field.size
    field.size /= 8.0
    bytesize = int(ceil(float(size) / 8 + field.offset)) - int(field.offset)
    return read_int(data, int(field.offset), bytesize) >> \
           (bytesize * 8 - int(field.offset % 1 * 8) - size) & ((1 << size) - 1)


def parse_flag(field, data):
    offset = field.offset
    field.size = 0.125
    return bool(ord(data[int(offset)]) & (1 << int(7 - (offset % 1 * 8))))


def parse_header(header, data):
    return cf.fields.parse_header(header, data)


def get_payload(payload_dict):
    key = getattr(payload_dict['parent'], payload_dict['key'])
    for p in payload_dict['parent'].parser.children:
        if p[payload_dict['key']] == key: return p


def parse_dnsstr(field, data):
    offset = field.offset
    name, c, size = '', ord(data[offset]), 0
    while c:
        if c & 0xC0:
            t = field.offset
            field.offset = field.parent.parent.offset + (read_int(data, offset, 2) ^ 0xC000)
            name += parse_dnsstr(field, data)
            field.offset = t
            offset += 2
            break
        name += data[offset + 1:offset + 1 + c] + '.'
        offset += c + 1
        c = ord(data[offset])
    else:
        name = name[:-1]
        offset += 1

    field.size = offset - field.offset
    return name


def parse_dnsres(field, data):
    if field.parent.type == 5: return parse_dnsstr(field, data)
    else: return parse_str(field, data)


def parse_list(list, data):
    res, size = [], 0
    for _ in range(list.size):
        value = list.field.parse_main(data, list.offset + size, list.parent)
        res.append(value)
        size += value.size
    list.size = size
    return res
