import binascii
import calendar
from datetime import datetime

pcap_global_header = ('D4 C3 B2 A1'
                      '02 00'  # File format major revision (i.e. pcap <2>.4)
                      '04 00'  # File format minor revision (i.e. pcap 2.<4>)
                      '00 00 00 00'
                      '00 00 00 00'
                      'FF FF 00 00'
                      '01 00 00 00')

pcap_packet_header = ('AA 77 9F 47'
                      '90 A2 04 00'
                      'XX XX XX XX'  # Frame Size (little endian)
                      'YY YY YY YY')  # Frame Size (little endian)


def write_header_bytes(bytestring, f):
    f.write(binascii.a2b_hex(''.join(bytestring.split())))


def write_int(i, f):
    hex_str = '%08x' % i
    f.write((hex_str[6:] + hex_str[4:6] + hex_str[2:4] + hex_str[:2]).decode('hex'))


tz_correction = datetime.fromtimestamp(calendar.timegm((1970, 1, 1, 0, 0, 0)))


def generatePCAP(packets, filename):
    """
    Exports packets into a libpcap file.

    :type packets: list[Packet]
    :param packets: The packets to export.
    :type filename: str
    :param filename: The name of the libpcap file.
    """

    f = open(filename, 'wb')
    write_header_bytes(pcap_global_header, f)
    for p in packets:
        time = datetime.fromtimestamp(p.ts)
        write_int((time - tz_correction).total_seconds(), f)
        write_int(time.microsecond, f)
        write_int(len(p.raw_data), f)
        write_int(len(p.raw_data), f)
        f.write(p.raw_data)
