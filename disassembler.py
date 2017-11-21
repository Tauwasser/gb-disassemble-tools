# -*- coding: utf-8 -*-

class Disassembler:
    def __init__(self, infile, outfile, mapper, instr):
        self._infile = infile
        self._outfile = outfile
        self._mapper = mapper
        self._instr = instr
        self._rom = bytes()
        # read the input file in one go
        with open(infile, 'rb') as fin:
            self._rom = fin.read()
    
    def disassemble(self, address, **mapper_kwargs):
        
        self._mapper.setup(**mapper_kwargs)
        
        mapper = self._mapper
        rom = self._rom
        prefixes = self._instr['prefixes']
        instr = self._instr['instructions']
        infile = self._infile
        outfile = self._outfile
        
        addr = address
        data = bytes()
        needed = 1
        
        with open(self._outfile, 'w') as fout:
            
            fin.seek(addr)
            while (True):
                # Read a big chunk
                data = selffin.read(0x4000)
                
                if (needed > len(data)):
                    break
                
                while (True):
                    length = 1
                    if data[0] in prefixes:
                        length = prefixes[data[0]]
                    
                    if data[:length] in instr:
                        pass
                    else:
                        # consume one byte
                        fout.write('db ${0:02x}\n'.format(data[0]))
                        data = data[1:]
                    
                    if (needed > len(data)):
                        break
         