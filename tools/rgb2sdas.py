#!/usr/bin/env python3
from pathlib import Path
from optparse import OptionParser
from struct import unpack_from, calcsize

WRAM0 = 0; VRAM = 1; ROMX = 2; ROM0 = 3; HRAM = 4; WRAMX = 5; SRAM = 6; OAM = 7
SYM_LOCAL = 0; SYM_IMPORT = 1; SYM_EXPORT = 2
PATCH_BYTE = 0; PATCH_LE_WORD = 1; PATCH_LE_LONG = 2; PATCH_JR = 3

rpnPlus = 0x00; rpnMinus = 0x01; rpnTimes = 0x02; rpnDiv = 0x03; rpnMod = 0x04; rpnNegate = 0x05; rpnExponent = 0x06; rpnOr = 0x10;
rpnAnd = 0x11; rpnXor = 0x12; rpnComplement = 0x13; rpnBoolAnd = 0x21; rpnBoolOr = 0x22; rpnBoolNeg = 0x23; rpnEqual = 0x30; rpnNotEqual = 0x31;
rpnGreater = 0x32; rpnLess = 0x33; rpnGreaterEqual = 0x34; rpnLessEqual = 0x35; rpnShl = 0x40; rpnShr = 0x41; rpnBankSymbol = 0x50; rpnBankSection = 0x51;
rpnCurrentBank = 0x52; rpnSizeOfSection = 0x53; rpnStartOfSection = 0x54; rpnHramCheck = 0x60; rpnRstCheck = 0x61; rpnInteger = 0x80; rpnSymbol = 0x81

class RGBObject(object):
    def __init__(self, data):
        self.Symbols  = []
        self.Sections = []
        self.Nodes = []

        offset = 0
        self.id, self.rev = unpack_from('<4si', data, offset); offset += calcsize('<4si')
        if (self.id != b'RGB9') or (self.rev != 8): raise Exception("RGBDS Object version mismatch!")

        nSymbols, nSections, nNodes = unpack_from('<iii', data, offset); offset += calcsize('<iii')

        # read Nodes
        for i in range(nNodes):
            parentid, parentlineno, nodetype  = unpack_from('<iiB', data, offset); offset += calcsize('<iiB')
            iter = [];
            name = ''
            if (nodetype != 0):
                name, sz = self.read_null_term(data, offset); offset += sz
            else:
                depth = unpack_from('<i', data, offset)[0]; offset += calcsize('i')
                iter, sz = self.read_array('<i', depth, data, offset); offset += sz

            self.Nodes.append({'ParentID': parentid, 'ParentLineNo': parentlineno, 'NodeType': nodetype, 'Name': name, 'Iter': iter})

        # read Symbols
        for i in range(nSymbols):
            name, sz = self.read_null_term(data, offset); offset += sz
            symtype = unpack_from('B', data, offset)[0]; offset += calcsize('B')
            if ((symtype & 0x7f) != SYM_IMPORT):
                sourcefile, linenum, sectionid, value = unpack_from('<iiii', data, offset); offset += calcsize('<iiii')
                self.Symbols.append({'Id': i, 'Name': name, 'SymType': symtype, 'SourceFile': sourcefile, 'LineNum': linenum, 'SectionId': sectionid, 'Value': value})
            else:
                self.Symbols.append({'Id': i, 'Name': name, 'SymType': symtype})

        # read Sections
        for i in range(nSections):
            name, sz = self.read_null_term(data, offset); offset += sz
            size, secttype, org, bank, align, ofs = unpack_from('<iBiiBi', data, offset); offset += calcsize('<iBiiBi')

            sect = {'Id': i, 'Name': name, 'Size': size, 'SectType': secttype, 'Org': org, 'Bank': bank, 'Align': align, 'Ofs': ofs}
            self.Sections.append(sect)

            if (sect['SectType'] in [ROM0, ROMX]):
                sect['Data'] = data[offset:offset+size]; offset += size
                npatches = unpack_from('<i', data, offset)[0]; offset += calcsize('i')
                sect['Patches'] = patches = []
                for j in range(npatches):
                    sourcefile, linenum, ofs, pcsectionid, pcoffset, patchtype, rpnsize = unpack_from('<iiiiiBi', data, offset); offset += calcsize('<iiiiiBi')
                    rpn = self.decode_rpn(data[offset:offset+rpnsize]); offset += rpnsize
                    patches.append({'SourceFile': sourcefile, 'LineNum': linenum, 'Offset': ofs, 'PCSectionId': pcsectionid, 'PCOffset': pcoffset, 'PatchType': patchtype, 'RPN': rpn})

    def read_null_term(self, data, offset):
        j = 0
        while (data[offset + j] != 0): j += 1
        return (data[offset:offset + j].decode('ansi'), j + 1)

    def read_array(self, fmt, count, data, offset):
        sz = calcsize(fmt)
        res = []
        for j in range(count):
            res.append(unpack_from(fmt, data, offset)); offset += sz
        return (res, sz * count)

    def decode_rpn(self, data):
        result = []
        i = 0
        while (i < len(data)):
            itm = {}
            itm['Tag'] = tag = data[i]; i += 1
            if tag == rpnBankSymbol:
                itm['BankSymbol'], sz = self.read_null_term(data, i); i += sz
            elif tag == rpnBankSection:
                itm['BankSection'], sz = self.read_null_term(data, i); i += sz
            elif tag == rpnSizeOfSection:
                itm['SizeOfSection'], sz = self.read_null_term(data, i); i += sz
            elif tag == rpnStartOfSection:
                itm['StartOfSection'], sz = self.read_null_term(data, i); i += sz
            elif tag == rpnInteger:
                itm['IntValue'] = unpack_from('<i', data, i)[0]; i += calcsize('i')
            elif tag == rpnSymbol:
                itm['SymbolId'] = unpack_from('<i', data, i)[0]; i += calcsize('i')
            result.append(itm)
        return result

    def find_patch(self, section, index):
        for patch in section['Patches']:
            if (patch['Offset'] == index):
                return True, patch
        return False, {}

    def log(self):
        print("ID: {:s} REV: {:d}".format(self.id.decode('ansi'), self.rev))
        print(self.Nodes)
        print(self.Symbols)
        print(self.Sections)



