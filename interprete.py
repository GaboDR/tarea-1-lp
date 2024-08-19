from funciones import *

with open("codigo.txt", "r") as archivo:
    numero_linea = 0
    for linea in archivo:
        revision1 = False
        revision2 = False
        numero_linea += 1 
        print(numero_linea)
        linea = linea.strip()
        j = -1
        for condcional in tipos_cond:
            j += 1
            match = condcional.fullmatch(linea)
            if match:
                coincidencias = match.groups()
                print(coincidencias, numero_linea, j)

                
                if j == 0:
                    estado, detalle = ejec_if(coincidencias[0])

                    
                elif j == 1:
                    estado, detalle = ejec_if_else()
                
                elif j == 2:
                    estado, detalle = ejec_end_else()
                revision1 = True  

        if len(continuacion)>0:
            print(bloque_if, bloque_else, continuacion)
            if continuacion[-1]:
                print("@")
                continue

        i = -1
        for tipo in tipos_lineas:
            
            i += 1
            match2 = tipo.fullmatch(linea)
            if match2:
                coincidencias = match2.groups()
                print(coincidencias, numero_linea, i)
                
                if i == 0:
                    estado, detalle = ejec_def(coincidencias)
                    
                elif i == 1:
                    estado, detalle = ejec_dp_asig(coincidencias)
                
                elif i == 2:
                    estado, detalle = ejec_dp_num_str(coincidencias)
                elif i == 3:
                    estado, detalle = funcion_mostrar(coincidencias[0])
                revision2 = True

                break
        if revision1 ==False and revision2 == False:
            #analisis de no coincidencias
            estado, detalle = analisis_sintaxis(linea)
        if estado == False:
            Error(detalle, numero_linea)
            break

archivo.close()