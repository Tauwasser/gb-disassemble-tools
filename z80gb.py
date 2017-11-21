#!/usr/bin/python3
# -*- coding: utf-8 -*-
from opcode import *;

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

RegA = Register('a', REG_A, 1)
RegF = Register('f', REG_F, 1)
RegB = Register('b', REG_B, 1)
RegC = Register('c', REG_C, 1)
RegD = Register('d', REG_D, 1)
RegE = Register('e', REG_E, 1)
RegH = Register('h', REG_H, 1)
RegL = Register('l', REG_L, 1)

RegAF = Register('af', REG_AF, 2)
RegBC = Register('bc', REG_BC, 2)
RegDE = Register('de', REG_DE, 2)
RegHL = Register('hl', REG_HL, 2)
RegSP = Register('sp', REG_SP, 2)
RegHLInd = Register('[hl]', REG_HL_IND, 1)

tbl_r = {
    0: RegB,
    1: RegC,
    2: RegD,
    3: RegE,
    4: RegH,
    5: RegL,
    6: RegHLInd,
    7: RegA,
}

tbl_rp = {
    0: RegBC,
    1: RegDE,
    2: RegHL,
    3: RegSP,
}

tbl_rp2 = {
    0: RegBC,
    1: RegDE,
    2: RegHL,
    3: RegAF,
}

