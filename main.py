import re

def registers_map(register):
    registers = {
        '$1' : '00001', '$2' : '00010', '$3' : '00011', '$4' : '00100', '$5' : '00101',
        '$6' : '00110', '$7' : '00111', '$8' : '01000', '$9' : '01001', '$10': '01010',
        '$11': '01011', '$12': '01100', '$13': '01101', '$14': '01110', '$15': '01111',
        '$16': '10000', '$17': '10001', '$18': '10010', '$19': '10011', '$20': '10100',
        '$21': '10101', '$22': '10110', '$23': '10111', '$24': '11000', '$25': '11001',
        '$26': '11010', '$27': '11011', '$28': '11100', '$29': '11101', '$30': '11110',
        '$31': '11111'
    }
    return registers.get(register, '00000') 

def intr_type(instruction):
    if instruction in ['add', 'sub', 'and', 'or', 'slt']:
        return 'R'
    elif instruction in ['lw', 'sw']:
        return 'I'
    elif instruction in ['andi', 'addi']:
        return 'II'
    elif instruction in ['j']:
        return 'J'
    else:
        return 'U'

def fun_codes(instr):
    fun_codes = {
        'add': '100000',
        'sub': '100010',
        'and': '100100',
        'or' : '100101',
        
        'lw' : '100011',
        'sw' : '101011',
        'andi': '001100',
        'addi': '001000'
    }
    return fun_codes.get(instr, '00000')

def r_type(instr): #add $0, $1, $2 | opcode	$rs	$rt	$rd	shamt	funct
    intsr_parts = instr.split(' ')
    opcode = '000000' 
    rs = registers_map(intsr_parts[2].replace(',', '').strip())
    rt = registers_map(intsr_parts[3].replace(',', '').strip())
    rd = registers_map(intsr_parts[1].replace(',', '').strip())
    # print("rd", rd, "rs", rs, "rt", rt)
    # print(intsr_parts[0], intsr_parts[1], intsr_parts[2], intsr_parts[3])
    funct = fun_codes(intsr_parts[0])

    b_instr = opcode + rs + rt + rd + '00000' + funct
    return b_instr


def i_type_helper(instr):
    pattern = r'(lw|sw)\s+\$([a-zA-Z0-9]+),\s*(-?\d+)\(\$([a-zA-Z0-9]+)\)'
    match = re.match(pattern, instr)
    
    if match:
        opcode = '100011' if match.group(1) == 'lw' else '101011'
        rt  = format(int(match.group(2).replace('s', '')), '05b')
        imm = format(int(match.group(3)), '016b')
        rs  = format(int(match.group(4).replace('s', '')), '05b')
        return opcode, rs, rt, imm
    else:
        raise ValueError("Invalid lw/sw instruction format")

def i_type(instr):
    opcode, rt, rs, imm = i_type_helper(instr)
    b_instr = opcode + rs + rt + imm
    return b_instr

def ii_type(instr):
    #andi $s14, $s15, 10
    intsr_parts = instr.split(' ')
    opcode = fun_codes(intsr_parts[0])
    rt = registers_map(intsr_parts[1].replace(',', '').strip())
    rs = registers_map(intsr_parts[2].replace(',', '').strip())
    print("rt ", rt, "rs ", rs, "opcode ", opcode)
    imm = format(int(intsr_parts[3]), '016b')
    b_instr = opcode + rs + rt + imm
    return b_instr

def to_hex(binary_str):
    if len(binary_str) % 4 != 0:
        raise ValueError("Binary string length must be a multiple of 4")
    hex_str = ""

    for i in range(0, len(binary_str), 4):
        chunk = binary_str[i:i+4]
        hex_digit = hex(int(chunk, 2))[2:]
        hex_str += hex_digit
        if (i + 4) % 8 == 0:
            hex_str += " "

    return hex_str

if __name__ == "__main__":

    counter = 0xfc00

    try:
        f = open("test.asm", "r")
        f_bin = open("./intr_mem.bin", "w")
        f_hex = open("./intr_mem.hex", "w")
        lines = f.readlines()
    except: 
        print("Error reading file")        
    
    for line in lines:
        if line.strip() == "":
            continue
        elif line.startswith("#"):
            continue
        else:
            intr_t = intr_type(line.split(' ')[0]) # R, I, II add $1 $2 $3
            if intr_t == 'R':
                binary_instr = r_type(line)
                print(hex(counter) , " : Instr: "+str(line)+" "+str(binary_instr)+"  OK")
                counter += 4
                f_bin.write(binary_instr+'\n')
                f_hex.write(to_hex(binary_instr)+'\n')
            elif intr_t == 'I':
                binary_instr = i_type(line)
                print("Instr: "+str(line)+" "+str(binary_instr)+"  OK")
                f_bin.write(binary_instr+'\n')
                f_hex.write(to_hex(binary_instr)+'\n')
            elif intr_t == 'II':                #Andi and addi
                binary_instr = ii_type(line)
                print("Instr: "+str(line)+" "+str(binary_instr)+"  OK")
                f_bin.write(binary_instr+'\n')
                f_hex.write(to_hex(binary_instr)+'\n')
            else:
                print("Instr: "+str(line)+"  Not supported")
                # f_out.write('\n')
                continue
    f.close()
    f_bin.close()