import re

pattern_MAC = re.compile('[:-]'.join('[0-9a-fA-F]{1,2}' for _ in range(6)))
pattern_IP = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
pattern_IDENTIFIER = re.compile('(?<!\w)(([a-zA-Z_][a-zA-Z0-9_]*\.)*[a-zA-Z_][a-zA-Z0-9_]*)')


def address_replace(match, split, base):
    return '+'.join('chr(%i)' % int(i, base=base) for i in re.split(split, match.group()))


def ip_replace(match): return address_replace(match, '\.', 10)


def mac_replace(match): return address_replace(match, '[:-]', 16)


def identifier_replace(match):
    m = match.group()
    if m in ['and', 'or', 'not', 'chr']: return m

    return 'self.getattr("%s")' % m


# TODO: check validity of identifiers against the packet structure

def fix_filter(filter):
    """
    Converts a filter given by the user into usable code.

    :type filter: str
    :param filter: The filter.
    :rtype: str
    :return: The fixed filter.
    """
    filter = filter.lower()
    filter = re.sub(pattern_MAC, mac_replace, filter)
    filter = re.sub(pattern_IP, ip_replace, filter)
    return re.sub(pattern_IDENTIFIER, identifier_replace, filter)
