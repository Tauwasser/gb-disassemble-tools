#!/usr/bin/python3
# -*- coding: utf-8 -*-

#z80gbRegs8
REG_A = 0x001
REG_B = 0x002
REG_C = 0x004
REG_D = 0x008
REG_E = 0x010
REG_F = 0x080
REG_H = 0x020
REG_L = 0x040

#z80gbRegs16
REG_AF = REG_A | REG_F
REG_BC = REG_B | REG_C
REG_DE = REG_D | REG_E
REG_HL = REG_H | REG_L
REG_SP = 0x100

#z80gbRegs8Spec
REG_HL_IND = 0x200

#z80gbCondCodes
CC_NONE = 0x00
CC_Z    = 0x01
CC_NZ   = 0x02
CC_C    = 0x04
CC_NC   = 0x08

tbl_r = {
	0: ('b',    REG_B),
	1: ('c',    REG_C),
	2: ('d',    REG_D),
	3: ('e',    REG_E),
	4: ('h',    REG_H),
	5: ('l',    REG_L),
	6: ('[hl]', REG_HL_IND),
	7: ('a',    REG_L),
}

tbl_rp = {
	0: ('bc', REG_BC),
	1: ('de', REG_DE),
	2: ('hl', REG_HL),
	3: ('sp', REG_SP),
}

tbl_rp2 = {
	0: ('bc', REG_BC),
	1: ('de', REG_DE),
	2: ('hl', REG_HL),
	3: ('af', REG_AF),
}

tbl_cc = {
	0: ('nz', CC_NZ),
	1: ('z',  CC_Z),
	2: ('nc', CC_NC),
	3: ('c',  CC_C),
}

tbl_alu = {
	0: ('add'),
	1: ('adc'),
	2: ('sub'),
	3: ('sbc'),
	4: ('and'),
	5: ('xor'),
	6: ('or'),
	7: ('cp'),
}

tbl_rot = {
	0: ('rlc'),
	1: ('rrc'),
	2: ('rl'),
	3: ('rr'),
	4: ('sla'),
	5: ('sra'),
	6: ('swap'),
	7: ('srl'),
}

class Opcode:
	def __init__(self, label):
		self._label = label
	
	def __repr__(self):
		return str(self)
	
	def getLabel(self):
		if self._label:
			return self._label
	
	def getBytes(self):
		return self._bytes
	
	def getOpcode(self):
		return int(self._bytes[0])

class OpcodeXYZ(Opcode):
	def __init__(self, x, y, z, label):
		Opcode.__init__(self, label)
		self._bytes = bytearray([(x << 6) | (y << 3) | (z << 0)])
	
	def __str__(self):
		return "0x%02X (x%d y%d z%d) %s" % (self._bytes[-1], (self._bytes[-1] & 0xC0) >> 6, (self._bytes[-1] & 0x38) >> 3, (self._bytes[-1] & 0x07) >> 0, self._label)

class OpcodeXQPZ(Opcode):
	def __init__(self, x, q, p, z, label):
		Opcode.__init__(self, label)
		self._bytes = bytearray([(x << 6) | (p << 4) | (q << 3) | (z << 0)])
	
	def __str__(self):
		return "0x%02X (x%d q%d p%d z%d) %s" % (self._bytes[-1], (self._bytes[-1] & 0xC0) >> 6, (self._bytes[-1] & 0x30) >> 4, (self._bytes[-1] & 0x08) >> 3, (self._bytes[-1] & 0x07) >> 0, self._label)
	

class OpcodeCB_XYZ(OpcodeXYZ):
	def __init__(self, x, y, z, label):
		OpcodeXYZ.__init__(self, x, y, z, label)
		self._bytes = bytearray([0xCB, self.getBytes()[0]])
	
	def __str__(self):
		return "0xCB " + OpcodeXYZ.__str__(self)
	
	def getCBOpcode(self):
		return int(self._bytes[1])

