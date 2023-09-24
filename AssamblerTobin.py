''' 
# This is a interpreter assitant for assembly code to binary  32bit instrucctions
# LazyRiscv32I
|---------------------------------------------|------|
|31 27 26 25 |24 20 |19 15 |14 12 |11 7       |6 0   |     
|funct7      |rs2   |rs1   |funct3|rd         |opcode|R-type
|imm[11:0]          |rs1   |funct3|rd         |opcode|I-type
|imm[11:5]   |rs2   |rs1   |funct3|imm[4:0]   |opcode|S-type
|imm[12|10:5]|rs2   |rs1   |funct3|imm[4:1|11]|opcode|B-type
|imm[31:12]                       |rd         |opcode|U-type
|imm[20|10:1|11|19:12]            |rd         |opcode|J-type
|---------------------------------------------|------|
'''

## Tipo de operacion (luego se terminan de añadir)
Ropcode = "0110011"
Immopcode = "0010011"
Sopcode = "0100011"
Lopcode = "0000011"
Bopcode = "1100011"
Jopcode = "1101111"
Jalopcode = "1100111"
Especialopcode = "0110111" #lui | auipc
OSopcode = "1110011"

'''
Diccionario de instrucciones, con su respectivo orden de operacion
cada key -> token
Arbol de sintaxys -> tupla en orden de instruccion
'''

INST = { 
    # pos  1,2,4 registers DONE
    "add" : ("0000000"," "," ","000"," ",Ropcode),
    "sub" : ("0100000"," "," ","000"," ",Ropcode),
    "xor" : ("0000000"," "," ","001"," ",Ropcode),
    "or" : ("0000000"," "," ","010"," ",Ropcode),
    "and" : ("0000000"," "," ","011"," ",Ropcode),
    "sll": ("0000000"," "," ","100"," ",Ropcode),
    "slr": ("0100000"," "," ","101"," ",Ropcode),
    "sra": ("0000000"," "," ","101"," ",Ropcode),
    "slt": ("0000000"," "," ","110"," ",Ropcode),
    "sltu": ("0000000"," "," ","111"," ",Ropcode),
    # pos  0 IMM 11bits,1 RS1,3 RD DONE
    "addi": ("","","000","",Immopcode),
    "xori" : ("","","100","",Immopcode),
    "ori" : ("","","110","",Immopcode),
    "andi" : ("","","111","",Immopcode),
    "slli" : ("","","001","",Immopcode),
    "srli" : ("","","110","",Immopcode),
    "srai" : ("","","110","",Immopcode),
    "slti" : ("","","010","",Immopcode),
    "sltiu" : ("","","011","",Immopcode),
    # Load Imm,rs1,funct3,rd,op DONE
    "lb": ("","","000","",Lopcode),
    "lh": ("","","001","",Lopcode),
    "lw": ("","","010","",Lopcode),
    "lbu":("","","100","",Lopcode),
    "lhu": ("","","101","",Lopcode),
    # Store imm,rs2,rs1,funct3,imm,op DONE
    "sb": ("","","","000","",Sopcode),
    "sh": ("","","","001","",Sopcode),
    "sw": ("","","","010","",Sopcode),
    # branch imm,rs2,rs1,funct3,imm,op DONE
    "beq": ("","","","000","",Bopcode),
    "bne": ("","","","001","",Bopcode),
    "blt": ("","","","100","",Bopcode),
    "bge": ("","","","101","",Bopcode),
    "bltu":("","","","110","",Bopcode),
    "bgeu":("","","","111","",Bopcode),
    # Especial instructions 
    # imm,rd,op
    "lui":  ("","",Especialopcode),
    "auipc":("","",Especialopcode),
    # sistem instructions
    "ecall" : (0,"","000","",OSopcode),
    "ebreak": (1,"","000","",OSopcode),
    # Jumps
    "jal" : ("","",Jopcode),
    "jalr" : ("","",Jalopcode),
}

