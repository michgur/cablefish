def tcp_options_size(packet):
    return (packet.data_offset - 5) * 4


def dns_q_count(packet):
    return packet.question_count


def dns_rr_count(packet):
    return packet.ans_rr_count + packet.auth_rr_count + packet.add_rr_count


def dns_res_size(packet):
    return packet.res_size


def udp_payload(payload):
    packet = payload.args['parent']
    if len(packet.conversation) > 1:
        return packet.conversation[0].payload

    for i in ['dst', 'src']:
        key = payload.args['key']
        value = getattr(packet, i)
        for p in packet.parser.children:
            if p.args[key] == value: return p
    return None
