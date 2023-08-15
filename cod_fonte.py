# Dicionário que mapeia os códigos hexadecimais para instruções MIPS
INSTRUCTIONS = {
    'xor': '00',
    'addi': '08',
    'andi': '0c',
    'addu': '21',
    'lw': '23',
    'sw': '2b',
    'beq': '04',
    'bne': '05',
    'slt': '2a',
    'j': '02',
    'sll': '00',
    'srl': '02'
}

def assemble(instruction):
    opcode = instruction.split()[0]
    if opcode in ['addi', 'andi']:  # addi ou andi
        _, rt, rs, immediate = instruction.split()
        opcode_hex = INSTRUCTIONS[opcode]
        rt_hex = format(int(rt[1:]), '02x')
        rs_hex = format(int(rs[1:]), '02x')
        immediate_hex = format(int(immediate), '04x')
        return opcode_hex + rs_hex + rt_hex + immediate_hex
    elif opcode in ['lw', 'sw']:  # lw ou sw
        _, rt, offset_base = instruction.split()
        opcode_hex = INSTRUCTIONS[opcode]
        rt_hex = format(int(rt[1:]), '02x')
        offset, base = offset_base.strip(')').split('(')
        offset_hex = format(int(offset), '04x')
        base_hex = format(int(base[1:]), '02x')
        return opcode_hex + base_hex + rt_hex + offset_hex
    elif opcode in ['beq', 'bne']:  # beq ou bne
        _, rs, rt, offset = instruction.split()
        opcode_hex = INSTRUCTIONS[opcode]
        rs_hex = format(int(rs[1:]), '02x')
        rt_hex = format(int(rt[1:]), '02x')
        offset_hex = format(int(offset), '04x')
        return opcode_hex + rs_hex + rt_hex + offset_hex
    elif opcode == 'j':  # j
        _, target = instruction.split()
        opcode_hex = INSTRUCTIONS[opcode]
        target_hex = format(int(target), '08x')
        return opcode_hex + target_hex
    elif opcode in ['sll', 'srl']:  # sll ou srl
        _, rd, rt, sa = instruction.split()
        opcode_hex = INSTRUCTIONS[opcode]
        rd_hex = format(int(rd[1:]), '02x')
        rt_hex = format(int(rt[1:]), '02x')
        sa_hex = format(int(sa), '02x')
        return opcode_hex + '00' + rt_hex + rd_hex + sa_hex
    else:  # xor, addu ou slt
        _, rd, rs, rt = instruction.split()
        opcode_hex = INSTRUCTIONS[opcode]
        rd_hex = format(int(rd[1:]), '02x')
        rs_hex = format(int(rs[1:]), '02x')
        rt_hex = format(int(rt[1:]), '02x')
        return opcode_hex + rs_hex + rt_hex + rd_hex

def disassemble(hex_code):
    opcode = hex_code[:2]
    if opcode in ['08', '0c']:  # addi ou andi
        rs = hex_code[2:4]
        rt = hex_code[4:6]
        immediate = hex_code[6:]
        return f"{INSTRUCTIONS[opcode]} ${rt}, ${rs}, {immediate}"
    elif opcode in ['23', '2b']:  # lw ou sw
        base = hex_code[2:4]
        rt = hex_code[4:6]
        offset = hex_code[6:]
        return f"{INSTRUCTIONS[opcode]} ${rt}, {offset}(${base})"
    elif opcode in ['04', '05']:  # beq ou bne
        rs = hex_code[2:4]
        rt = hex_code[4:6]
        offset = hex_code[6:]
        return f"{INSTRUCTIONS[opcode]} ${rt}, ${rs}, {offset}"
    elif opcode == '02':  # j, sll ou srl
        if hex_code[6:] == '00':  # sll ou srl
            rd = hex_code[2:4]
            rt = hex_code[4:6]
            sa = hex_code[6:8]
            return f"{INSTRUCTIONS[opcode]} ${rd}, ${rt}, {sa}"
        else:  # j
            target = hex_code[2:]
            return f"{INSTRUCTIONS[opcode]} {target}"
    else:  # xor, addu ou slt
        rd = hex_code[2:4]
        rs = hex_code[4:6]
        rt = hex_code[6:]
        return f"{INSTRUCTIONS[opcode]} ${rd}, ${rs}, ${rt}"


# Função para montar o código
def assemble_code(file_path):
    with open(file_path, 'r') as file:
        assembly_code = file.readlines()

    assembled_code = []
    for line in assembly_code:
        instruction = line.strip()
        if instruction:
            assembled_code.append(assemble(instruction))

    return assembled_code


# Função para desmontar o código
def disassemble_code(file_path):
    with open(file_path, 'r') as file:
        hex_code = file.readlines()

    disassembled_code = []
    for line in hex_code:
        hex_instruction = line.strip()
        if hex_instruction:
            disassembled_code.append(disassemble(hex_instruction))

    return disassembled_code


# Exemplo de uso para montagem
assembly_file = 'codigo.asm'  # Arquivo de entrada com o código assembly
output_file = 'codigo.obj'  # Arquivo de saída com o código objeto em hexadecimal

assembled_code = assemble_code(assembly_file)

with open(output_file, 'w') as file:
    file.write('\n'.join(assembled_code))


# Exemplo de uso para desmontagem
object_file = 'codigo.obj'  # Arquivo de entrada com o código objeto em hexadecimal
output_file = 'codigo.asm'  # Arquivo de saída com o código assembly

disassembled_code = disassemble_code(object_file)

with open(output_file, 'w') as file:
    file.write('\n'.join(disassembled_code))

