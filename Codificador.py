
arquivo = 'tiposalto'
##arquivo = input('Informe o nome do arquivo ')
REGISTRADORES = {
    '$zero': '00000',
    '$v0': '00010',
    '$v1': '00011',
    '$a0': '00100',
    '$a1': '00101',
    '$a2': '00110',
    '$a3': '00111',
    '$t0': '01000',
    '$t1': '01001',
    '$t2': '01010',
    '$t3': '01011',
    '$t4': '01100',
    '$t5': '01101',
    '$t6': '01110',
    '$t7': '01111',
    '$s0': '10000',
    '$s1': '10001',
    '$s2': '10010',
    '$s3': '10011',
    '$s4': '10100',
    '$s5': '10101',
    '$s6': '10110',
    '$s7': '10111',
    '$t8': '11000',
    '$t9': '11001',
    '$gp': '11100',
    '$sp': '11101',
    '$fp': '11110',
    '$ra': '11111'
}
INSTRUCTIONS = {
    'xor': '100110',
    'addiu': '001001',
    'andi': '001100',
    'addu': '100001',
    'lw': '100011',
    'sw': '101011',
    'beq': '000100',
    'bne': '000101',
    'slt': '101010',
    'j': '000010',
    'sll': '000000',
    'srl': '000010'
}

""" 
To convert binary string to hexadecimal string, we don't need any external libraries. Use formatted string literals (known as f-strings). This feature was added in python 3.6 (PEP 498)

>>> bs = '0000010010001101'
>>> hexs = f'{int(bs, 2):X}'
>>> print(hexs)
>>> '48D'
If you want hexadecimal strings in small-case, use small "x" as follows

f'{int(bs, 2):x}'
Where bs inside f-string is a variable which contains binary strings assigned prior

f-strings are lost more useful and effective. They are not being used at their full potential. """

def codificarTipoR(comando, registradores):
    if comando != 'sll' and comando != 'srl':
        numBinario = '000000' + REGISTRADORES.get(registradores[1]) + REGISTRADORES.get(registradores[2]) + REGISTRADORES.get(registradores[0]) + '00000' + INSTRUCTIONS.get(comando)
        hexs = f'{int(numBinario, 2):X}'
        hexs = completarNumero(hexs, 8)
        return hexs
    else:
        parteShift = bin(int(registradores[2]))[2:]
        parteShift = completarNumero(parteShift, 5)
        numBinario = '00000000000' + REGISTRADORES.get(registradores[1]) + REGISTRADORES.get(registradores[0]) + parteShift + '000000'
        hexs = f'{int(numBinario, 2):X}'
        hexs = completarNumero(hexs, 8)
        return hexs

def codificarTipoI(comando, resto_comando):
    parteImediata = str(bin(int(resto_comando[2])))[2:]
    parteImediata = completarNumero(parteImediata, 16)
    numBinario = INSTRUCTIONS.get(comando) + REGISTRADORES.get(resto_comando[1]) + REGISTRADORES.get(resto_comando[0]) + parteImediata
    hexs = f'{int(numBinario, 2):X}'
    hexs = completarNumero(hexs, 8)
    return hexs

def codificarTipoJ(endereco):
    numBinario = INSTRUCTIONS.get('j')  +  completarNumero(bin(int(completarNumero(hex(int('00400000', 16)+endereco)[2:], 8)))[2:], 32)[5:31]
    print(hex(int('00400000', 16)+endereco)[2:])
    hexs = f'{int(numBinario, 2):X}'
    hexs = completarNumero(hexs, 8)
    return hexs

def completarNumero(numero, tamanho):
    for i in range(len(str(numero)), tamanho):
        numero = '0' + numero
    return numero

#Le o arquivo
with open('EntradaDeDados/' + arquivo + '.asm') as f:
    comandos_do_programa = []
    codigoMain = False
    lista = []
    for linhas in f.readlines():
        termos = linhas.split()
        for termo in termos:
            termo = termo.lower()
            if termo == '.data':
                codigoMain = False
            elif termo == 'main:':
                codigoMain = True
            elif codigoMain is True:
                lista.append(termo)
        if codigoMain is True and lista != []:
            comandos_do_programa.append(lista)
            lista = []

    for index in range(0, len(comandos_do_programa)):
        comando = comandos_do_programa[index][0]
        if (comando == 'addu' or comando == 'xor' or comando == 'sll' or comando == 'srl' or comando == 'slt'):
            registradores = str(comandos_do_programa[index][1]).split(",")
            print(comando)
            print(registradores)
            print(codificarTipoR(comando, registradores))

        elif (comando == 'addiu' or comando == 'andi'):
            resto_comando = str(comandos_do_programa[index][1]).split(",")
            print(comando)
            print(resto_comando)
            print(codificarTipoI(comando, resto_comando))

        elif (comando == 'lw' or comando == 'sw'):
            resto_comando = str(comandos_do_programa[index][1]).split(",")
            print(comando)
            print(resto_comando)
            print(codificarTipoI(comando, [resto_comando[0], resto_comando[1][2:5],resto_comando[1][0]]))
        
        elif(comando == 'beq' or comando == 'bne'):
            contador = 0
            print(comando)
            resto_comando = str(comandos_do_programa[index][1]).split(",")
            print(resto_comando)
            for i in range(index+1, len(comandos_do_programa)-1):
                if((resto_comando[2] + ':') == str(comandos_do_programa[i][0]).split(",")[0]):
                    break
                contador +=1
            print(codificarTipoI(comando, [resto_comando[0], resto_comando[1], contador]))
        elif(comando == 'j'):
            contador = 0
            print(comando)
            resto_comando = str(comandos_do_programa[index][1]).split(",")
            print(resto_comando)
            for i in range(index, len(comandos_do_programa)-1):
                if((resto_comando[0] + ':') == str(comandos_do_programa[i][0]).split(",")[0]):
                    break
                contador +=1
            print(codificarTipoJ((contador+index)*4))



        



    #Regulares: OK!
    #Iregulares: beq, bne, 
    #Tipo J: J
    #Shift: OK!