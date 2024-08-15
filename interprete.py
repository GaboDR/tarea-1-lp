import re

variables = {}
mayusculas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
minusculas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#para restringir iterados hay que implementar una pila
bloque_if = False
bloque_else = False
continuacion = False
numeros = r"(\d+)"
bools = r"(True | False)"
strings = r"(#.+#)"

opciones = f"({numeros} | {strings} | {bools})"


tipo_var = re.compile(r"(\$_[A-Z][a-z]*[A-Z]*)")

tipo_define = re.compile(r"(^DEFINE)\s+"+ tipo_var.pattern)

tipo_dp_asig = re.compile(r"(^DP)\s+" + tipo_var + r"\s+(^ASIG)\s+" +  opciones )

tipo_dp_gen = re.compile(r"(^DP)\s+" + tipo_var+ r" \s+ [\+ | == | \* | > ] \s+" + (opciones | tipo_var) + r"\s" + (opciones | tipo_var))

tipo_mostrar = re.compile(r"^MOSTRAR({tipo_var})")

tipo_if = re.compile(r"(^if)\s+\(" + tipo_var + r"^\)\s+" r"^{")

tipo_else = re.compile(r"^\}\s+" + r"^else\s+" + r"^\{")

cierre_llaves = re.compile(r"^\}")

def picar(linea_funcion):
    return

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
            if re.match(r'^\#', linea[3]) :
                linea[3] = re.sub(r'^\#',"",linea[3])
                variables[linea[1]]= linea[3]
            elif linea[3] == "True":
                variables[linea[1]]= True
            elif linea[3] == "False":
                variables[linea[1]]= False

            else:
                variables[linea[1]] = int(linea[3])

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
                if isinstance(par1, str) or isinstance(par2, str):
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

                if isinstance(par1, str) or isinstance(par2, str):
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

def verificar_if(cond):
    if cond in variables:
        resultado = variables[cond]
        if isinstance(resultado, bool):
            return [True, resultado]
        else:
            error = "tipo incorrecto"
    else:
        error = "variable no definida"
    return [False, error]


archivo = open("codigo.txt", "r")
numero_linea = 0
for linea in archivo:
    #print(bloque_if, bloque_else, continuacion)
    numero_linea +=1 
    linea=linea.strip()
    
    linea_str= re.split(r'#',linea)
    linea_funcion=re.split(r'\s+',linea_str[0])

    if len(linea_str) > 2:
        string1= "#"+linea_str[1]
        string2= "#"+linea_str[2]

        linea_funcion.append(string1)
        linea_funcion.append(string2)
    elif len(linea_str) > 1:
        string1= "#"+linea_str[1]
        linea_funcion.append(string1)  
    
    linea_funcion = list(filter(None, linea_funcion))

    #print(linea_funcion)

    if "if" == linea_funcion[0]:
        condicion = re.sub(r'\(|\)',"",linea_funcion[1])
        estado , detalle = verificar_if(condicion)

        if estado == True and detalle == True:
            bloque_if =True
            #hacer el if
        elif estado == True and detalle == False:
            bloque_else=True
            continuacion = True
            #hacer el else
 
    elif "}" == linea_funcion[0] and len(linea_funcion) >1:
        #finaliza un bloque if y empieza else
        if bloque_if:
            bloque_if = False
            continuacion = True
        else:
            continuacion = False

    elif "}" == linea_funcion[0] and len(linea_funcion) ==1:
        #finaliza un bloque else
        bloque_else=False
        continuacion = False

    #espacio para poner continue
    if continuacion:
        print(numero_linea)
        continue


    elif "DEFINE" == linea_funcion[0]:
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