tbl_cc = {
    0: ConditionCode('nz', CC_NZ),
    1: ConditionCode('z',  CC_Z),
    2: ConditionCode('nc', CC_NC),
    3: ConditionCode('c',  CC_C),
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

class OpcodeXYZ(Opcode):
    def __init__(self, x, y, z):
        Opcode.__init__(self)
        self._bytes = bytes([(x << 6) | (y << 3) | (z << 0)])
        self._layout = {'length': 1, 'vals': {'x': (6,8), 'y': (3,6), 'z': (0,3)}}
    
    def __repr__(self):
        return '{0!s} (x{1:d} y{2:d} z{3:d})'.format(
            str(self),
            (self._bytes[-1] & 0xC0) >> 6,
            (self._bytes[-1] & 0x38) >> 3,
            (self._bytes[-1] & 0x07) >> 0
            )

class OpcodeXQPZ(Opcode):
    def __init__(self, x, q, p, z):
        Opcode.__init__(self)
        self._bytes = bytes([(x << 6) | (p << 4) | (q << 3) | (z << 0)])
        self._layout = {'length': 1, 'vals': {'x': (6,8), 'p': (4,6), 'q': (3,4), 'z': (0,3)}}
    
    def __repr__(self):
        return '{0!s} (x{1:d} q{2:d} p{3:d} z{4:d})'.format(
            str(self),
            (self._bytes[-1] & 0xC0) >> 6,
            (self._bytes[-1] & 0x30) >> 4,
            (self._bytes[-1] & 0x08) >> 3,
            (self._bytes[-1] & 0x07) >> 0
            )

class OpcodeCB_XYZ(OpcodeXYZ):
    def __init__(self, x, y, z):
        OpcodeXYZ.__init__(self, x, y, z)
        self._bytes = bytes([0xCB, self.getBytes()[0]])
        self._layout['length'] += 1
        self._layout['vals']['prefix'] = (8, 16)

z80gb_instr_lists = [
    # X0 Z0
    [Instruction(OpcodeXYZ(0, 0, 0), 'nop')],
    #[OpcodeXYZ(0, 1, 0, Operation('ld [{0}], sp', [], [OpArgType.u16, RegSP]))],
    #[OpcodeXYZ(0, 2, 0, Operation('stop'))],
    #[OpcodeXYZ(0, 3, 0, Operation('jr {0}', [], [OpArgType.i8]))],
    #[OpcodeXYZ(0, y, 0, Operation('jr ' + str(tbl_cc[y-4]) + ', {0}', [], [OpArgType.i8])) for y in range(4, 8)],
    ## X0 Z1
    #[OpcodeXQPZ(0, 0, p, 1, Operation('ld {0}, {1}', [], [tbl_rp[p], OpArgType.u16])) for p in range(0, 4)],
    #[OpcodeXQPZ(0, 1, p, 1, Operation('add hl, {1}', [], [RegHL, tbl_rp[p]])) for p in range(0, 4)],
    ## X0 Z2
    #[OpcodeXQPZ(0, 0, 0, 2, Operation('ld [bc], a', [], [RegBC, RegA]))],
    #[OpcodeXQPZ(0, 0, 1, 2, Operation('ld [de], a', [], [RegDE, RegA]))],
    #[OpcodeXQPZ(0, 0, 2, 2, Operation('ldi [hl], a', [], [RegHL, RegA]))],
    #[OpcodeXQPZ(0, 0, 3, 2, Operation('ldd [hl], a', [], [RegHL, RegA]))],
    #[OpcodeXQPZ(0, 1, 0, 2, Operation('ld a, [bc]', [], [RegA, RegBC]))],
    #[OpcodeXQPZ(0, 1, 1, 2, Operation('ld a, [de]', [], [RegA, RegDE]))],
    #[OpcodeXQPZ(0, 1, 2, 2, Operation('ldi a, [hl]', [], [RegA, RegHL]))],
    #[OpcodeXQPZ(0, 1, 3, 2, Operation('ldd a, [hl]', [], [RegA, RegHL]))],
    ## X0 Z3
    #[OpcodeXQPZ(0, 0, p, 3, Operation('inc {0}', [], [tbl_rp[p]])) for p in range(0, 4)],
    #[OpcodeXQPZ(0, 1, p, 3, Operation('dec {0}', [], [tbl_rp[p]])) for p in range(0, 4)],
    ## X0 Z4
    #[OpcodeXYZ(0, y, 4, Operation('inc {0}', [], [tbl_r[y]])) for y in range(0, 8)],
    ## X0 Z5
    #[OpcodeXYZ(0, y, 5, Operation('dec {0}', [], [tbl_r[y]])) for y in range(0, 8)],
    ## X0 Z6
    #[OpcodeXYZ(0, y, 6, Operation('ld {0}, {1}', [], [tbl_r[y], OpArgType.u8])) for y in range(0, 8)],
    ## X0 Z7
    #[OpcodeXYZ(0, 0, 7, Operation('rlca'))],
    #[OpcodeXYZ(0, 1, 7, Operation('rrca'))],
    #[OpcodeXYZ(0, 2, 7, Operation('rla'))],
    #[OpcodeXYZ(0, 3, 7, Operation('rra'))],
    #[OpcodeXYZ(0, 4, 7, Operation('daa'))],
    #[OpcodeXYZ(0, 5, 7, Operation('cpl'))],
    #[OpcodeXYZ(0, 6, 7, Operation('scf'))],
    #[OpcodeXYZ(0, 7, 7, Operation('ccf'))],
    ## X1
    #[OpcodeXYZ(1, y, z, Operation('ld {0}, {1}', [], [tbl_r[y], tbl_r[z]])) for y in range(0,8) for z in range(0,8) if not(y == 6 and z == 6)],
    #[OpcodeXYZ(1, 6, 6, Operation('halt'))],
    ## X2
    #[OpcodeXYZ(2, y, z, Operation(tbl_alu[y] + ' a, {1}', [], [RegA, tbl_r[z]])) for y in range(0,8) for z in range(0,8)],
    ## X3 Z0
    #[OpcodeXYZ(3, y, 0, Operation('ret ' + str(tbl_cc[y]))) for y in range(0,4)],
    #[OpcodeXYZ(3, 4, 0, Operation('ld [$FF00 + {0}], a', [], [OpArgType.u8, RegA]))],
    #[OpcodeXYZ(3, 5, 0, Operation('add sp, {1}', [], [RegSP, OpArgType.i8]))],
    #[OpcodeXYZ(3, 6, 0, Operation('ld a, [$FF00 + {1}]', [], [RegA, OpArgType.u8]))],
    #[OpcodeXYZ(3, 7, 0, Operation('ld hl, sp + {2}', [], [RegHL, RegSP, OpArgType.i8]))],
    ## X3 Z1
    #[OpcodeXQPZ(3, 0, p, 1, Operation('pop {0}', [], [tbl_rp2[p]])) for p in range(0,4)],
    #[OpcodeXQPZ(3, 1, 0, 1, Operation('ret'))],
    #[OpcodeXQPZ(3, 1, 1, 1, Operation('reti'))],
    #[OpcodeXQPZ(3, 1, 2, 1, Operation('jp hl', [], [RegHL]))],
    #[OpcodeXQPZ(3, 1, 3, 1, Operation('ld sp, hl', [], [RegSP, RegHL]))],
    ## X3 Z2
    #[OpcodeXYZ(3, y, 2, Operation('jp ' + str(tbl_cc[y]) + ', {0}', [], [OpArgType.u16])) for y in range(0,4)],
    #[OpcodeXYZ(3, 4, 2, Operation('ld [$FF00 + c], a', [], [RegC, RegA]))],
    #[OpcodeXYZ(3, 5, 2, Operation('ld [{0}], a', [], [OpArgType.u16, RegA]))],
    #[OpcodeXYZ(3, 6, 2, Operation('ld a, [$FF00 + c]', [], [RegA, RegC]))],
    #[OpcodeXYZ(3, 7, 2, Operation('ld a, [{1}]', [], [RegA, OpArgType.u16]))],
    ## X3 Z3 Y0
    #[OpcodeXYZ(3, 0, 3, Operation('jp {0}', [], [OpArgType.u16]))],
    ## X3 Z3 Y1 CB-prefix
    #[OpcodeCB_XYZ(0, y, z, Operation(tbl_rot[y] + ' {0}', [], [tbl_r[z]])) for y in range(0,8) for z in range(0,8)],
    #[OpcodeCB_XYZ(1, y, z, Operation('bit {0}, {1}', [], [Literal(y, '{:d}'), tbl_r[z]])) for y in range(0,8) for z in range(0,8)],
    #[OpcodeCB_XYZ(2, y, z, Operation('res {0}, {1}', [], [Literal(y, '{:d}'), tbl_r[z]])) for y in range(0,8) for z in range(0,8)],
    #[OpcodeCB_XYZ(3, y, z, Operation('set {0}, {1}', [], [Literal(y, '{:d}'), tbl_r[z]])) for y in range(0,8) for z in range(0,8)],
    ## X3 Z3 Y2..5 N/A
    ## X3 Z3 Y6..7
    #[OpcodeXYZ(3, 6, 3, Operation('di'))],
    #[OpcodeXYZ(3, 7, 3, Operation('ei'))],
    ## X3 Z4 Y0..3
    #[OpcodeXYZ(3, y, 4, Operation('call ' + str(tbl_cc[y]) + ', {0}', [], [OpArgType.u16])) for y in range(0,4)],
    ## X3 Z4 Y4..7 N/A
    ## X3 Z5
    #[OpcodeXQPZ(3, 0, p, 5, Operation('push {0}', [], [tbl_rp2[p]])) for p in range(0,4)],
    #[OpcodeXQPZ(3, 1, 0, 5, Operation('call {0}', [], [OpArgType.u16]))],
    ## X3 Z5 Q1 P1..3 DD, ED, FD prefixes N/A
    ## X3 Z6
    #[OpcodeXYZ(3, y, 6, Operation(tbl_alu[y] + ' a, {1}', [], [RegA, OpArgType.u8])) for y in range(0,8)],
    # X3 Z7
    [Instruction(OpcodeXYZ(3, y, 7), 'rst {0}', [Literal(y << 3, '${0:02X}')], [], []) for y in range(0,8)],
]

z80gb_instr = [op for sublist in z80gb_instr_lists for op in sublist]
z80_instr_dict = {i.getOpcode().getBytes(): i for i in z80gb_instr}

z80gb_instr_info = {
    'instructions': z80_instr_dict,
    'prefixes':     {0xCB: 2}
}

def z80gb_dump_instructions(outfile):
    with open(outfile, 'w', newline='\n') as fout:
        for k, v in sorted(z80gb_instr_info['instructions'].items()):
            fout.write('{0!s}: {1!s}\n'.format(v.getOpcode(), v))

z80gb_dump_instructions('output.txt')