z80gb_opcodes = [
	# X0 Z0
	[OpcodeXYZ(0, 0, 0, 'nop')],
	[OpcodeXYZ(0, 1, 0, 'ld [u16], sp')],
	[OpcodeXYZ(0, 2, 0, 'stop')],
	[OpcodeXYZ(0, 3, 0, 'jr i8')],
	[OpcodeXYZ(0, y, 0, 'jr ' + tbl_cc[y-4][0] + ', i8') for y in range(4, 8)],
	# X0 Z1
	[OpcodeXQPZ(0, 0, p, 1, 'ld ' + tbl_rp[p][0] + ', u16') for p in range(0, 4)],
	[OpcodeXQPZ(0, 1, p, 1, 'add hl, ' + tbl_rp[p][0]) for p in range(0, 4)],
	# X0 Z2
	[OpcodeXQPZ(0, 0, 0, 2, 'ld [bc], a')],
	[OpcodeXQPZ(0, 0, 1, 2, 'ld [de], a')],
	[OpcodeXQPZ(0, 0, 2, 2, 'ldi [hl], a')],
	[OpcodeXQPZ(0, 0, 3, 2, 'ldd [hl], a')],
	[OpcodeXQPZ(0, 1, 0, 2, 'ld a, [bc]')],
	[OpcodeXQPZ(0, 1, 1, 2, 'ld a, [de]')],
	[OpcodeXQPZ(0, 1, 2, 2, 'ldi a, [hl]')],
	[OpcodeXQPZ(0, 1, 3, 2, 'ldd a, [hl]')],
	# X0 Z3
	[OpcodeXQPZ(0, 0, p, 3, 'inc ' + tbl_rp[p][0]) for p in range(0, 4)],
	[OpcodeXQPZ(0, 1, p, 3, 'dec ' + tbl_rp[p][0]) for p in range(0, 4)],
	# X0 Z4
	[OpcodeXYZ(0, y, 4, 'inc ' + tbl_r[y][0]) for y in range(0, 8)],
	# X0 Z5
	[OpcodeXYZ(0, y, 5, 'dec ' + tbl_r[y][0]) for y in range(0, 8)],
	# X0 Z6
	[OpcodeXYZ(0, y, 6, 'ld ' + tbl_r[y][0] + ', u8') for y in range(0, 8)],
	# X0 Z7
	[OpcodeXYZ(0, 0, 7, 'rlca')],
	[OpcodeXYZ(0, 1, 7, 'rrca')],
	[OpcodeXYZ(0, 2, 7, 'rla')],
	[OpcodeXYZ(0, 3, 7, 'rra')],
	[OpcodeXYZ(0, 4, 7, 'daa')],
	[OpcodeXYZ(0, 5, 7, 'cpl')],
	[OpcodeXYZ(0, 6, 7, 'scf')],
	[OpcodeXYZ(0, 7, 7, 'ccf')],
	# X1
	[OpcodeXYZ(1, y, z, 'ld ' + tbl_r[y][0] + ', ' + tbl_r[z][0]) for y in range(0,8) for z in range(0,8) if not(y == 6 and z == 6)],
	[OpcodeXYZ(1, 6, 6, 'halt')],
	# X2
	[OpcodeXYZ(2, y, z, tbl_alu[y] + ' a, ' + tbl_r[z][0]) for y in range(0,8) for z in range(0,8)],
	# X3 Z0
	[OpcodeXYZ(3, y, 0, 'ret ' + tbl_cc[y][0]) for y in range(0,4)],
	[OpcodeXYZ(3, 4, 0, 'ld [$FF00 + u8], a')],
	[OpcodeXYZ(3, 5, 0, 'add sp, i8')],
	[OpcodeXYZ(3, 6, 0, 'ld a, [$FF00 + u8]')],
	[OpcodeXYZ(3, 7, 0, 'ld hl, sp + i8')],
	# X3 Z1
	[OpcodeXQPZ(3, 0, p, 1, 'pop ' + tbl_rp2[p][0]) for p in range(0,4)],
	[OpcodeXQPZ(3, 1, 0, 1, 'ret')],
	[OpcodeXQPZ(3, 1, 1, 1, 'reti')],
	[OpcodeXQPZ(3, 1, 2, 1, 'jp hl')],
	[OpcodeXQPZ(3, 1, 3, 1, 'ld sp, hl')],
	# X3 Z2
	[OpcodeXYZ(3, y, 2, 'jp ' + tbl_cc[y][0] + ', u16') for y in range(0,4)],
	[OpcodeXYZ(3, 4, 2, 'ld [$FF00 + c], a')],
	[OpcodeXYZ(3, 5, 2, 'ld [u16], a')],
	[OpcodeXYZ(3, 6, 2, 'ld a, [$FF00 + c]')],
	[OpcodeXYZ(3, 7, 2, 'ld a, [u16]')],
	# X3 Z3 Y0
	[OpcodeXYZ(3, 0, 3, 'jp u16')],
	# X3 Z3 Y1 CB-prefix
	[OpcodeCB_XYZ(0, y, z, tbl_rot[y] + ' ' + tbl_r[z][0]) for y in range(0,8) for z in range(0,8)],
	[OpcodeCB_XYZ(1, y, z, 'bit {0:d}, '.format(y) + tbl_r[z][0]) for y in range(0,8) for z in range(0,8)],
	[OpcodeCB_XYZ(2, y, z, 'res {0:d}, '.format(y) + tbl_r[z][0]) for y in range(0,8) for z in range(0,8)],
	[OpcodeCB_XYZ(3, y, z, 'set {0:d}, '.format(y) + tbl_r[z][0]) for y in range(0,8) for z in range(0,8)],
	# X3 Z3 Y2..5 N/A
	# X3 Z3 Y6..7
	[OpcodeXYZ(3, 6, 3, 'di')],
	[OpcodeXYZ(3, 7, 3, 'ei')],
	# X3 Z4 Y0..3
	[OpcodeXYZ(3, y, 4, 'call ' + tbl_cc[y][0] + ', u16') for y in range(0,4)],
	# X3 Z4 Y4..7 N/A
	# X3 Z5
	[OpcodeXQPZ(3, 0, p, 5, 'push ' + tbl_rp2[p][0]) for p in range(0,4)],
	[OpcodeXQPZ(3, 1, 0, 5, 'call u16')],
	# X3 Z5 Q1 P1..3 DD, ED, FD prefixes N/A
	# X3 Z6
	[OpcodeXYZ(3, y, 6, tbl_alu[y] + ' a, u8') for y in range(0,8)],
	# X3 Z7
	[OpcodeXYZ(3, y, 7, 'rst ${0:02X}'.format(y << 3)) for y in range(0,8)],
]

z80_opcode_dict = {}
z80_CBOpcode_dict = {}

z80gb_opcodes_flat = [op for sublist in z80gb_opcodes for op in sublist]

for op in z80gb_opcodes_flat:
	if op.getOpcode() != 0xCB:
		z80_opcode_dict[op.getOpcode()] = op
	else:
		z80_CBOpcode_dict[op.getCBOpcode()] = op

file = "output.txt"

f = open(file, "w");

for k, v in z80_opcode_dict.items():
	f.write("0x{0:02X}: {1:s}\n".format(k, v.getLabel()))

for k, v in z80_CBOpcode_dict.items():
	f.write("0xCB 0x{0:02X}: {1:s}\n".format(k, v.getLabel()))

f.close()