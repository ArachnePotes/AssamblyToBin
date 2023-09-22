''' 
This is a interpreter assitant for assembly code to binary  32bit instrucctions
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
    # pos  1,2,4 registers
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
    # pos  0 IMM 11bits,1 RS1,3 RD
    "addi": ("","","000","",Immopcode),
    "xori" : ("","","100","",Immopcode),
    "ori" : ("","","110","",Immopcode),
    "andi" : ("","","111","",Immopcode),
    "slli" : ("","","001","",Immopcode),
    "srli" : ("","","110","",Immopcode),
    "srai" : ("","","110","",Immopcode),
    "slti" : ("","","010","",Immopcode),
    "sltiu" : ("","","011","",Immopcode),
    # Load Imm,rs1,funct3,rd,op
    "lb": ("","","000","",Lopcode),
    "lh": ("","","001","",Lopcode),
    "lw": ("","","010","",Lopcode),
    "lbu":("","","100","",Lopcode),
    "lhu": ("","","101","",Lopcode),
    # Store imm,rs2,rs1,funct3,imm,op
    "sb": ("","","","000","",Sopcode),
    "sh": ("","","","001","",Sopcode),
    "sw": ("","","","010","",Sopcode),
    # branch imm,rs2,rs1,funct3,imm,op
    "beq": ("","","","000","",Bopcode),
    "bne": ("","","","001","",Bopcode),
    "blt": ("","","","100","",Bopcode),
    "bge": ("","","","101","",Bopcode),
    "bltu":("","","","110","",Bopcode),
    "bgeu":("","","","111","",Bopcode),
    # Especial instructions 
    "lui":  ("","","","",Especialopcode),
    "auipc":("","","","",Especialopcode),
    # sistem instructions
    "ecall" : ("",OSopcode),
    "ebreak": ("",OSopcode),
    # Jumps
    "jal" : ("",Jopcode),
    "jalr" : ("",Jalopcode),
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
}

class MsgError():
    def __init__(self,nameerror,var):
        self.ErrorName = nameerror
        self.vars = var

    def __repr__(self):
        return f" Error {self.ErrorName} with {self.vars} In Translation execution. This Line Will be Depreciated"
    def showError(self):
        print( f" Error {self.ErrorName} with {self.vars} In Translation execution. This Line Will be Depreciated")

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

def CheckImm(ImmValue):
    '''
    convertir el valor inmediato a binario
    '''
    reg_bin = str(bin(ImmValue).replace("b","").zfill(12))
    if len(reg_bin) > 12:
        reg_bin = reg_bin[1::]
    return reg_bin
    

def Rtype(inst,regD,reg1,reg2):
    inst_aux = [ inst[i] for i in range(6)]
    inst_aux[1],inst_aux[2],inst_aux[4] = LexReg(reg2),LexReg(reg1),LexReg(regD)
        
    #inst_traslated = inst_aux[0]+inst_aux[1]+inst_aux[2]+inst_aux[3]+inst_aux[4]+inst_aux[5]
    inst_traslated = ""
    for i in range(6): inst_traslated += inst_aux[i]
    #print(f"Rtype : {inst_traslated}")
    return inst_traslated

def Immtype(inst,regD,reg1,ImmValue):
    '''
    1. Verificar el tamaño de el valor inmedito
    2. convertir los registros a bin
    3. concatenar instruccion
    ("","","000","",Immopcode)
    '''
    if (ImmValue < 4096):
        inst_aux = [ inst[i] for i in range(5)]
        # 0 IMM 11bits,1 RS1,3 RD
        inst_aux[0],inst_aux[1],inst_aux[3] = CheckImm(ImmValue),LexReg(reg1),LexReg(regD)      
        #inst_traslated = inst_aux[0]+inst_aux[1]+inst_aux[2]+inst_aux[3]+inst_aux[4]+inst_aux[5]
        inst_traslated = ""
        for i in range(5): inst_traslated += inst_aux[i]
        #print(f"Immtype : {inst_traslated}")
        return inst_traslated
    else:
        MsgError("Immediate value",ImmValue).showError()
        return ""


def Interpreter(data):
    dataOut= ""
    inst_traslated = ""
    for line in data:
        asbInst = line.lower().replace(","," ").replace("\n","").replace("\t","").split(" ")
        inst,regD,reg1,reg2 = INST[asbInst[0]],asbInst[1],asbInst[2],asbInst[3] 
        #1,2,4 registers
        if (asbInst[0] in ["add","sub" ,"xor" ,"or" ,"and" ,"sll","slr","sra","slt","sltu"]):
            inst_traslated = Rtype(inst,regD,reg1,reg2)
            #dataOut += "\n"
        elif (asbInst[0] in ["addi","xori" ,"ori" ,"andi" ,"slli" ,"srli" ,"srai" ,"slti" ,"sltiu"]):
            imm = "" 
            imm += reg2
            imm = int(imm)
            inst_traslated = Immtype(inst,regD,reg1,imm)
            #print(f"ESTA GONORREA NO APARECE {imm}")
            
        else:
            pass
        dataOut += inst_traslated
        dataOut += "\n"
        # Debug
        
        #print(f"\n\tREGISTROS TRADUCIDOS DEBUG:  {inst_aux[1]} ,{ inst_aux[2]} ,{ inst_aux[4] }")
        print(f"""
                instruccion en ASSAMBLY : {line}
                instruccion : {inst}
                reg destination : {regD}
                reg operator1 : {reg1}
                reg operator2 : {reg2}
                instruccion traducida: {inst_traslated}
                type to write : {type(inst_traslated)}
            """
            )
        
        
    # print(out.write(dataOut),dataOut) # Debug
    # Escritura final
    out.write(dataOut)

    
if __name__ == '__main__':
    import sys
    ## archivos Default
    #fileName = "sum.s"
    #outputfile= "bininst.txt"
    # definicion de archivo de salida con linea en blanco
    
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