def lo(v): return v & 0xff
def hi(v): return (v >> 8) & 0xff

def main(argv=None):
    parser = OptionParser("Usage: rgb2sdas.py [options] INPUT_FILE_NAME.OBJ")
    parser.add_option("-o", '--out',        dest='outfilename',                                          help='output file name')

    parser.add_option("-b", '--bank',       dest='default_bank',                       default="0",      help='BANK number (default: 0)')
    parser.add_option("-c", '--codeseg',    dest='CODESEG',                            default="_CODE",  help='CODE segment name (default: "_CODE")')
    parser.add_option("-r", '--rename',     dest='rename',                                               help='rename symbol: old=new')
    parser.add_option("-e", '--export-all', dest='export_all',   action="store_true",  default=False,    help='export all symbols')
    parser.add_option("-m", '--target',     dest='target',                             default="sm83",   help='target platform (default: "sm83")')

    (options, args) = parser.parse_args()

    if (len(args) == 0):
        parser.print_help()
        parser.error("Input file name required\n")

    infilename = Path(args[0])

    if (options.outfilename == None):
        outfilename = infilename.with_suffix('.o')
    else:
        outfilename = Path(options.outfilename)

    if (options.rename != None):
        old_sym, new_sym = str(options.rename).split('=')
    else:
        old_sym = new_sym = ''

    with open(str(infilename), mode="rb") as f:
        obj = RGBObject(f.read())

    with open(str(outfilename), "wb") as f:
        idx = 0
        # pass 1: all imports first
        for symbol in obj.Symbols:
            if ((symbol['SymType'] & 0x7f) == SYM_IMPORT):
                symbol['No'] = idx
                idx += 1
            elif ((symbol['SymType'] & 0x7f) == SYM_EXPORT):
                symbol['No'] = -1
                section = obj.Sections[symbol['SectionId']]
                if (section['SectType'] == ROMX):
                    symbol['BankAlias'] = (max(int(options.default_bank), section['Bank']) > 0)
                    symbol['BankValue'] = max(int(options.default_bank), section['Bank'])
                    if (symbol['BankAlias']):
                        idx += 1
            else:
                symbol['No'] = -1

        # pass 2: all other (export local only when forced)
        for symbol in obj.Symbols:
            if ((symbol['SymType'] & 0x7f) == SYM_LOCAL):
                if (options.export_all):
                    symbol['No'] = idx
                    idx += 1
            elif ((symbol['SymType'] & 0x7f) == SYM_IMPORT):
                pass
            elif ((symbol['SymType'] & 0x7f) == SYM_EXPORT):
                if ((len(old_sym) != 0) and (symbol['Name'] == old_sym)):
                    symbol['Name'] = new_sym
                symbol['No'] = idx
                idx += 1
            else:
                raise Exception('Unsupported symbol type: {:d}'.format(symbol['SymType'] & 0x7f))

        # output object header
        f.write(bytes('XL3\n', 'ascii'))
        f.write(bytes('H {:X} areas {:X} global symbols\n'.format(len(obj.Sections), idx), 'ascii'))
        f.write(bytes('M {:s}\n'.format(infilename.name.replace('.', '_')), 'ascii'))
        f.write(bytes('O -m{:s}\n'.format(options.target), 'ascii'))

        # output all imported symbols
        for symbol in obj.Symbols:
            if ((symbol['SymType'] & 0x7f) == SYM_IMPORT):
                f.write(bytes('S {:s} Ref{:06X}\n'.format(symbol['Name'].replace('.', '____'), 0), 'ascii'))
            elif ((symbol['SymType'] & 0x7f) == SYM_EXPORT) and (symbol.setdefault('BankAlias', False)):
                f.write(bytes('S b{:s} Ref{:06X}\n'.format(symbol['Name'].replace('.', '____'), symbol['BankValue']), 'ascii'))

        # output all sections and other symbols
        for section in obj.Sections:
            if (section['Org'] == -1):
                if (section['SectType'] == ROM0):
                    f.write(bytes('A {:s} size {:X} flags 0 addr 0\n'.format(options.CODESEG, section['Size']), 'ascii'));
                elif (section['SectType'] == ROMX):
                    if (int(options.default_bank) == 0):
                        f.write(bytes('A {:s} size {:X} flags 0 addr 0\n'.format(options.CODESEG, section['Size']), 'ascii'));
                    else:
                        f.write(bytes('A _CODE_{:d} size {:X} flags 0 addr 0\n'.format(max(int(options.default_bank), section['Bank']), section['Size']), 'ascii'));
                else:
                    f.write(bytes('A _DATA size {:X} flags 0 addr 0\n'.format(section['Size']), 'ascii'));
            else:
                raise Exception('Absolute sections currently unsupported: {:s}'.format(section['Name']))

            for symbol in obj.Symbols:
                if (symbol['SectionId'] == section['Id']):
                    if (((symbol['SymType'] & 0x7f) != SYM_IMPORT) and (symbol['No'] >= 0)):
                        f.write(bytes('S {:s} Def{:06X}\n'.format(symbol['Name'], symbol['Value']).replace('.', '____'), 'ascii'))


        # convert object itself
        for section in obj.Sections:
            if (section['SectType'] != ROM0) and (section['SectType'] != ROMX):
                continue
            data = section.setdefault('Data', [])
            if (len(data) == 0):
                continue;

            PC = 0
            while PC < len(data):
                write_pos = PC + (section['Org'] if (section['Org'] != -1) else 0)

                res, patch = obj.find_patch(section, PC)
                if (res):
                    RPN = patch['RPN']
                    if (patch['PatchType'] == PATCH_BYTE):
                        if (((len(RPN) == 3) and ((RPN[1]['Tag'] != rpnInteger) or (RPN[2]['Tag'] != rpnAnd))) or
                            ((len(RPN) == 5) and ((RPN[1]['Tag'] != rpnInteger) or (RPN[2]['Tag'] != rpnShr) or (RPN[3]['Tag'] != rpnInteger) or (RPN[4]['Tag'] != rpnAnd))) or
                            (not len(RPN) in [3, 5])):
                            raise Exception('Unsupported RPN expression in byte patch')

                        symbol = obj.Symbols[RPN[0]['SymbolId']]
                        if len(RPN) == 3:
                            f.write(bytes('T {:02X} {:02X} 00 {:02X} {:02X} 00\n'.format(lo(write_pos), hi(write_pos), lo(symbol['Value']), hi(symbol['Value'])), 'ascii'))
                            f.write(bytes('R 00 00 {:02X} {:02X} 09 03 {:02X} {:02X}\n'.format(lo(section['Id']), hi(section['Id']), lo(symbol['SectionId']), hi(symbol['SectionId'])), 'ascii'))
                        elif len(RPN) == 5:
                            f.write(bytes('T {:02X} {:02X} 00 {:02X} {:02X} 00\n'.format(lo(write_pos), hi(write_pos), lo(symbol['Value']), hi(symbol['Value'])), 'ascii'))
                            f.write(bytes('R 00 00 {:02X} {:02X} 89 03 {:02X} {:02X}\n'.format(lo(section['Id']), hi(section['Id']), lo(symbol['SectionId']), hi(symbol['SectionId'])), 'ascii'))
                        PC += 1
                    elif (patch['PatchType'] == PATCH_LE_WORD):
                        if (((len(RPN) == 3) and ((RPN[1]['Tag'] != rpnInteger) or (RPN[2]['Tag'] != rpnPlus))) or
                            (not len(RPN) in [1, 3])):
                            raise Exception('Unsupported RPN expression in word patch')

                        symbol = obj.Symbols[RPN[0]['SymbolId']]
                        value_to_write = symbol['Value']

                        if (RPN[-1]['Tag'] == rpnPlus):
                            value_to_write += RPN[1]['IntValue']

                        if (symbol['SymType'] == SYM_IMPORT):
                            if (symbol['No'] < 0):
                                raise Exception('Trying to reference eliminated symbol');
                            f.write(bytes('T {:02X} {:02X} 00 {:02X} {:02X}\n'.format(lo(write_pos), hi(write_pos), lo(value_to_write), hi(value_to_write)), 'ascii'))
                            f.write(bytes('R 00 00 {:02X} {:02X} 02 03 {:02X} {:02X}\n'.format(lo(section['Id']), hi(section['Id']), lo(symbol['No']), hi(symbol['No'])), 'ascii'))
                        else:
                            f.write(bytes('T {:02X} {:02X} 00 {:02X} {:02X}\n'.format(lo(write_pos), hi(write_pos), lo(value_to_write), hi(value_to_write)), 'ascii'))
                            f.write(bytes('R 00 00 {:02X} {:02X} 00 03 {:02X} {:02X}\n'.format(lo(section['Id']), hi(section['Id']), lo(symbol['SectionId']), hi(symbol['SectionId'])), 'ascii'))
                        PC += 2
                    elif (patch['PatchType'] == PATCH_JR):
                        if (len(RPN) != 1):
                            raise Exception('Unsupported RPN expression in JR patch')

                        symbol = obj.Symbols[RPN[0]['SymbolId']]
                        f.write(bytes('T {:02X} {:02X} 00 {:02X}\n'.format(lo(write_pos), hi(write_pos), symbol['Value'] - PC - 1), 'ascii'))
                        f.write(bytes('R 00 00 {:02X} {:02X}\n'.format(lo(section['Id']), hi(section['Id'])), 'ascii'))
                        PC += 1
                    else:
                        raise Exception('Unsupported patch type: {:d} Section: {:s}'.format(patch['PatchType'], section['Name']))
                else:
                    f.write(bytes('T {:02X} {:02X} 00 {:02X}\n'.format(lo(write_pos), hi(write_pos), data[PC]), 'ascii'))
                    f.write(bytes('R 00 00 {:02X} {:02X}\n'.format(lo(section['Id']), hi(section['Id'])), 'ascii'))
                    PC += 1
    print('RGB2SDAS: object {:s} was successfully converted to {:s}'.format(infilename.name, outfilename.name))

if __name__=='__main__':
    main()