import re

variables = {}
mayusculas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
minusculas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numeros = [0,1,2,3,4,5,6,7,8,9]

def Error(tipo, linea):
    print(tipo)
    print(linea)



def definicion(linea):
    valido = r'^\$_'
    match=re.match(valido,linea[1])
    if match:
        if linea[1][2] in mayusculas:
            nombre = linea[1]           #se guarda la variable con el $_
            if nombre in variables:
                error = "ya existente"
            else:
                variables[nombre]=None
                return [True, None]
        else:
            error = "mayusculas"
    else:
        error = "mal inicio"
    return [False, error]

def funcion_dp(linea):
    error = "sintaxsis desconocida"
    if linea[1] in variables:
        if linea[2] == "ASIG":
            variables[linea[1]]= linea[3]
            return [True, None]
        if any(linea[i] in [True, False] or variables.get(linea[i]) in [True, False] for i in [3, 4]):
            error = "no operable"
        else:    
            par1 = linea[3]
            par2 = linea[4]
            if par1 in variables:
                par1 = variables[par1]
            if par2 in variables:
                par2 = variables[par2]

            if linea[2] in ["+", "=="]:
                if re.search(r'[a-zA-z]', par1) or re.search(r'[a-zA-z]', par2):
                    par1= str(par1)
                    par2= str(par2)
                
                if linea[2] == "+":
                    
                    resultado= par1 + par2
                    variables[linea[1]]=resultado
                    return [True, None]
                else:
                    if par1 == par2:

                        variables[linea[1]]=True
                        return [True, None]
                    else:
                        variables[linea[1]]=False
                        return [True, None]
            
            elif linea[2] in ["*", ">"]:

                if re.search(r'[a-zA-z]', par1) or re.search(r'[a-zA-z]', par2):
                    error = "no valido"

                else:
                    if linea[2] == "*":
                        resultado = int(par1) * int(par2)
                        variables[linea[1]]=resultado

                        return [True, None]

                    else:
                        if par1 > par2:

                            variables[linea[1]]=True
                            return [True, None]
                        else:
                            variables[linea[1]]=False

                            return [True, None]
    else:
        error = "no variable"

    return [False, error]

def funcion_mostrar(variable):
    if variable in variables:
        printear = open("output.txt", "w")
        printear.write(str(variables[variable]))
        printear.close()
        return [True, None]
    return [False, "no existe"]


archivo = open("codigo.txt", "r")
numero_linea = 0
for linea in archivo:
    numero_linea +=1 
    linea=linea.strip()
    
    linea_str= re.split(r'#',linea)
    linea_funcion=re.split(r'\s+',linea_str[0])




    if len(linea_str) > 2:
        string1= linea_str[1]
        string2= linea_str[2]

        linea_funcion.append(string1)
        linea_funcion.append(string2)
    elif len(linea_str) > 1:
        string1= linea_str[1]
        linea_funcion.append(string1)  
    
    
    
    linea_funcion = list(filter(None, linea_funcion))
 


    if "DEFINE" == linea_funcion[0]:

        estado, detalle = definicion(linea_funcion)
    elif "DP" == linea_funcion[0]:
        estado, detalle = funcion_dp(linea_funcion)
    elif "MOSTRAR" in linea_funcion[0]:
        parametros = re.split(r'\(',linea_funcion[0])
        estado, detalle = funcion_mostrar(parametros[1][:-1])
    
    if estado == False:
        Error(detalle, numero_linea)
        break


archivo.close()