#!/usr/bin/python3
# -*- coding: utf-8 -*-

from disassembler import *
from mappers import *
from z80gb import *

mapper = SachenMMC2()
instr = {'prefixes': {}, 'instructions': {}}

dis = Disassembler('test.bin', 'test.bin.txt', mapper, instr)

dis.disassemble(0)
