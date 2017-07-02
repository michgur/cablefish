def basicstr(x):
    return str(x)


def mactostr(addr):
    return ':'.join('%02x' % ord(i) for i in addr)


def inttohexstr(i):
    return '0x%02x' % i


def iptostr(addr):
    return '.'.join(str(ord(i)) for i in addr)


def strtohexstr(s):
    return ' '.join('%02x' % ord(c) for c in s)


def dnsres_choosestr(packet):
    if packet.type == 1: return iptostr
    if packet.type == 5: return str
    return strtohexstr


def listtostr(l):
    if not len(l): return ''
    return '[\n' + ',\n'.join('\t' + repr(i).replace('\n', '\n\t') for i in l) + '\n]'
