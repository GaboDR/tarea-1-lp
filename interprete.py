import re

variables = {}

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
opciones_num_str = f"({numeros}|{strings}|{tipo_var})"

# Definiciones de líneas
tipo_define = re.compile(r"(DEFINE)\s+" + f"({tipo_var})")
tipo_dp_asig = re.compile(r"(DP)\s+" + f"({tipo_var})" + r"\s+(ASIG)\s+" + opciones_asig)
tipo_dp_num_str = re.compile(r"(DP)\s+" + f"({tipo_var})" + r"\s+(\+|==|\*|>)\s+" + opciones_num_str + r"\s+" + opciones_num_str)
tipo_mostrar = re.compile(rf"^MOSTRAR\("+ f"({tipo_var})\)")
tipo_if = re.compile(r"if\(" + f"({tipo_var})" + r"\)\s+\{")
tipo_else = re.compile(r"\}\s+else\s+\{")
cierre_llaves = re.compile(r"^\}$")

# Agrupar todas las expresiones regulares
tipos_lineas = [tipo_define, tipo_dp_asig,  tipo_dp_num_str, tipo_mostrar, ]

tipos_cond = [tipo_if, tipo_else, cierre_llaves]

def determinar_tipo_y_castear(valor):
    if re.fullmatch(numeros, valor):
        return int(valor) 
    elif re.fullmatch(bools, valor):

        return valor == "True" 
    elif re.fullmatch(strings, valor):

        return valor.strip("#") 

def Error(tipo, linea):
    print(f"Error en la linea {linea}, {tipo}")

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
            error = "variable no booleana"
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
    # Intenta detectar cuál parte de la línea es incorrecta
    partes = linea.split()
    
    if not partes:
        return False, "línea vacía o incompleta"
    
    # Revisa si la primera palabra clave coincide con alguna esperada
    palabra_clave = partes[0]
    
    if palabra_clave not in ["DEFINE", "DP", "MOSTRAR", "if", "}"]:
        return False, f"palabra clave no válida: '{palabra_clave}'"
    
    # Revisa el formato según la palabra clave detectada
    if palabra_clave == "DEFINE":
        if len(partes) != 2 or not re.fullmatch(tipo_var, partes[1]):
            return False, f"error de sintaxis en DEFINE: se esperaba 'DEFINE $Variable'"
    
    elif palabra_clave == "DP":
        if len(partes) < 4:
            return False, "error de sintaxis en DP: línea incompleta"
        
        if not re.fullmatch(tipo_var, partes[1]):
            return False, f"variable no válida: '{partes[1]}' en DP"
        
        if partes[2] != "ASIG" and partes[2] not in ["+", "==", "*", ">"]:
            return False, f"aperador no válido en DP: '{partes[2]}'"
        
        if not re.fullmatch(opciones_asig, partes[3]):
            return False, f"valor no válido: '{partes[3]}' en DP"
    
    elif palabra_clave == "MOSTRAR":
        if len(partes) != 2 or not re.fullmatch(tipo_var, partes[1]):
            return False, "error de sintaxis en MOSTRAR: se esperaba 'MOSTRAR($Variable)'"
    
    elif palabra_clave == "if":
        if len(partes) < 4 or partes[1] != "(" or partes[-1] != "{":
            return False, "error de sintaxis en if: se esperaba 'if($Variable) {'"
    
    elif palabra_clave == "}":
        # Analizar el formato "} else {"
        if len(partes) == 3 and partes[1] == "else" and partes[2] == "{":
            return True, None
        return False, "error de sintaxis en else: se esperaba '} else {'"
    
    return False, "sintaxis no identificado"

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