alias_dict = {
    "t0": "x5",
    "t1": "x6",
    "t2": "x7",
    "t3": "x28",
    "t4": "x29",
    "t5": "x30",
    "t6": "x31",
    "a0": "x10",
    "a1": "x11",
    "a2": "x12",
    "a3": "x13",
    "a4": "x14",
    "a5": "x15",
    "a6": "x16",
    "a7": "x17",
    "s0": "x8",
    "s1": "x9",
    "s2": "x8",
    "s3": "x8",
    "s4": "x20",
    "s5": "x21",
    "s6": "x22",
    "s7": "x23",
    "s8": "x24",
    "s9": "x25",
    "s10": "x26",
    "s11": "x27",
    "ra": "x1",
    "gp": "x3",
    "sp": "x2",
    "zero":"x0",
}

class MsgError():
    def __init__(self,nameerror,var):
        self.ErrorName = nameerror
        self.vars = var

    def showError(self):
        print(f" Error {self.ErrorName} with {self.vars} In Translation execution.")
        exit(1)
        
def binner(regD):
    '''
    Se eliminan las x de los registros  y se convierte a su valor en binario
    ademas de transformar ese valor a una cadena de 5 bits
    se verifica que la cadena de salida sea de 5 bits para valores de 2 cifras
    esto arregla el bug de que bin(31).zfill(5) -> 011111
    '''
    reg = int(regD.replace("x",""))
    reg_bin = str(bin(reg).replace("b","").zfill(5))
    if len(reg_bin) > 5:
        reg_bin = reg_bin[1::]
    return reg_bin

def LexReg(reg):
    '''
    Esta funcion busca en el diccionario de alias su valor correspondiente
    y retorna el binario de el valor correspondiente
    '''
    if (reg in alias_dict.keys()):
        aux_reg = alias_dict[reg]
    else: aux_reg = reg
    # return_var = binner(aux_reg)
    return binner(aux_reg)

def CheckImm(imm, num_bits):
    """
    Convierte un valor inmediato (imm) en una cadena binaria de longitud num_bits.
    Si el valor inmediato no cabe en el número de bits especificado, se genera un error.
    """
    if 0 <= imm < 2**num_bits:
        # Convierte el valor inmediato en una cadena binaria de longitud num_bits
        imm_bin = bin(imm)[2:].zfill(num_bits)
        return imm_bin
    else:
        MsgError("Immediate value", imm).showError()
        return None
    
def Rtype(inst,regD,reg1,reg2):
    '''
    Convierte una instrucción de tipo R (R-type) en su representación en binario.

    Args:
        inst (tuple): Una tupla que contiene los campos de la instrucción.
        regD (str): El nombre del registro de destino.
        reg1 (str): El nombre del primer registro operando.
        reg2 (str): El nombre del segundo registro operando.

    Returns:
        str: La instrucción de tipo R en su representación en binario.
    '''
    # Crea una copia de la tupla de instrucción
    inst_aux = [ inst[i] for i in range(6)]

    # Asigna los valores de los registros a los campos correspondientes en la copia
    inst_aux[1],inst_aux[2],inst_aux[4] = LexReg(reg2),LexReg(reg1),LexReg(regD)   

    # Concatena los campos para formar la instrucción en binario
    inst_traslated = ""
    for i in range(6): inst_traslated += inst_aux[i]

    # Devuelve la instrucción en binario
    return inst_traslated

def Immtype(inst,regD,reg1,ImmValue):
    '''
    Convierte una instrucción de tipo I (I-type) en su representación en binario.

    Args:
        inst (tuple): Una tupla que contiene los campos de la instrucción.
        regD (str): El nombre del registro de destino.
        reg1 (str): El nombre del registro operando.
        ImmValue (int): El valor inmediato a ser convertido.

    Returns:
        str: La instrucción de tipo I en su representación en binario.
    '''
    if (ImmValue < 4096):

        # Crea una copia de la tupla de instrucción
        inst_aux = [ inst[i] for i in range(5)]

        # Asigna los valores de los registros a los campos correspondientes en la copia
        inst_aux[0],inst_aux[1],inst_aux[3] = CheckImm(ImmValue, 12),LexReg(reg1),LexReg(regD)   

        # Concatena los campos para formar la instrucción en binario
        inst_traslated = ""
        for i in range(5): inst_traslated += inst_aux[i]

        # Devuelve la instrucción en binario
        return inst_traslated
    else:
        # Muestra un error si el valor inmediato es demasiado grande
        MsgError("Immediate value",ImmValue).showError()
        return None

