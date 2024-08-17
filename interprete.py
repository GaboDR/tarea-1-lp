import re

variables = {}
mayusculas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
minusculas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#para restringir iterados hay que implementar una pila
bloque_if = []
bloque_else = []
continuacion = []

# Definir las expresiones regulares
numeros = r"\d+"  # Captura el número
bools = r"True|False"  # Captura True o False
strings = r"#.+#"  # Captura el string entre #
tipo_var = r"\$_[A-Z][a-zA-Z]*"  # Captura el tipo de variable

datos = [numeros, bools, strings, tipo_var]

# Opciones con captura agrupada
opciones = f"({numeros}|{strings}|{bools})"
opciones_asig = f"({numeros}|{strings}|{bools}|{tipo_var})"
#opciones_num = f"({numeros}|{tipo_var})"
opciones_num_str = f"({numeros}|{strings}|{tipo_var})"

# Definiciones de líneas
tipo_define = re.compile(r"(DEFINE)\s+" + f"({tipo_var})")
tipo_dp_asig = re.compile(r"(DP)\s+" + f"({tipo_var})" + r"\s+(ASIG)\s+" + opciones_asig)
#tipo_dp_num = re.compile(r"(DP)\s+" + f"({tipo_var})" + r"\s+(\+|==|\*|>)\s+" + opciones_num + r"\s+" + opciones_num)
tipo_dp_num_str = re.compile(r"(DP)\s+" + f"({tipo_var})" + r"\s+(\+|==|\*|>)\s+" + opciones_num_str + r"\s+" + opciones_num_str)
tipo_mostrar = re.compile(rf"^MOSTRAR\("+ f"({tipo_var})\)")
tipo_if = re.compile(r"if\s+\(" + f"({tipo_var})" + r"\)\s+\{")
tipo_else = re.compile(r"\}\s+else\s+\{")
cierre_llaves = re.compile(r"^\}$")

# Agrupar todas las expresiones regulares
tipos_lineas = [tipo_define, tipo_dp_asig,  tipo_dp_num_str, tipo_mostrar, ]

tipos_cond = [tipo_if, tipo_else, cierre_llaves]

def determinar_tipo_y_castear(valor):
    if re.fullmatch(numeros, valor):
        return int(valor)  # Castear a entero
    elif re.fullmatch(bools, valor):

        return valor == "True"  # Castear a booleano
    elif re.fullmatch(strings, valor):

        return valor.strip("#")  # Eliminar los #

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
    return [False, "variable no existente"]

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

def ejec_def(linea_div):
    _, var = linea_div
    if var not in variables:
        variables[var] = None
        return [True, None]
    return [False, "variable ya existente"]

def ejec_dp_asig(linea_div):
    _ , var, _, valor = linea_div
    if valor in variables:
        valor = variables[valor]
    if var in variables:
        valor = determinar_tipo_y_castear(valor)
        variables[var] = valor
        return [True, None]
    return [False, "variable no existente"]

def ejec_dp_num_str(linea_div):
    _, var,operador, par1, par2 = linea_div
    if var not in variables:
        return [False, "variable no definida"]
    match1 = re.match(r"\$_", par1)
    if match1:
        if par1 in variables:
            par1 = variables[par1]
        else:
            return [False, "variable no definida"]

    match2 = re.match(r"\$_", par2)
    if match2:
        if par2 in variables:
            par2 = variables[par2]
        else:
            return [False, "variable no definida"]

    if isinstance(par1,bool) or isinstance(par2,bool):
        return [False, "variable no operable"]
    
    if operador == "+":
        if isinstance(par1,str) or isinstance(par2,str):
            par1 = str(par1)
            par2 = str(par2)
        resultado = par1 + par2
        variables[var] = resultado
        return [True, None]
    elif operador == "==":
        if isinstance(par1,str) or isinstance(par2,str):
            par1 = str(par1)
            par2 = str(par2)
        if par1 == par2:
            variables[var] = True
        else:
            variables[var] = False
        return [True, None]
    elif operador == "*":
        if isinstance(par1,int) or isinstance(par2,int):
        
            resultado = par1 * par2
            variables[var] = resultado
            return [True, None]
        return [False, "variable no operable"]
        
    else:
        if isinstance(par1,int) or isinstance(par2,int):
            if par1 > par2:
                variables[var] = True
            else:
                variables[var] = False
            return [True, None]
        return [False, "variable no operable"]
        
def ejec_if(cond):
    estado, detalle = verificar_if(cond)
    if estado == True and detalle == True:
        #hacer el if
        bloque_if.append(True)
        bloque_else.append(False)
        continuacion.append(False)
        return [True, None]
    elif estado == True and detalle == False:
        #hacer el else
        bloque_else.append(True)
        continuacion.append(True)
        bloque_if.append(False)
        return [True, None]
    return [estado, detalle]

def ejec_if_else():
    #finaliza un bloque if y empieza else
    if bloque_if[-1]:
        bloque_if.pop()
        bloque_if.append(False)
        continuacion.pop()
        continuacion.append(True)
    else:
        continuacion.pop()
        continuacion.append(False)
    return [True, None]

def ejec_end_else():
    #finaliza bloque condicional
    bloque_if.pop()
    bloque_else.pop()
    continuacion.pop()
    return [True, None]

def analisis_sintaxis(linea):
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
    if "DEFINE" == linea_funcion[0]:
        estado, detalle = definicion(linea_funcion)

    elif "DP" == linea_funcion[0]:
        estado, detalle = funcion_dp(linea_funcion)

    elif "MOSTRAR" in linea_funcion[0]:
        parametros = re.split(r'\(',linea_funcion[0])
        estado, detalle = funcion_mostrar(parametros[1][:-1])
    else:
        estado=False
        detalle = "sintaxis no reconocida"
    return estado, detalle

with open("codigo.txt", "r") as archivo:
    numero_linea = 0
    for linea in archivo:
        numero_linea += 1 
        linea = linea.strip()
        print(linea)
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

        if len(continuacion)>0:
            print(bloque_if, bloque_else, continuacion)
            if continuacion[-1]:
                continue

        i = -1
        for tipo in tipos_lineas:
            i += 1
            match = tipo.fullmatch(linea)
            if match:
                coincidencias = match.groups()
                print(coincidencias, numero_linea, i)
                
                if i == 0:
                    estado, detalle = ejec_def(coincidencias)
                    
                elif i == 1:
                    estado, detalle = ejec_dp_asig(coincidencias)
                
                elif i == 2:
                    estado, detalle = ejec_dp_num_str(coincidencias)
                elif i == 3:
                    estado, detalle = funcion_mostrar(coincidencias[0])
                break
            else:
                #analisis de no coincidencias
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
                if "DEFINE" == linea_funcion[0]:
                    estado, detalle = definicion(linea_funcion)

                elif "DP" == linea_funcion[0]:
                    estado, detalle = funcion_dp(linea_funcion)

                elif "MOSTRAR" in linea_funcion[0]:
                    parametros = re.split(r'\(',linea_funcion[0])
                    estado, detalle = funcion_mostrar(parametros[1][:-1])
                else:
                    estado=False
                    detalle = "sintaxis no reconocida"
        if estado == False:
            Error(detalle, numero_linea)
            break

archivo.close()

