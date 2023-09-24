# LazyRiscv32I - Asistente de Interpretación de Código Ensamblador a Instrucciones Binarias de 32 bits

LazyRiscv32I es una herramienta que te permite convertir código ensamblador en instrucciones binarias de 32 bits. Facilita la traducción de programas escritos en ensamblador RISC-V a su representación binaria, lo que es útil para ejecutar programas en una arquitectura RISC-V o para simular ejecuciones de programas ensamblados.

## Estructura de Instrucciones

Las instrucciones RISC-V de 32 bits se dividen en varios campos, como se muestra a continuación:

    |---------------------------------------------|------|
    |31 27 26 25 |24 20 |19 15 |14 12 |11 7       |6 0   |     
    |funct7      |rs2   |rs1   |funct3|rd         |opcode|R-type
    |imm[11:0]          |rs1   |funct3|rd         |opcode|I-type
    |imm[11:5]   |rs2   |rs1   |funct3|imm[4:0]   |opcode|S-type
    |imm[12|10:5]|rs2   |rs1   |funct3|imm[4:1|11]|opcode|B-type
    |imm[31:12]                       |rd         |opcode|U-type    
    |imm[20|10:1|11|19:12]            |rd         |opcode|J-type
    |---------------------------------------------|------|


## Tipos de Operaciones

- **R-type**: Instrucciones de tipo R.
- **I-type**: Instrucciones de tipo I.
- **S-type**: Instrucciones de tipo S.
- **B-type**: Instrucciones de tipo B (Branch).
- **U-type**: Instrucciones de tipo U.
- **J-type**: Instrucciones de tipo J.

## Uso

Para utilizar LazyRiscv32I, sigue estos pasos:

1. Asegúrate de tener Python instalado en tu sistema.
2. Ejecuta el programa proporcionando el archivo de código ensamblador de entrada y el archivo de salida donde deseas que se almacenen las instrucciones binarias. Puedes ejecutarlo de la siguiente manera:

        python lazy_riscv32i.py input.s output.txt


Donde `input.s` es el archivo de código ensamblador de entrada y `output.txt` es el archivo de salida donde se almacenarán las instrucciones binarias.

3. LazyRiscv32I analizará el código ensamblador de entrada, traducirá las instrucciones a su representación binaria y las almacenará en el archivo de salida.

## Ejemplo de Código Ensamblador de Entrada

A continuación, se muestra un ejemplo de código ensamblador de entrada:

    sub x1,x2,x3
    add t1,t2,t3
    add s1,s2,s3
    add a1,a2,a3
    addi x1,x2,5
    addi x1,x2,25
    addi x1,x2,15
    sw x1,4095(x2)
    jal x1,label
    jalr x5,x6,4095
    beq x0,x0,hola
    bne x1,x2,jajaxd
    lw a0,25(x5)
    lh a7,15(x7) 
    lb a3,5(x9)
    lui x25,56
    auipc x31,25
    ecall x0
    ebreak x0


## Ejemplo de Salida

La salida generada por LazyRiscv32I contendrá las instrucciones binarias correspondientes a las instrucciones de entrada. A continuación, se muestra un ejemplo de salida:

    01000000001100010000000010110011
    00000001110000111000001100110011
    00000000100001000000010010110011
    00000000110101100000010110110011
    00000000010100010000000010010011
    00000001100100010000000010010011
    00000000111100010000000010010011
    11111110000100010010111110100011
    00000000000000000101000011101111
    00000000001111111111110011000101
    00000000001000000000000001100011
    00000000001100000100100011100011
    00000000001100100101010100000011
    00000000000111100111100010000011
    00000000000010101001011010000011
    00000000000000111000110010110111
    00000000000000011001111110110111
    00000000000000000000000001110011
    00000000000100000000000001110011
