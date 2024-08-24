from funciones import *

with open("codigo.txt", "r") as archivo:
    numero_linea = 0
    for linea in archivo:
        revision1 = False
        revision2 = False
        numero_linea += 1 
        linea = linea.strip()
        j = -1
        for condcional in tipos_cond:
            j += 1
            match = condcional.fullmatch(linea)
            if match:
                revision1 = True  
                coincidencias = match.groups()
               
                if j == 0:
                    if len(continuacion)>0:
                        if continuacion[-1] == True and bloque_if[-1] == False:
                            ignorar_if +=2
                            break
                    estado, detalle = ejec_if(coincidencias[0])
                    
                elif j == 1:
                    if ignorar_if > 0:
                        ignorar_if -= 1
                        break
                    estado, detalle = ejec_if_else()
                
                elif j == 2:
                    if ignorar_if > 0:
                        ignorar_if -= 1
                        break
                    estado, detalle = ejec_end_else()

        if len(continuacion)>0:
            if continuacion[-1]:
                continue

        i = -1
        for tipo in tipos_lineas:
            
            i += 1
            match2 = tipo.fullmatch(linea)
            if match2:
                revision2 = True
                coincidencias = match2.groups()                
                if i == 0:
                    estado, detalle = ejec_def(coincidencias)
                    
                elif i == 1:
                    estado, detalle = ejec_dp_asig(coincidencias)
                
                elif i == 2:
                    estado, detalle = ejec_dp_num_str(coincidencias)
                elif i == 3:
                    estado, detalle = funcion_mostrar(coincidencias[0])

                break
        if revision1 ==False and revision2 == False:
            estado, detalle = analisis_sintaxis(linea)
        if estado == False:
            Error(detalle, numero_linea)
            break

if len(print_mostrar)>0:
    printear = open("output.txt", "w")
    for resultado in print_mostrar:
        printear.write(resultado+"\n")
    printear.close()
archivo.close()