def Stype(inst, reg2, reg1, offset):
    '''
    Convierte una instrucción de tipo S (S-type) en su representación en binario.

    Args:
        inst (tuple): Una tupla que contiene los campos de la instrucción.
        reg2 (str): El nombre del registro rs2.
        reg1 (str): El nombre del registro rs1.
        offset (int): El valor inmediato (offset) a ser convertido.

    Returns:
        str: La instrucción de tipo S en su representación en binario.
    '''
    # Crea una copia de la tupla de instrucción
    inst_aux = [inst[i] for i in range(6)]
    
    # Convierte el valor inmediato (offset) en una cadena binaria de 12 bits usando la función CheckImm
    imm = CheckImm(offset, 12)

    # Asigna los campos de la instrucción en el orden correcto
    inst_aux[0], inst_aux[1], inst_aux[2], inst_aux[4] = imm[5:12] , LexReg(reg2), LexReg(reg1) , imm[0:5]
    
    # Concatena los campos para formar la instrucción en binario
    inst_traslated = ""
    for i in range(6): inst_traslated += inst_aux[i]

    # Devuelve la instrucción en binario
    return inst_traslated

def Jtype(inst, regD, offset):
    '''
    Convierte una instrucción de tipo J (J-type) en su representación en binario.

    Args:
        inst (tuple): Una tupla que contiene los campos de la instrucción.
        regD (str): El nombre del registro de destino.
        offset (int): El valor inmediato (offset) a ser convertido.

    Returns:
        str: La instrucción de tipo J en su representación en binario.
    '''

    # Crea una copia de la tupla de instrucción
    inst_aux = [inst[i] for i in range(3)]

    # Convierte el valor inmediato (offset) en una cadena binaria de 20 bits usando la función CheckImm
    inst_aux[0] = CheckImm(offset, 20)  # 21 bits para offsets de saltos

    # Asigna el registro de destino (rd) a la posición correcta en la instrucción
    inst_aux[1] = LexReg(regD)
    
    # Concatena los campos para formar la instrucción en binario
    inst_traslated = ""
    for i in range(3): inst_traslated += inst_aux[i]
    
    # Devuelve la instrucción en binario
    return inst_traslated

def IJtype(inst, regD, reg1, offset):
    '''
    Convierte una instrucción de tipo I/J (Jal-type) en su representación en binario.

    Args:
        inst (tuple): Una tupla que contiene los campos de la instrucción.
        regD (str): El nombre del registro de destino.
        reg1 (str): El nombre del registro fuente 1.
        offset (int): El valor inmediato (offset) a ser convertido.

    Returns:
        str: La instrucción de tipo I/J en su representación en binario.
    '''
    # Crea una copia de la tupla de instrucción
    inst_aux = [inst[i] for i in range(3)]

    # Convierte el valor inmediato (offset) en una cadena binaria de 22 bits usando la función CheckImm
    # Convierte los nombres de los registros fuente 1 y destino en sus representaciones en binario
    inst_aux[0], inst_aux[1], inst_aux[2] = CheckImm(offset, 22), LexReg(reg1), LexReg(regD)
    
    # Concatena los campos para formar la instrucción en binario
    inst_traslated = ""
    for i in range(3): inst_traslated += inst_aux[i]

    # Devuelve la instrucción en binario como una cadena de caracteres
    return inst_traslated

def Btype(inst, reg1, reg2, offset):
    '''
    Convierte una instrucción de tipo B (Branch-type) en su representación en binario.

    Args:
        inst (tuple): Una tupla que contiene los campos de la instrucción.
        reg1 (str): El nombre del registro fuente 1 (rs1).
        reg2 (str): El nombre del registro fuente 2 (rs2).
        offset (int): El valor inmediato (offset) a ser convertido.

    Returns:
        str: La instrucción de tipo B en su representación en binario.
    '''

    # Crea una copia de la tupla de instrucción
    inst_aux = [inst[i] for i in range(6)]

    # Convierte el valor inmediato (offset) en una cadena binaria de 13 bits usando la función CheckImm
    imm = CheckImm(offset, 13)
    
    # Divide el offset en sus partes relevantes y asigna a los campos correspondientes en la instrucción
    inst_aux[0], inst_aux[1], inst_aux[2],inst_aux[4] = (imm[12] + imm[3:10]), LexReg(reg2), LexReg(reg1) , (imm[0:3] + imm[11])
    
    # Concatena los campos para formar la instrucción en binario
    inst_traslated = ""
    for i in range(6): inst_traslated += inst_aux[i]

    # Devuelve la instrucción en binario como una cadena de caracteres
    return inst_traslated

