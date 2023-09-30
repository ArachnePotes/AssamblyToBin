archivo = "bininst.txt"
archivo2 = "bininst.full"
inst = "00000000000000000000000000000000\n"
data = open(archivo,"r",encoding="utf-8")
out = open(archivo2,"w")
counter = 0
while counter < 1023:
    out.write(inst)
    counter += 1

## Cerrar los archivos
data.close()
out.close()
