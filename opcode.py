# -*- coding: utf-8 -*-
from enum import Enum

class Register:
    def __init__(self, name, id, width):
        self._name = name
        self._id = id
    
    def __repr__(self):
        return 'Register {0:s} <{1:#04x}>'.format(str(self), self._id)
    
    def __str__(self):
        return self._name

class Literal:
    def __init__(self, val, fmt):
        self._val = val
        self._fmt = fmt
    
    def __repr__(self):
        return 'Literal {0:s} <{1:#04x}>'.format(str(self), self._val)
    
    def __str__(self):
        return self._fmt.format(self._val)
    
class ConditionCode:
    def __init__(self, name, id):
        self._name = name
        self._id = id
        
    def __repr__(self):
        return 'Condition Code {0:s} <{1:#02x}>'.format(str(self), self._id)
    
    def __str__(self):
        return self._name
    
class Opcode:
	def __init__(self, operation):
		self._operation = operation
	
	def __repr__(self):
		return str(self)
	
	def getOperation(self):
		if self._operation:
			return self._operation
	
	def getBytes(self):
		return self._bytes
	
	def getOpcode(self):
		return int(self._bytes[0])

class OpArgType(Enum):
    reg = (0, '{!s}',    0)
    lit = (1, '{!s}',    0)
    i8  = (2, '${:02x}', 1)
    u8  = (3, '${:02x}', 1)
    u16 = (4, '${:04x}', 2)
    
    def __init__(self, id, fmt, length):
        self._id = id
        self._fmt = fmt
        self._len = length
    
    def getFormat(self):
        return self._fmt

def printOpArgType(type, val):
    
    if (None == val):
        return str(type.name)
    
    return type.getFormat().format(val)

class Operation:
    def __init__(self, label, ir = [], arg_types = []):
        self._label = label
        self._ir = ir
        # init arguments as tuples of (type, value)
        self._args = []
        
        for t in arg_types:
            
            if (OpArgType == type(t)):
                self._args.append((t, None))
            elif (Register == type(t)):
                self._args.append((OpArgType.reg, t))
            elif (Literal == type(t)):
                self._args.append((OpArgType.lit, t))
            else:
                print('Encountered unknown operand type: {0!r}...').format(t)
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        args = [printOpArgType(t, v) for (t, v) in self._args]
        return self._label.format(*args)
            