def LoadType(inst, regD, offset, reg1):
    '''
    Convierte una instrucción de carga (Load-type) en su representación en binario.

    Args:
        inst (tuple): Una tupla que contiene los campos de la instrucción.
        regD (str): El nombre del registro destino (rd).
        offset (int): El valor inmediato (offset) a ser convertido.
        reg1 (str): El nombre del registro fuente 1 (rs1).

    Returns:
        str: La instrucción de carga en su representación en binario.
    '''

    # Crea una copia de la tupla de instrucción
    inst_aux = [inst[i] for i in range(5)]

    # Convierte el valor inmediato (offset) en una cadena binaria de 15 bits usando la función CheckImm
    # Convierte los registros fuente 1 (rs1) y destino (rd) en sus representaciones binarias
    inst_aux[0], inst_aux[1], inst_aux[2] = CheckImm(offset, 15), LexReg(reg1), LexReg(regD) 

    # Concatena los campos para formar la instrucción en binario
    inst_traslated = ""
    for i in range(5): inst_traslated += inst_aux[i]

    # Devuelve la instrucción de carga en binario como una cadena de caracteres
    return inst_traslated

def SpecialType(inst, regD, offset):
    '''
    Convierte una instrucción especial (Special-type) en su representación en binario.

    Args:
        inst (tuple): Una tupla que contiene los campos de la instrucción.
        regD (str): El nombre del registro destino (rd).
        offset (int): El valor inmediato (upimm) a ser convertido.

    Returns:
        str: La instrucción especial en su representación en binario.
    '''

    # Crea una copia de la tupla de instrucción
    inst_aux = [inst[i] for i in range(3)]

    # Convierte el valor inmediato (upimm) en una cadena binaria de 20 bits usando la función CheckImm
    # Convierte el registro destino (rd) en su representación binaria
    inst_aux[0], inst_aux[1] = CheckImm(offset, 20), LexReg(regD) 
    
    # Concatena los campos para formar la instrucción en binario
    inst_traslated = ""
    for i in range(3): inst_traslated += inst_aux[i]

    # Devuelve la instrucción especial en binario como una cadena de caracteres
    return inst_traslated

def OSType(inst, regD):
    '''
    Convierte una instrucción especial (Special-type) en su representación en binario.

    Args:
        inst (tuple): Una tupla que contiene los campos de la instrucción.
        regD (str): El nombre del registro destino (rd).

    Returns:
        str: La instrucción especial en su representación en binario.
    '''
    # Crea una copia de la tupla de instrucción
    inst_aux = [inst[i] for i in range(5)]

    # Convierte el valor inmediato (0) Si es ecall (1) Si es ebreak en una cadena binaria de 12 bits usando la función CheckImm, 
    # Convierte el registro destino (rd) en su representación binaria 
    inst_aux[0], inst_aux[1],inst_aux[3] = CheckImm(inst[0],12),LexReg("zero"),LexReg(regD)

    # Concatena los campos para formar la instrucción en binario
    inst_traslated = ""
    for i in range(5): inst_traslated += inst_aux[i]

    # Devuelve la instrucción especial en binario como una cadena de caracteres
    return inst_traslated

