
## Tipo de operacion (luego se terminan de añadir)
Ropcode = "0110011"

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

## archivos Default
fileName = "sum.s"
outputfile= "bininst.txt"
#Definir los archivos
data = open(fileName,"r",encoding="utf-8")
out = open(outputfile,"w")

dataOut = "" # definicion de archivo de salida con linea en blanco
for line in data:
    asbInst = line.lower().replace(","," ").replace("\n","").replace("\t","").split(" ")
    inst,regD,reg1,reg2 = INST[asbInst[0]],asbInst[1],asbInst[2],asbInst[3] 
    #1,2,4 registers
    inst_aux = [ inst[i] for i in range(6)]
    inst_aux[1],inst_aux[2],inst_aux[4] = binner(reg2),binner(reg1),binner(regD)        
    inst_traslated = inst_aux[0]+inst_aux[1]+inst_aux[2]+inst_aux[3]+inst_aux[4]+inst_aux[5]
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
## Cerrar los archivos
data.close()
out.close()

