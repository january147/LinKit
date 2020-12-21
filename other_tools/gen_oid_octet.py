#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Tue Dec 15 09:49:17 2020
# Author: January
# Description: This script is used to convert an oid expressed in string format to asn.1 encoded octet format.

import sys

def convert_oid_unit_num_to_otcet(num):
    oid_bytes_reverse = []
    oid_bytes = []
    mask_7bit = 0x80 - 1
    while True:
        single_byte = num & mask_7bit
        # The oid num shoud be big-endian, but we convert the num to a little-endian oid byte array first
        # and then print it backwards.
        oid_bytes_reverse.append(single_byte)
        num = num >> 7
        if num == 0:
            break
    # the least byte should have a leading 0 bit and all others bytes should have a leading 1 bit
    size = len(oid_bytes_reverse)
    for i in range(1, size):
        oid_bytes.append(oid_bytes_reverse.pop() | 0x80)
    oid_bytes.append(oid_bytes_reverse[0])
    return oid_bytes

def print_hex(data):
    i = 0
    for item in data:
        print("0x%02x "%(item), end="")
        i += 1
        if i % 10 == 0:
            print()
    if i % 10 != 0:
        print()

usage = "gen_oid_otcet [<oid> ... <oid>]"


def convert_oid_string_to_otcet(oid_s):
    oid_s = oid_s.split('.')
    oid = []
    for oid_unit in oid_s:
        oid_unit_bytes = convert_oid_unit_num_to_otcet(int(oid_unit))
        oid.extend(oid_unit_bytes)
    return oid



def main():
    if len(sys.argv) < 2:
        print("######################################")
        print("#        oid number translator       #")
        print("######################################")
        while True:
            try:
                oid_s = input("input an string oid to convert:")
            except:
                print()
                exit(0)
            try:
                print("oid bytes are:")
                print_hex(convert_oid_string_to_otcet(oid_s))
            except:
                print("invalid oid")
    else:
        for oid_s in sys.argv[1:]:
            try:
                print("[%s]:"%(oid_s))
                print_hex(convert_oid_string_to_otcet(oid_s))
            except:
                print("invalid oid")

if __name__ == "__main__":
    main()