def Interpreter(data):
    # definicion de archivo de salida con linea en blanco
    dataOut= ""
    inst_traslated = ""
    for line in data:
        asbInst = line.lower().replace(",", " ").replace("\n", "").replace("\t", "").replace("(", " ").replace(")", " ").split(" ")
        #1,2,4 registers
        if (asbInst[0] in ["add","sub" ,"xor" ,"or" ,"and" ,"sll","slr","sra","slt","sltu"]):
            inst,regD,reg1,reg2 = INST[asbInst[0]],asbInst[1],asbInst[2],asbInst[3]
            inst_traslated = Rtype(inst,regD,reg1,reg2)
        elif (asbInst[0] in ["addi","xori" ,"ori" ,"andi" ,"slli" ,"srli" ,"srai" ,"slti" ,"sltiu"]):
            inst,regD,reg1,reg2 = INST[asbInst[0]],asbInst[1],asbInst[2],asbInst[3]
            # Avoid Int Literal Trick
            imm = "" 
            imm += reg2
            imm = int(imm)
            inst_traslated = Immtype(inst,regD,reg1,imm)
        elif (asbInst[0] in ["sb","sh","sw"]):
            inst, regD, reg1, offset = INST[asbInst[0]] , asbInst[1], asbInst[3], asbInst[2]  # Parsea el offset como entero
            imm = "" 
            imm += offset
            imm = int(imm)
            reg2 = offset #Debug Propurses
            inst_traslated = Stype(inst, regD, reg1, imm)
        elif (asbInst[0] == "jal"):
            inst, regD, offset = INST[asbInst[0]], asbInst[1], str(len(asbInst[2])) # Parsea el offset como entero
            imm = "" 
            imm += offset
            imm = int(imm)
            reg2 = offset #Debug Propurses
            inst_traslated = Jtype(inst, regD, imm)
        elif (asbInst[0] == "jalr"):
            '''
            Parsea el offset como entero.
            La verdad, supongamos que se lo que estoy haciendo, estamos suponiendo que cada nombre de label tiene un tamaño distinto
            en base al tamaño le estamos asignando un offset.
            Lazy RiscV
            '''
            inst, regD, reg1, offset = INST[asbInst[0]], asbInst[1], asbInst[2], asbInst[3]
            #print(asbInst)
            imm = "" 
            imm += offset
            imm = int(imm)
            reg2 = offset #Debug Propurses
            inst_traslated = IJtype(inst, regD, reg1, imm)
        elif (asbInst[0] in ["beq", "bne", "blt", "bge", "bltu", "bgeu"]):
            inst, reg1, reg2, offset = INST[asbInst[0]], asbInst[1], asbInst[2], str(len(asbInst[3])) 
            imm = "" 
            imm += offset
            imm = int(imm)
            reg2 = offset #Debug Propurses # Parsea el offset como entero
            inst_traslated = Btype(inst, reg1, reg2, imm)
        elif (asbInst[0] in ["lb", "lh", "lw", "lbu", "lhu"]):
            inst, regD, offset, reg1 = INST[asbInst[0]], asbInst[1], asbInst[2], asbInst[3]
            imm = "" 
            imm += offset
            imm = int(imm)
            reg2 = offset #Debug Propurses # Parsea el offset como entero
            inst_traslated = LoadType(inst, regD, imm, reg1)
        elif (asbInst[0] in ["lui", "auipc"]):
            inst, regD, offset = INST[asbInst[0]], asbInst[1], asbInst[2]
            imm = "" 
            imm += offset
            imm = int(imm)
            reg2 = offset #Debug Propurses # Parsea el offset como entero
            inst_traslated = SpecialType(inst, regD, imm)
        elif (asbInst[0] in ["ecall", "ebreak"]):
            inst, regD = INST[asbInst[0]], asbInst[1]
            inst_traslated = OSType(inst, regD)
        else:
            pass
        dataOut += inst_traslated
        dataOut += "\n"
        # Debug
        '''
        #print(f"\n\tREGISTROS TRADUCIDOS DEBUG:  {inst_aux[1]} ,{ inst_aux[2]} ,{ inst_aux[4] }")
        print(f"""
                instruccion en ASSAMBLY : {line}
                instruccion Partida: { asbInst }
                instruccion : {inst}
                reg destination : {regD}
                reg operator1 : {reg1}
                reg operator2 : {reg2}
                instruccion traducida: {inst_traslated}
                type to write : {type(inst_traslated)}
            """
            )
        '''
    # print(out.write(dataOut),dataOut) # Debug
    # Escritura final
    out.write(dataOut)

if __name__ == '__main__':
    import sys
    ## archivos Default
    #fileName = "sum.s"
    #outputfile= "bininst.txt"
    
    if len(sys.argv) != 3:
        print(f"usage: py {sys.argv[0]} assambler_file destination_file ")
        exit(1)
        
    # Se abren los archivos Primero se tiene que cargar los tokens en mem volatil
    data = open(sys.argv[1],"r",encoding="utf-8")
    out = open(sys.argv[2],"w")
    Interpreter(data)

## Cerrar los archivos
data.close()
out.close()