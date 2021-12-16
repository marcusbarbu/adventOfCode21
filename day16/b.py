import binascii
import typing
import bitarray
import bitarray.util
from dataclasses import dataclass, field
from typing import Any, List

@dataclass
class LiteralPacket:
    version: int
    op: int
    literal: int

@dataclass
class OperatorPacket:
    version: int
    op: int
    packets: List

def parse_literal_packet(ba, offset):
    start = offset
    done = False
    out = bitarray.bitarray()
    while start < len(ba) and not done:
        cur = ba[start:start+5]
        done = cur[0] == 0
        out += cur[1:]
        start += 5
    return bitarray.util.ba2int(out), start

def parse_operator_packet(ba, offset, t):
    length_id = ba[offset]
    offset+=1
    subpack_len_len = 15 if length_id == 0 else 11
    subpack_len = ba[offset:offset+subpack_len_len]
    offset += subpack_len_len
    packets = []
    if subpack_len_len == 15:
        total_len = bitarray.util.ba2int(subpack_len)
        # print(f'Subpack len: {subpack_len}')
        max_offset = offset + total_len
        while offset < max_offset:
            packet, offset = parse_binary_packet(ba, offset=offset)
            packets.append(packet)
    else:
        num_packets = bitarray.util.ba2int(subpack_len)
        # print(f'Num packets: {num_packets}')
        for _ in range(num_packets):
            packet, offset = parse_binary_packet(ba, offset=offset)
            packets.append(packet)
    return packets, offset


def parse_binary_packet(ba, offset=0, max_offset=0):
    outputs = []
    done = False
    while not done:
        if max_offset == 0:
            done = True
        # print(f'Offset {offset} target {max_offset}')
        v = bitarray.util.ba2int(ba[offset:offset+3])
        offset += 3
        t = bitarray.util.ba2int(ba[offset:offset+3])
        offset += 3
        # print(f'Bin packet {ba} has v {v} t {t}')
        if t == 4:
            # print(f'Parsing literal')
            literal, offset = parse_literal_packet(ba, offset)
            literal = LiteralPacket(v, t, literal)
            # print(f'Literal: {literal}, ends at {offset}')
            # offset += 4 - (offset % 4)
            outputs.append(literal)
        else:
            # print(f'Parsing operator')
            packets, offset = parse_operator_packet(ba, offset, t)
            packet = OperatorPacket(v, t, packets)
            # print(f'Operator {packet}, ends at {offset}')
            outputs.append(packet)
        if max_offset != 0 and not (offset < max_offset):
            done = True
    if len(outputs) == 1:
        return outputs[0], offset
    return outputs, offset

def parse(hex_in):
    binary_in = binascii.unhexlify(hex_in)
    a = bitarray.bitarray()
    a.frombytes(binary_in)
    return parse_binary_packet(a)

def version_sum(outermost_packet):
    print(f'Called version sum on {outermost_packet}')
    s = 0
    if isinstance(outermost_packet, LiteralPacket):
        print(f'Literal has version {outermost_packet.version}')
        return outermost_packet.version
    elif isinstance(outermost_packet, OperatorPacket):
        s += outermost_packet.version
        for packet in outermost_packet.packets:
            s += version_sum(packet)
        print(f'Operator has version sum {s}')
    return s
    

def evaluate_packet(pkt):
    print(f'Called evaluate on {pkt}')
    total = 0
    if isinstance(pkt, LiteralPacket):
        return pkt.literal
    elif isinstance(pkt, OperatorPacket):
        if pkt.op == 0:
            for sub in pkt.packets:
                total += evaluate_packet(sub)
        elif pkt.op == 1:
            total = 1
            for sub in pkt.packets:
                total *= evaluate_packet(sub)
        elif pkt.op == 2:
            options = []
            for sub in pkt.packets:
                options.append(evaluate_packet(sub))
            total = min(options)
        elif pkt.op == 3:
            options = []
            for sub in pkt.packets:
                options.append(evaluate_packet(sub))
            total = max(options)
        elif pkt.op == 5:
            a = evaluate_packet(pkt.packets[0])
            b = evaluate_packet(pkt.packets[1])
            total = 1 if a > b else 0
        elif pkt.op == 6:
            a = evaluate_packet(pkt.packets[0])
            b = evaluate_packet(pkt.packets[1])
            total = 1 if a < b else 0
        elif pkt.op == 7:
            a = evaluate_packet(pkt.packets[0])
            b = evaluate_packet(pkt.packets[1])
            total = 1 if a == b else 0
        else:
            print(f'Packet with op {pkt.op}, wtf.')
    return total

test_a = 'C200B40A82'
test_b = '9C0141080250320F1802104A08'
pkt, offset = parse(test_a)
pkt, offset = parse(test_b)
pkt, offset = parse('CE00C43D881120')
pkt, offset = parse('880086C3E88112')
pkt, offset = parse('04005AC33890')
pkt, offset = parse('D8005AC2A8F0')
pkt, offset = parse('F600BC2D8F')
pkt, offset = parse('9C005AC2F8F0')
pkt, offset = parse(open('input','r').read())

print(evaluate_packet(pkt))