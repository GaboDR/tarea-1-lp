import re

variables = {}

bloque_if = []
bloque_else = []
continuacion = []
print_mostrar = []
ignorar_if = 0


numeros = r"\d+"  
bools = r"True|False" 
strings = r"#.+#"  
tipo_var = r"\$_[A-Z][a-zA-Z]*" 

datos = [numeros, bools, strings, tipo_var]

opciones = f"({numeros}|{strings}|{bools})"
opciones_asig = f"({numeros}|{strings}|{bools}|{tipo_var})"
opciones_num_str = f"({numeros}|{strings}|{tipo_var})"

# Definiciones de líneas
tipo_define = re.compile(r"(DEFINE)\s+" + f"({tipo_var})")
tipo_dp_asig = re.compile(r"(DP)\s+" + f"({tipo_var})" + r"\s+(ASIG)\s+" + opciones_asig)
tipo_dp_num_str = re.compile(r"(DP)\s+" + f"({tipo_var})" + r"\s+(\+|==|\*|>)\s+" + opciones_num_str + r"\s+" + opciones_num_str)
tipo_mostrar = re.compile(rf"^MOSTRAR\(\s*"+ f"({tipo_var})\s*\)")
tipo_if = re.compile(r"if\s+\(" + f"({tipo_var})" + r"\)\s*\{")
tipo_else = re.compile(r"\}\s+else\s+\{")
cierre_llaves = re.compile(r"^\}$")

tipos_lineas = [tipo_define, tipo_dp_asig,  tipo_dp_num_str, tipo_mostrar, ]
tipos_cond = [tipo_if, tipo_else, cierre_llaves]

"""
***
Parametro 1 : valor de variable extraida del .txt
...
***
Retorna la variable casteada 
***
El parametro se compara con los 3 datos posibles (booln, int, str) y retorna el valor
casteado al tipo correspondiente, con los str les extrae los "#"
"""
def determinar_tipo_y_castear(valor):
    if re.fullmatch(numeros, valor):
        return int(valor) 
    elif re.fullmatch(bools, valor):

        return valor == "True" 
    elif re.fullmatch(strings, valor):

        return valor.strip("#") 
"""
***
Parametro 1 : str con la descripcion del error
Parametro 2 : int con el numero de la linea donde fallo el codigo
...
***
No tiene retorno
***
la funcion muestra en consola el tipo y la linea del error, en un formato simple
"""
def Error(tipo, linea):
    print(f"Error en la linea {linea}, {tipo}")
"""
***
Parametro 1 : Variable a añadir en el archivo output.txt
...
***
Retorna una lista con el estado de la solicitud (True hecha, False con un error)
***
Verifica si la variable existe y añade su valor a una lista para escribirla al final
"""
def funcion_mostrar(variable):
    if variable in variables:
        if variables[variable] != None:
            print_mostrar.append(str(variables[variable]))
            return [True, None]
        return [False, "variable no definida"]
    return [False, "variable no existente"]
"""
***
Parametro 1 : condicion dentro del if booleana
...
***
Retorna una lista con el estado de la solicitud y el detalle (True y el valor de la comparacion
o False y el error)
***
Verifica la existencia y el tipo de la variable, si esta todo correcto la retorna, en caso con-
trario clasifica y retorna el error
"""
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
"""
***
Parametro 1 : lista con las partes de una linea de definicion
...
***
Retorna una lista con el estado de la solicitud (True hecha, False con un error)
***
Revisa si la variable no fue declarada y la declara
"""
def ejec_def(linea_div):
    _, var = linea_div
    if var not in variables:
        variables[var] = None
        return [True, None]
    return [False, "variable ya existente"]
"""
***
Parametro 1 : lista con las partes de una linea de asignación
...
***
Retorna una lista con el estado de la solicitud (True hecha, False con un error)
***
Asigna un valor a una variable previamente definida. Si la variable a la que se 
quiere asignar un valor no existe, o si el valor a asignar no puede ser 
casteado correctamente, retorna un error.
"""
def ejec_dp_asig(linea_div):
    _ , var, _, valor = linea_div
    if valor in variables:
        valor = variables[valor]
    if var in variables:
        valor = determinar_tipo_y_castear(valor)
        variables[var] = valor
        return [True, None]
    return [False, "variable no existente"]
"""
***
Parametro 1 : lista con las partes de una linea de operación numérica o comparación
...
***
Retorna una lista con el estado de la solicitud (True hecha, False con un error)
***
Realiza operaciones numéricas o comparaciones entre variables o valores. 
Soporta suma, multiplicación, comparación de igualdad y comparación mayor que. 
En caso de error, retorna un mensaje de error adecuado.
"""
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
"""
***
Parametro 1 : condicion dentro del if booleana
...
***
Retorna una lista con el estado de la solicitud (True si la condición se cumple, False con un error)
***
Maneja la evaluación de una condición booleana en una sentencia if. Controla 
la cantidad de bloques if anidados permitidos y gestiona los bloques else 
correspondientes en base al resultado de la condición.
"""
def ejec_if(cond):
    if len(bloque_if)>4:
        return [False, "numero de if anidados soportados superado"]
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
"""
***
Parametro 1 : No recibe
...
***
Retorna una lista con el estado de la solicitud (True hecha, None)
***
Maneja la transición de un bloque if a un bloque else. Controla la finalización 
del bloque if y la activación del bloque else.
"""
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
"""
***
Parametro 1 : No recibe
...
***
Retorna una lista con el estado de la solicitud (True hecha, None)
***
Finaliza un bloque condicional (if o else), limpiando las pilas de control de 
bloques y continuaciones.
"""
def ejec_end_else():
    #finaliza bloque condicional
    bloque_if.pop()
    bloque_else.pop()
    continuacion.pop()
    return [True, None]
"""
***
Parametro 1 : str con la linea de código a analizar
...
***
Retorna una lista con el estado de la solicitud (True si no hay errores, False con un mensaje de error)
***
Realiza un análisis de sintaxis de una línea de código para detectar posibles errores. 
Verifica la correcta utilización de palabras clave y estructuras del lenguaje.
"""
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
