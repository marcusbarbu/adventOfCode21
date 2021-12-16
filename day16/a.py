import binascii
import typing
import bitarray
import bitarray.util
from dataclasses import dataclass, field
from typing import Any, List

@dataclass
class LiteralPacket:
    version: int
    datatype: int
    literal: int

@dataclass
class OperatorPacket:
    version: int
    datatype: int
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


test_a = 'D2FE28'
test_b = '38006F45291200'
test_c = 'EE00D40C823060'
test_d = 'A0016C880162017C3686B18A3D4780'

apkt, offset = parse(test_a)
bpkt, offset = parse(test_b)
cpkt, offset = parse(test_c)
dpkt, offset = parse(test_d)

print(version_sum(cpkt))
print(version_sum(dpkt))

chal_pkt, offset = parse(open('input','r').read())
print(version_sum(chal_pkt))