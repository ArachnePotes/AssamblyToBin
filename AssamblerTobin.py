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


}


def binner(regD):
    '''
    Se eliminan las x,t y s (alias) de los registros  y se convierte a su valor en binario
    ademas de transformar ese valor a una cadena de 5 bits
    se verifica que la cadena de salida sea de 5 bits para valores de 2 cifras
    esto arregla el bug de que bin(31).zfill(5) -> 011111
    '''
    reg = int(regD.replace("x","").replace("t","").replace("s",""))
    reg_bin = str(bin(reg).replace("b","").zfill(5))
    if len(reg_bin) > 5:
        reg_bin = reg_bin[1::]
    return reg_bin

def Interpreter(data):
    for line in data:
        asbInst = line.lower().replace(","," ").replace("\n","").replace("\t","").split(" ")
        inst,regD,reg1,reg2 = INST[asbInst[0]],asbInst[1],asbInst[2],asbInst[3] 
        #1,2,4 registers
        inst_aux = [ inst[i] for i in range(6)]
        inst_aux[1],inst_aux[2],inst_aux[4] = binner(reg2),binner(reg1),binner(regD)
        
        #inst_traslated = inst_aux[0]+inst_aux[1]+inst_aux[2]+inst_aux[3]+inst_aux[4]+inst_aux[5]
        inst_traslated = ""
        for i in range(6): inst_traslated += inst_aux[i]
        dataOut += "\n"
        # Debug
        '''
        print(f"""
                instruccion en ASSAMBLY : {line}
                instruccion : {inst}
                reg destination : {inst_aux[4]}
                reg operator1 : {inst_aux[2]}
                reg operator2 : {inst_aux[1]}
                instruccion traducida: {inst_traslated}
                type to write : {type(inst_traslated)}
            """
            )
        '''
        dataOut += inst_traslated
    # print(out.write(dataOut),dataOut) # Debug
    # Escritura final
    out.write(dataOut)

def InterpreterImm(data):
    pass


if __name__ == '__main__':
    import sys
    ## archivos Default
    #fileName = "sum.s"
    #outputfile= "bininst.txt"
    # definicion de archivo de salida con linea en blanco
    dataOut = ""
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

