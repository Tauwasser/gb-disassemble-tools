# -*- coding: utf-8 -*-

class SachenMMC2:
    def __init__(self):
        self._bank = 0x01
        self._base = 0x00
        self._mask = 0x00
    
    def setup(self, **kwargs):
        
        if (0 == len(kwargs)):
            return
        
        self._bank = kwargs.get('bank', 0x01)
        self._base = kwargs.get('base', 0x00)
        self._mask = kwargs.get('mask', 0x00)
    
    def write(self, addr, val):
        addr &= 0xe000
        
        if (0x0000 == addr):
            if (0x30 == (self._bank & 0x30)):
                self._base = val
        elif (0x2000 == addr):
            # zero-adjust bank
            self._bank = val if (0x00 != val) else 0x01
        elif (0x4000 == addr):
            if (0x30 == (self._bank & 0x30)):
                self._mask = val
        
    def map(self, u16addr):
        rb = 0x00 if (0x0000 == (u16addr & 0x4000)) else self._bank
        return (((self._base & self._mask) | (rb & ~self._mask)) << 14) | (u16addr & 0x3fff)