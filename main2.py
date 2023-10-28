import re
import pandas as pd
import openpyxl

direccion_final= []
##realizar caso por caso, limpiar un caso y despues el otro
sustituciones = {
    r'\bCARRERA\b': 'CR',
    r'\bCALLE\b': 'CL',
    r'\bCIRCULAR\b': 'CQ',
    r'\bTRANSVERSAL\b': 'TV',
    r'\bDIAGONAL\b': 'DG',
}

palabras_clave = {"CARRERA", "CALLE", "CIRCULAR", "TRANSVERSAL", "DIAGONAL", "CL", "CR"}

def eliminar_palabras_sobrantes(direcciones):
    direccion_limpia = []
    patron = r"^[a-zA-Z0-9]+\s[a-zA-Z0-9]+$"

    # Iterar a través de las cadenas y comprobar si cumplen con el patrón
    for direccion in direcciones:
        if not re.match(patron, direccion):
            direccion= ""
            direccion_limpia.append(direccion)
        direccion_limpia.append(direccion)
    return direccion_limpia

def reemplazo(match):
    return sustituciones[match.group()]

def borrar_direccion_repetida(direcciones):
    direccion_limpia = []
    pattern = re.compile(r'^(.*?)(CALLE|CARRERA)')

    for direccion in direcciones:
        match = re.search(pattern, direccion)
        if match:
            inicio_direccion = match.group(1)
            direccion_limpia.append(inicio_direccion)
        else:
            direccion_limpia.append(direccion)
    return direccion_limpia

def borrar_entre(direcciones):
    direcciones_estandarizadas = []

    for direccion in direcciones:
        palabras = direccion.split()
        if 'ENTRE' in palabras or 'POR' in palabras:
            if 'ENTRE' in palabras:
                indice_entre = palabras.index('ENTRE')
                if indice_entre > 0 and palabras[indice_entre + 1] in ['CR', 'CL', 'CARRERA', 'CALLE', 'CALLES']:
                    palabras[indice_entre:indice_entre + 2] = ['']
                    if 'Y' in palabras[indice_entre:]:
                        indice_y = palabras.index('Y', indice_entre)
                        palabras = palabras[:indice_y]
                    if 'Y' in palabras:
                        palabras = [palabra for palabra in palabras if palabra != 'Y']
            if 'POR' in palabras:
                indice_entre = palabras.index('POR')
                if indice_entre > 0 and palabras[indice_entre + 1] in ['CR', 'CL', 'CARRERA', 'CALLE', 'CALLES']:
                    palabras[indice_entre:indice_entre + 2] = ['']
                    if 'Y' in palabras[indice_entre:]:
                        indice_y = palabras.index('Y', indice_entre)
                        palabras = palabras[:indice_y]
                    if 'Y' in palabras:
                        palabras = [palabra for palabra in palabras if palabra != 'Y']

        
        direccion_final = ' '.join(palabra for palabra in palabras if palabra)
        direcciones_estandarizadas.append(direccion_final.strip())
    return direcciones_estandarizadas

def estandarizar_direccion(direcciones):
    nuevas_direcciones = []
    print(direcciones)
    nueva_cadena = []
    for direccion in direcciones:
        palabras = direccion.split()
        print(palabras)
        if palabras[0] == "CR":
            print(palabras[0])
            nueva_cadena.append(palabras[0])
            print
            if re.match(r'^[0-9]{1,3}$', palabras[1]):
                nueva_cadena.append(palabras[1])
            elif re.match(r'^[0-9]{1,3}[A-Za-z]{0,2}$', palabras[1]):
                nueva_cadena.append(palabras[1])
        direccion_unida = " ".join(nueva_cadena)
        nuevas_direcciones.append(direccion_unida)
    return nuevas_direcciones

def limpiar_direccion(direcciones):
    direccion_limpia = []
    direccion_corta = []
    direccion_split = []

    # Define un diccionario que mapea palabras clave a funciones de reemplazo

    for direccion in direcciones:
        nueva_cadena = ""
        encontrado = False
        direccion = str.upper(direccion)
        #print(direccion)
        if direccion.strip() == "":
            direccion_corta.append(direccion)
        elif direccion.startswith("<"):
            contenido = direccion[1:-1]  # Elimina los signos "<" y ">"
            #print(contenido)
            split_contenido = contenido.split()
            #print(split_contenido)
            if split_contenido[0] in palabras_clave:
                #print(split_contenido)
                contenido = " ".join(split_contenido)
                if ";" in contenido:
                    parte_anterior = contenido.split(";", 1)[0]
                    #print(parte_anterior)
                    dire_upper = str.upper(parte_anterior)
                    direccion_split = dire_upper.split()
                    #print(direccion_split)
                    #print(direccion_split)
                    direccion_unida= ""
                    if direccion_split[0] in palabras_clave:
                        direccion_unida = " ".join(direccion_split)
                        #print(direccion_unida)
                        direccion_unida = re.compile(r'<[^>]+>')
                        cadena_sin_contenido = direccion_unida.sub('', dire_upper)
                        contenido_entre_parentesis = re.compile(r'\([^)]+\)')
                        cadena_sin_parentesis = contenido_entre_parentesis.sub('', cadena_sin_contenido)
                        #print(cadena_sin_parentesis)
                        for caracter in cadena_sin_parentesis:
                            if caracter == ';' or caracter == ',' or caracter == '<' or caracter == '>' or caracter == '>' or caracter == '/' or caracter=='&':
                                encontrado = True
                            if not encontrado:
                                nueva_cadena += caracter
                        direccion_corta.append(nueva_cadena)
                else:
                    direccion_unida = re.compile(r'<[^>]+>')
                    cadena_sin_contenido = direccion_unida.sub('', contenido)
                    contenido_entre_parentesis = re.compile(r'\([^)]+\)')
                    cadena_sin_parentesis = contenido_entre_parentesis.sub('', cadena_sin_contenido)
                    #print(cadena_sin_parentesis)
                    for caracter in cadena_sin_parentesis:
                        if caracter == ';' or caracter == ',' or caracter == '<' or caracter == '>' or caracter == '>' or caracter == '/' or caracter=='&':
                            encontrado = True
                        if not encontrado:
                            nueva_cadena += caracter
                    direccion_corta.append(nueva_cadena)

            elif split_contenido[0] not in palabras_clave:
                contenido = " ".join(split_contenido)
                if ";" in contenido:
                    parte_anterior = contenido.split(";", 1)[1]
                    dire_upper = str.upper(parte_anterior)
                    direccion_split = dire_upper.split()
                    #print(direccion_split)
                    #print(direccion_split)
                    direccion_unida= ""
                    if direccion_split[0] in palabras_clave:
                        direccion_unida = " ".join(direccion_split)
                        #print(direccion_unida)
                        direccion_unida = re.compile(r'<[^>]+>')
                        cadena_sin_contenido = direccion_unida.sub('', dire_upper)
                        contenido_entre_parentesis = re.compile(r'\([^)]+\)')
                        cadena_sin_parentesis = contenido_entre_parentesis.sub('', cadena_sin_contenido)
                        #print(cadena_sin_parentesis)
                        for caracter in cadena_sin_parentesis:
                            if caracter == ';' or caracter == ',' or caracter == '<' or caracter == '>' or caracter == '>' or caracter == '/' or caracter=='&':
                                encontrado = True
                            if not encontrado:
                                nueva_cadena += caracter
                        direccion_corta.append(nueva_cadena)
                    elif "SUBURBANO" in contenido:
                        contenido = ""
                        #print(contenido)
                        direccion_corta.append(contenido)  
                elif "VEREDA" in contenido:
                    contenido = ""
                    #print(contenido)
                    direccion_corta.append(contenido)          
        else:
            dire_upper = str.upper(direccion)
            direccion_split = dire_upper.split()
            #print(direccion_split)
            direccion_unida= ""
            
            if direccion_split[0] in palabras_clave:
                direccion_unida = " ".join(direccion_split)
                #print(direccion_unida)
                # Define una expresión regular que coincide con contenido entre '<' y '>'
                direccion_sin_caracteres = re.compile(r'<[^>]+>')
                # si dentro de  <> encuentra la palabra carrera,calle,cl...etc no me lo borre

                # Sustituye el contenido entre '<' y '>' con una cadena vacía
                cadena_sin_contenido = direccion_sin_caracteres.sub('', dire_upper)
                contenido_entre_parentesis = re.compile(r'\([^)]+\)')

                # Sustituye el contenido entre paréntesis con una cadena vacía
                cadena_sin_parentesis = contenido_entre_parentesis.sub('', cadena_sin_contenido)
                

                #print(cadena_sin_parentesis)
                for caracter in cadena_sin_parentesis:
                    if caracter == ';' or caracter == ',' or caracter == '<' or caracter == '>' or caracter == '/' or caracter=='&':
                        ##if caract < equivale al primer caracter ejecute otra funcion que verifica si la informacion contenida si es valida
                        encontrado = True
                    if not encontrado:
                        nueva_cadena += caracter
                # direccion sin < y ;
                
                direccion_corta.append(nueva_cadena)
            else:
                direccion_unida = " ".join(direccion_split)
                direccion_sin_caracteres = re.compile(r'<[^>]+>')
                # si dentro de  <> encuentra la palabra carrera,calle,cl...etc no me lo borre

                # Sustituye el contenido entre '<' y '>' con una cadena vacía
                cadena_sin_contenido = direccion_sin_caracteres.sub('', dire_upper)
                contenido_entre_parentesis = re.compile(r'\([^)]+\)')

                # Sustituye el contenido entre paréntesis con una cadena vacía
                cadena_sin_parentesis = contenido_entre_parentesis.sub('', cadena_sin_contenido)
                

                #print(cadena_sin_parentesis)
                for caracter in cadena_sin_parentesis:
                    if caracter == ';' or caracter == ',' or caracter == '<' or caracter == '>' or caracter == '/' or caracter=='&':
                        ##if caract < equivale al primer caracter ejecute otra funcion que verifica si la informacion contenida si es valida
                        encontrado = True
                    if not encontrado:
                        nueva_cadena += caracter
                direccion_corta.append(nueva_cadena)
            

    return direccion_corta

direccion_original2 = ["<CARRERA 48 ENTRE CALLES 17 Y 24>",
                       "CL 5 Y 6 ENTRE CR 25",
                       "CR 70 117 19CARRERA",
                       "CL 94D 83AC 36CALLE 94D 83AC 38"]

direccion_original = ["<CARRERA 48 ENTRE CALLES 17 Y 24>",
                       "CL 5 Y 6 ENTRE CR 25",
                        "64AE 97AB 07(201)<MANZANA 10>CALLE 64AE 97AB 09<MANZANA 10>CALLE 64AE 97AB 78(201)<MANZANA 10>CALLE 64AE 97AB 06<MANZANA 10>CARRERA 97A 64AC 21(202) <MANZANA 12>CARRERA 97A 64AC 31(202)<MANZANA 12>CARRERA 97A 64AC 63<MANZANA 12>CARRERA 97BB 64AG 66<MANZANA 1>CARRERA 97BB 64AG 64(0201,0202)<MANZANA 1>CARRERA 97BB 64AG 62<LOTE 1><MANZANA 1>CARRERA 97BB 64AG 56<MANZANA 1>CARRERA 97BB 64AG 54(0201,0202)<MANZANA 1>CARRERA 97BB 64AG 52<LOTE 2><MANZANA 1>CARRERA 97BB 64AG 46<MANZANA 1>CARRERA 97BB 64AG 44(0201,0202)<MANZANA 1>CARRERA 97BB 64AG 42<LOTE 3><MANZANA 1>CARRERA 97BB 64AG 36<MANZANA 1>CARRERA 97BB 64AG 34(0201,0202)<MANZANA 1>;97BB 64AG 32<LOTE4><MANZANA 1>CARRERA 97BB 64AG 26<MANZANA 1>CARRERA 97BB 64AG 24(0201,0202)<MANZANA 1>CARRERA 97BB 64AG 22<LOTE 5><MANZANA 1>CARRERA 97BB 64AG 16<MANZANA 1>CARRERA 97BB 64AG 14(0201,0202)<MANZANA 1>CARRERA 97BB 64AG 12<LOTE 6><MANZANA 1>CARRERA 97BB 64AG 06<MANZANA 1>CARRERA 97BB 64AG 04(0201,0202)<MANZANA 1>CARRERA 97BB 64AG 02<LOTE 7><MANZANA 1>CARRERA 97BA 64AG 01<MANZANA 1>CARRERA 97BA 64AG 03(0201,0202)<MANZANA 1>CARRERA 97BA 64AG 05<LOTE 8><MANZANA 1>CARRERA 97BA 64AG 11<MANZANA 1>CARRERA 97BA 64AG 13(0201,0202)<MANZANA 1>CARRERA 97BA 64AG 15<LOTE 9><MANZANA 1>CARRERA 97BA 64AG 21<MANZANA 1>CARRERA 97BA 64AG 23(0201,0202)<MANZANA 1>CARRERA 97BA 64AG 25<LOTE 10><MANZANA 1>CARRERA 97BA 64AG 31<MANZANA 1>CARRERA 97BA 64AG 33(0201,0202)<MANZANA 1>CARRERA 97BA 64AG 35<LOTE 11><MANZANA 1>CARRERA 97BA 64AG 41<MANZANA 1>CARRERA 97BA 64AG 43(0201,0202)<MANZANA 1>CARRERA 97BA 64AG 45<LOTE 12><MANZANA 1>CARRERA 97BA 64AG 51<MANZANA 1>CARRERA 97BA 64AG 53(0201,0202)<MANZANA 1>CARRERA 97BA 64AG 55<LOTE 13><MANZANA 1>CARRERA 97BA 64AG 48<MANZANA 1>CARRERA 97BA 64AG 46(0201,0202)<MANZANA 1>CARRERA 97BA 64AG 44<LOTE1><MANZANA 2>CARRERA 97BA 64AG 38<MANZANA 2>CARRERA 97BA 64AG 36(0201,0202)<MANZANA 2><MANZANA 2>CARRERA 97BA 64AG 34<LOTE 2><MANZANA 2>CARRERA 97BA 64AG 28<MANZANA 2>CARRERA 97BA 64AG 26(0201,0202)<MANZANA 2>CARRERA 97BA 64AG 24<LOTE 3><MANZANA 2>CARRERA 97BA 64AG 18<MANZANA 2>CARRERA 97BA 64AG 16(0201,0202)<MANZANA 2>CARRERA 97BA 64AG 14<LOTE 4><MANZANA 2>CARRERA 97BA 64AG 08<MANZANA 2>CARRERA 97BA 64AG 02(0201,0202) <MANZANA 2>CARRERA 97BA 64AG 04<LOTE 5><MANZANA 2>CARRERA 97AE 64AG 03<MANZANA 2>;97AE 64AG 05(0201,0202) <MANZANA 2> CARRERA 97AE 64AG 07<LOTE 6><MANZANA 2> CARRERA 97AE 64AG 13<MANZANA 2> CARRERA 97AE 64AG 15(0201,0202)<MANZANA 2> CARRERA 97AE 64AG 17<LOTE 7><MANZANA 2> CARRERA 97AE 64AG 23<MANZANA 2> CARRERA 97AE 64AG 25(0201,0202)<MANZANA 2> CARRERA 97AE 64AG 27<LOTE 8><MANZANA 2> CARRERA 97AE 64AG 33<MANZANA 2> CARRERA 97AE 64AG 35(0201,0202)<MANZANA 2> CARRERA 97AE 64AG 37<LOTE 9><MANZANA 2> CARRERA 97AE 64AG 43<MANZANA 2> CARRERA 97AE 64AG 45(0201,0202)<MANZANA 2> CARRERA 97AE 64AG 47<LOTE 10 MANZANA 2> CARRERA 97AE 64AG 40<MANZANA 3> CARRERA 97AE 64AG 38(0201,0202)<MANZANA 3> CARRERA 97AE 64AG 36<LOTE 1><MANZANA 3> CARRERA 97AE 64AG 30<MANZANA 3> CARRERA 97AE 64AG 28(0201,0202)<MANZANA 3> CARRERA 97AE 64AG 26<LOTE 2><MANZANA 3> CARRERA 97AE 64AG 20<MANZANA 3> CARRERA 97AE 64AG 18(0201,0202)<MANZANA 3> CARRERA 97AE 64AG 16<LOTE 3><MANZANA 3> CARRERA 97AE 64AG 10<MANZANA 3> CARRERA 97AE 64AG 08(0201,0202)<MANZANA 3> CARRERA 97AE 64AG 06<LOTE 4><MANZANA 3> CARRERA 97AE 64AG 05<MANZANA 3> CARRERA 97AE 64AG 07(0201,0202)<MANZANA 3> CARRERA 97AE 64AG 09<LOTE 5><MANZANA 3> CARRERA 97AC 64AG 15<MANZANA 3> CARRERA 97AC 64AG 17(0201,0202)<MANZANA 3> CARRERA 97AC 64AG 19<LOTE 6><MANZANA 3> CARRERA 97AC 64AG 25<MANZANA 3> CARRERA 97AC 64AG 27(0201,0202)<MANZANA 3> CARRERA 97AC 64AG 29<LOTE 7><MANZANA 3> CARRERA 97AC 64AG 35<MANZANA 3> CARRERA 97AC 64AG 37(0201,0202)<MANZANA 3> CARRERA 97AC 64AG 39<LOTE 8 MANZANA 3> CARRERA 97AC 64AG 38<MANZANA 4> CARRERA 97AC 64AG 36(0201,0202)<LOTE 1 MANZANA 4> CARRERA 97AC 64AG 28<MANZANA 4> CARRERA 97AC 64AG 26(0201,0202)<MANZANA 4> CARRERA 97AC 64AG 24<LOTE 2><MANZANA 4> CARRERA 97AC 64AG 18<MANZANA 4> CARRERA 97AC 64AG 16(0201,0202)<MANZANA 4> CARRERA 97AC 64AG 14<LOTE 3><MANZANA 4> CARRERA 97AC 64AG 08<MANZANA 4> CARRERA 97AC 64AG 06(0201,0202)<MANZANA 4> CARRERA 97AC 64AG 04<LOTE 4><MANZANA 4> CARRERA 97AB 64AG 03<MANZANA 4> CARRERA 97AB 64AG 05(0201,0202)<MANZANA 4> CARRERA 97AB 64AG 07<LOTE 5><MANZANA 4> CARRERA 97AB 64AG 13<MANZANA 4> CARRERA 97AB 64AG 15(0201,0202)<MANZANA 4> CARRERA 97AB 64AG 17<LOTE 6><MANZANA 4> CARRERA 97AB 64AG 23<MANZANA 4> CARRERA 97AB 64AG 25(0201,0202)<MANZANA 4> CARRERA 97AB 64AG 27<LOTE 7><MANZANA 4> CARRERA 97AB 64AG 33<MANZANA 4> CARRERA 97AB 64AG 35(0201,0202)<MANZANA 4> CARRERA 97AB 64AG 37<LOTE 8><MANZANA 4> CARRERA 97AB 64AF 78<MANZANA 5> CARRERA 97AB 64AF76<LOTE 1 MANZANA 5> CARRERA 97AB 64AF 70<MANZANA 5> CARRERA 97AB 64AF 68(0201,0202)<MANZANA 5> CARRERA 97AB 64AF 66<LOTE 2><MANZANA 5> CARRERA 97AB 64AF 60<MANZANA 5> CARRERA 97AB 64AF 58(0201,0202)<MANZANA 5> CARRERA 97AB 64AF 56<LOTE 3><MANZANA 5> CARRERA 97AB 64AF 50<MANZANA 5> CARRERA 97AB 64AF 48(0201,0202)<MANZANA 5> CARRERA 97AB 64AF 46<LOTE 4><MANZANA 5> CARRERA 97AB 64AF 40<MANZANA 5> CARRERA 97AB 64AF 38(0201,0202)<MANZANA 5> CARRERA 97AB 64AF 36<LOTE 5><MANZANA 5> CARRERA 97AB 64AF 20<MANZANA 5> CARRERA 97AB 64AF 18(0201,0202)<MANZANA 5>;97AB 64AF 16<LOTE 7><MANZANA 5>CARRERA 97AB 64AF 13<MANZANA 5>CARRERA 97AB 64AF 15(0201,0202)<MANZANA 5>CARRERA 97AB 64AF 17<LOTE 8><MANZANA 5>CARRERA 97AA 64AF 23<MANZANA 5>CARRERA 97AA 64AF 25(0201,0202)<MANZANA 5>CARRERA 97AA 64AF 27<LOTE 9><MANZANA 5>CARRERA 97AA 64AF 33<MANZANA 5>CARRERA 97AA 64AF 35(0201,0202)<MANZANA 5>CARRERA 97AA 64AF 37<LOTE 10><MANZANA 5>CARRERA 97AA 64AF 43<MANZANA 5>CARRERA 97AA 64AF 45(0201,0202) <MANZANA 5>CARRERA 97AA 64AF 47<LOTE 11><MANZANA 5>CARRERA 97AA 64AF 53<MANZANA 5>CARRERA 97AA 64AF 55(0201,0202)<MANZANA 5>CARRERA 97AA 64AF 57<LOTE 12><MANZANA 5>CARRERA 97AA 64AF 63<MANZANA 5>CARRERA 97AA 64AF 65(0201,0202)<MANZANA 5>CARRERA 97AA 64AF 67<LOTE 13><MANZANA 5>CARRERA 97AA 64AF 73<MANZANA 5>CARRERA 97AA 64AF 75(0201,0202)<MANZANA 5>CARRERA 97AA 64AF 77<LOTE 14><MANZANA 5>CARRERA 97AA 64AF 56<MANZANA 6>CARRERA 97AA 64AF 54(0201,0202)<MANZANA 6>CARRERA 97AA 64AF 52<LOTE 1 MANZANA 6>CARRERA 97AA 64AF 46<MANZANA 6>CARRERA 97AA 64AF 44(0201,0202)<MANZANA 6>CARRERA 97AA 64AF 42<LOTE 2><MANZANA 6>CARRERA 97AA 64AF 36<MANZANA 6>CARRERA 97AA 64AF 34(0201,0202)<MANZANA 6>CARRERA 97AA 64AF 32<LOTE 3><MANZANA 6>CARRERA 97AA 64AF 26<MANZANA 6>CARRERA 97AA 64AF 24(0201,0202)<MANZANA 6>CARRERA 97AA 64AF 22<LOTE 4><MANZANA 6>CARRERA 97AA 64AF 16<MANZANA 6>CARRERA 97AA 64AF 14(0201,0202)<MANZANA 6>CARRERA 97AA 64AF 12<LOTE 5><MANZANA 6>CARRERA 97AA 64AF 06<MANZANA 6>CARRERA 97AA 64AF 04(0201,0202)<MANZANA 6>CARRERA 97AA 64AF 02<LOTE 6><MANZANA 6>CARRERA 97 64AF 01<MANZANA 6><MANZANA 6>CARRERA 97 64AF 03(0201,0202)<MANZANA 6>CARRERA 97 64AF 05<LOTE 7><MANZANA 6>CARRERA 97 64AF 11<MANZANA 6>CARRERA 97 64AF 13(0201,0202)<MANZANA 6>CARRERA 97 64AF 15<LOTE 8><MANZANA 6>CARRERA 97 64AF 23<LOCAL><MANZANA 6>CARRERA 97 64AF 31<LOCAL><MANZANA 6>CARRERA 97 64AF 35<LOCAL><MANZANA 6>CARRERA 97 64AF 43<LOCAL><MANZANA 6>CARRERA 97 64AF 57<LOCAL><MANZANA 6>CARRERA 97 64AF 59<LOCAL><MANZANA 6>CARRERA 97BB 64AE 58<MANZANA 6>CARRERA 97BB 64AE 56(0201,0202)<MANZANA 6>CARRERA 97BB 64AE 54<LOTE 1 MANZANA 7>CARRERA 97BB 64AE 48<MANZANA 7>CARRERA 97BB 64AE 46(0201,0202)<MANZANA 7>CARRERA 97BB 64AE 44<LOTE 2><MANZANA 7>CARRERA 97BB 64AE 38<MANZANA 7>CARRERA 97BB 64AE 36(0201,0202)<MANZANA 7>CARRERA 97BB 64AE 34<LOTE 3><MANZANA 7>CARRERA 97BB 64AE 28<MANZANA 7>CARRERA 97BB 64AE 26(0201,0202)<MANZANA 7>CARRERA 97BB 64AE 24<LOTE 4><MANZANA 7>CARRERA 97BB 64AE 18<MANZANA 7>CARRERA 97BB 64AE 16(0201,0202)<MANZANA 7>CARRERA 97BB 64AE 14<LOTE 5><MANZANA 7>CARRERA 97BB 64AE 08<MANZANA 7>CARRERA 97BB 64AE 06<LOTE 6><MANZANA 7>CARRERA 97B 64AE 05<MANZANA 7>CARRERA 97B 64AE 07<LOTE 7><MANZANA 7>CARRERA 97B 64AE 13<MANZANA 7>CARRERA 97B 64AE 15(201,202)<MANZANA 7>CARRERA 97B 64AE 17<LOTE 8><MANZANA 7>CARRERA 97B 64AE 23<MANZANA 7>CARRERA 97B 64AE 25(0201,0202)<MANZANA 7>CARRERA 97B 64AE 27<LOTE 9><MANZANA 7>CARRERA 97B 64AE 33<MANZANA 7>CARRERA 97B 64AE 35(0201,0202)<MANZANA 7>CARRERA 97B 64AE 37<LOTE 10><MANZANA 7>CARRERA 97B 64AE 43<MANZANA 7>CARRERA 97B 64AE 45(0201,0202)<MANZANA 7>CARRERA 97B 64AE 47<LOTE 11><MANZANA 7>CARRERA 97B 64AE 53<MANZANA 7>CARRERA 97B 64AE 55(0201,0202)<MANZANA 7>CARRERA 97B 64AE 57<LOTE 12><MANZANA 7>CARRERA 97B 64AE 48<MANZANA 8>CARRERA 97B 64AE 46(0201,0202)<MANZANA 8>CARRERA 97B 64AE 44<LOTE 1 MANZANA 8>CARRERA 97B 64AE 38<MANZANA 8>CARRERA 97B 64AE 36(0201,0202)<MANZANA 8> CARRERA 97B 64AE 34<LOTE 2><MANZANA 8>CARRERA 97B 64AE 28<MANZANA 8>;97B 64AE 26(0201,0202)<MANZANA 8>CARRERA 97B 64AE 24<LOTE 3><MANZANA 8>CARRERA 97B 64AE 18<MANZANA 8>CARRERA 97B 64AE 16(0201,0202) <MANZANA 8>CARRERA 97B 64AE 14<LOTE 4><MANZANA 8>CARRERA 97B 64AE 08<MANZANA 8><MANZANA 8>CARRERA 97B 64AE 06<(0201,0202)><MANZANA 8>CARRERA 97B 64AE 04<LOTE 5><MANZANA 8>CARRERA 97AD 64AE 11<MANZANA 8>CARRERA 97AD 64AE 13(0201,0202)<MANZANA 8>CARRERA 97AD 64AE 15<LOTE 6 MANZANA 8>CARRERA 97AD 64AE 21<MANZANA 8>CARRERA 97AD 64AE 23(0201,0202)<MANZANA 8>CARRERA 97AD 64AE 25<LOTE 7 MANZANA 8>CARRERA 97AD 64AE 31<MANZANA 8>CARRERA 97AD 64AE 33(0201,0202)<MANZANA 8>CARRERA 97AD 64AE 35<LOTE 8><MANZANA 8>CARRERA 97AD 64AE 41<MANZANA 8>CARRERA 97AD 64AE 43(0201,0202)<MANZANA 8>CARRERA 97AD 64AE 45<LOTE 9 MANZANA 8>CARRERA 97AD 64AE 51<MANZANA 8><MANZANA 8>CARRERA 97AD 64AE 53(0201,0202)<MANZANA 8>CARRERA 97AD 64AE 55<LOTE 10 MANZANA 8>CARRERA 97AD 64AE 56<MANZANA 9>CARRERA 97AD 64AE 54(0201,0202)<MANZANA 9>CARRERA 97AD 64AE 52<LOTE 1 MANZANA 9>CARRERA 97AD 64AE 46<MANZANA 9>CARRERA 97AD 64AE 44(0201,0202)<MANZANA 9>CARRERA 97AD 64AE 42<LOTE 2 MANZANA 9>CARRERA 97AD 64AE 36<MANZANA 9>CARRERA 97AD 64AE 34(0201,0202)<MANZANA 9>CARRERA 97AD 64AE 32<LOTE 3 MANZANA 9>CARRERA 97AD 64AE 26<MANZANA 9>CARRERA 97AD 64AE 24(0201,0202)<MANZANA 9>CARRERA 97AD 64AE 22<LOTE 4 MANZANA 9>CARRERA 97AD 64AE 16<MANZANA 9>CARRERA 97AD 64AE 14(0201,0202)<MANZANA 9>CARRERA 97AD 64AE 12 <LOTE 5 MANZANA 9>CARRERA 97AD 64AE 06 <MANZANA 9>CARRERA 97AD 64AE 04(0201,0202)<MANZANA9>CARRERA 97AD 64AE 02<LOTE 6 MANZANA 9>CARRERA 97AD 64AE 01<MANZANA 9>CARRERA 97AD 64AE 03(0201,0202)<MANZANA 9>CARRERA 97AB 64AE 05 LOTE 7 MANZANA 9>CARRERA 97AB 64AE 11<MANZANA 9>CARRERA 97AB 64AE 13(0201,0202)<MANZANA 9>CARRERA 97AB 64AE 15 <LOTE 8 MANZANA 9>CARRERA 97AB 64AE 21 <MANZANA 9>CARRERA 97AB 64AE 23(0201,0202)<MANZANA 9>CARRERA 97AB 64AE 25<LOTE 9 MANZANA 9>CARRERA 97AB 64AE 31<MANZANA 9>CARRERA 97AB 64AE 33(0201,0202)<MANZANA 9>CARRERA 97AB 64AE 35<LOTE 10 MANZANA 9>CARRERA 97AB 64AE 41<MANZANA 9>CARRERA 97AB 64AE 43(0201,0202)<MANZANA 9>CARRERA 97AB 64AE 45 <LOTE 11 MANZANA 9>CARRERA 97AB 64AE 51 <MANZANA 9>CARRERA 97AB 64AE 53(0201,0202)<MANZANA 9>CARRERA 97AB 64AE 55 <LOTE 12 MANZANA 9>CALLE 64AE 97AB 69<MANZANA 10>CALLE 64AE 97AB 67(0201,0202)<MANZANA 10>CALLE 64AE 97AB 65 <LOTE 1 MANZANA 10 >CALLE 64AE 97AB 59<MANZANA 10>CALLE 64AE 97AB 57(0201,0202)<MANZANA 10>CALLE 64AE 97AB 55<LOTE 2 MANZANA 10>CALLE 64AE 97AB 49<MANZANA 10>CALLE 64AE 97AB 47(0201,0202)<MANZANA 10>CALLE 64AE 97AB 45 <LOTE 3 MANZANA 10>CALLE 64AE 97AB 39<MANZANA 10>CALLE 64AE 97AB 37(0201,0202)<MANZANA 10>CALLE 64AE 97AB 35<LOTE 4 MANZANA 10>CALLE 64AE 97AB 29<MANZANA 10>CALLE 64AE 97AB 27(0201,0202)<MANZANA 10>CALLE 64AE 97AB 25<LOTE 5 MANZANA 10>CALLE 64AE 97AB 19<MANZANA 10>CALLE 64AE 97AB 17(0201,0202)<MANZANA 10>CALLE 64AE 97AB 15 <LOTE 6 MANZANA 10>CALLE 64AE 97AB 09<MANZANA 10>CALLE 64AE 97AB 07(0201,0202)<MANZANA 10>CALLE 64AE 97AB 05<LOTE 7 MANZANA 10>CALLE 64AE 97AB 05<LOCAL LOTE 8 MANZANA 10>CALLE 64AE 97AB 01<LOCAL LOTE 9 MANZANA 10>CALLE 64AE 97AB 06<MANZANA 10>CALLE 64AE 97AB 08(0201,0202)<MANZANA 10>CALLE 64AE 97AB 10<LOTE 10 MANZANA 10>CALLE 64AE 97AB 16<MANZANA 10>CALLE 64AE 97AB 18(0201,0202)<MANZANA 10>CALLE 64AE 97AB 20 LOTE 11 MANZANA 10>CALLE 64AE 97AB 26<MANZANA 10>CALLE 64AE 97AB 28(0201,0202)<MANZANA 10>CALLE 64AE 97AB 30<LOTE 12 MANZANA 10>CALLE 64AE 97AB 36<MANZANA 10>CALLE 64AE 97AB 38(0201,0202)<MAZANA 10>CALLE 64AE 97AB 40<LOTE 13 MANZANA 10>CALLE 64AE 97AB 46<MANZANA 10>CALLE 64AE 97AB 48(0201,0202)<MANZANA 10>CALLE 64AE 97AB 50<LOTE 14 MANZANA 10>CALLE 64AE 97AB 56<MANZANA 10>CALLE 64AE 97AB 58(0201,0202)<MANZANA 10>CALLE 64AE 97AB 60 <LOTE 15 MANZANA 10>CALLE 64AE 97AB 66<MANZANA 10>CALLE 64AE 97AB 68(0201,0202)<MANZANA 10>CALLE 64AE 97AB 70<LOTE 16 MANZANA 10>CALLE 64AE 97AB 76<MANZANA 10>CALLE 64AE 97AB 78(0201,0202)<MANZANA 10>CALLE 64AE 97AB 80<LOTE 17 MANZANA 10>CARRERA 97AB 64AC 72<MANZANA 11>CARRERA 97AB 64AC 70<MANZANA 11>CARRERA 97AB 64AC 64<MANZANA 11>CARRERA 97AB 64AC 62(0201,0202)<MANZANA 11>CARRERA 97AB 64AC 60<LOTE 2 MANZANA 11>CARRERA 97AB 64AC 54 <MANZANA 11>CARRERA 97AB 64AC 52(0201,0202)<MANZANA 11>CARRERA 97AB 64AC 50 LOTE 3 MANZANA 11>CARRERA 97AB 64AC 44<MANZANA 11>CARRERA 97AB 64AC 42(0201,0202)<MANZANA 11>CARRERA 97AB 64AC 40 <LOTE 4 MANZANA 11>CARRERA 97AB 64AC 34<MANZANA 11>CARRERA 97AB 64AC 32(0201,0202)<MANZANA 11>CARRERA 97AB 64AC 30<LOTE 5 MANZANA 11>CARRERA 97AB 64AC 24 <MANZANA 11>CARRERA 97AB 64AC 22(0201,0202)<MANZANA 11>CARRERA 97AB 64AC 20<LOTE 6 MANZANA 11>CARRERA 97AB 64AC 14 <MANZANA 11>CARRERA 97AB 64AC 12(0201,0202)<MANZANA 11>CARRERA 97AB 64AC 10<LOTE 7 MANZANA 11>CARRERA 97AB 64AC 04<LOTE 8 MANZANA 11>CARRERA 97AB 64AC 02<LOTE 8 MANZANA 11>CARRERA 97AA 64AC 01<LOTE 9 MANZANA 11>CARRERA 97AA 64AC 03<LOTE 9 MANZANA 11>CARRERA 97AA 64AC 09 <LOTE 10 MANZANA 11>CARRERA 97AA 64AC 11<LOTE 10 MANZANA 11>CARRERA 97AA 64AC 17<MANZANA 11>CARRERA 97AA 64AC 19(0201,0202)<MANZANA 11>CARRERA 97AA 64AC 21 <LOTE 11 MANZANA 11>CARRERA 97AA 64AC 27 <MANZANA 11>CARRERA 97AA 64AC 29(0201,0202)<MANZANA 11>CARRERA 97AA 64AC 31<LOTE 12 MANZANA 11>CARRERA 97AA 64AC 37<MANZANA 11>CARRERA 97AA 64AC 39(0201,0202)<MANZANA 11>CARRERA 97AA 64AC 41 LOTE 13 MANZANA 11>CARRERA 97AA 64AC 47 <MANZANA 11>CARRERA 97AA 64AC 49(0201,0202)<MANZANA 11>CARRERA 97AA 64AC 51<LOTE 14 MANZANA 11>CARRERA 97AA 64AC 57 <MANZANA 11>CARRERA 97AA 64AC 59(0201,0202)<MANZANA 11>CARRERA 97AA 64AC 61<LOTE 15 MANZANA 11>CARRERA 97AA 64AC 67<MANZANA 11>CARRERA 97AA 64AC 69(0201,0202)<MANZANA 11>CARRERA 97AA 64AC 71 <LOTE 16 MANZANA 11>CARRERA 97AA 64AC 64<MANZANA 12>CARRERA 97AA 64AC 62(0201,0202)<MANZANA 12>CARRERA 97AA 64AC 60<LOTE 1 MANZANA 12>CARRERA 97AA 64AC 54<MANZANA 12>CARRERA 97AA 64AC 52(0201,0202)<MANZANA 12>CARRERA 97AA 64AC 50<LOTE 2 MANZANA 12>CARRERA 97AA 64AC 44<MANZANA 12>CARRERA 97AA 64AC 42(0201,0202)<MANZANA 12>CARRERA 97AA 64AC 40<LOTE 3 MANZANA 12>CARRERA 97AA 64AC 34<MAZANA 12>CARRERA 97AA 64AC 32(0201,0202)<MANZANA 12>CARRERA 97AA 64AC 30<LOTE 4 MANZANA 12>CARRERA 97AA 64AC 24<MANZANA 12>CARRERA 97AA 64AC 22(0201,0202)<MANZANA 12>CARRERA 97AA 64AC 20<LOTE 5 MANZANA 12>CARRERA 97AA 64AC 14<MANZANA 12>CARRERA 97AA 64AC 12(0201,0202)<MANZANA 12>CARRERA 97AA 64AC 10<LOTE 6 MANZANA 12>CARRERA 97A 64AC 09<MANZANA 12>CARRERA 97A 64AC 11(0201,0202)<MANZANA 12>CARRERA 97A 64AC 13<LOTE 7 MANZANA 12>CARRERA 97A 64AC 19 <MANZANA 12>CARRERA 97A 64AC 21(0201,0202)<MANZANA 12>CARRERA 97A 64AC 23<LOTE 8 MANZANA 12>CARRERA 97A 64AC 29<MANZANA 12>CARRERA 97A 64AC 31(0201,0202)<MANZANA 12>CARRERA 97A 64AC 33<LOTE 9 MANZANA 12>CARRERA 97A 64AC 39 <MANZANA 12>CARRERA 97A 64AC 41(0201,0202)<MANZANA 12>CARRERA 97A 64AC43<LOTE 10 MANZANA 12>CARRERA 97A 64AC 49<MANZANA 12>CARRERA 97A 64AC 51(0201,0202)<MANZANA 12>CARRERA 97A 64AC 53<LOTE 11 MANZANA 12>CARRERA 97A 64AC 59<MANZANA 12>CARRERA 97A 64AC 61(0201,0202)<MANZANA 12>CARRERA 97A 64AC 63<LOTE 12 MANZANA 1",
                      "<CL 96A 81 46>;<CL 96A 81 42>",
                      "<VIVIENDA: SEGUNDO PISO> Calle 86 93A 64;<PRIMER PISO> Calle 86 93A 66 <BARRIO ROBLEDO>",
                      "<TORRE 2>;Calle 8 84B 65 <0214-1314,0915,1015,1315,0316-0816,",
                      "CarreRa 9D 44E 40 <VIVIENDA PISO 1>;Carrera 9C 44E 39 <VIVIENDA PISO 2>;Carrera 9C 44E 43 (0201,0202) <VIVIENDA PISO 3>",
                      "CarRera 84 22 75 <VIVIENDA>;Carrera 84 22 77 (201,301) <VIVIENDA>",
                      "Carrera 90 44A 11(0201-1301,0202-1302,0203-1303,0204-1304)<VIVIENDA>;Carrera 90 44A 05<LOCAL>;Carrera 90 44A 17(01035-01037)<PARQUEADERO CARRO>;Calle 44A 90 10(99021-99029)<PARQUEADERO CARRO>;Carrera 90 44A 17(01021-01034)<PARQUEADERO MOTO>",
                      "Calle 42 27 32;Calle 42 27 30 (0201-0401,0202)",
                      "Carrera 68A 103 17 <PARQUEADERO>;Carrera 68A 103 23 (0101-0301,0302)",
                      "Carrera 80E 40 92 (0101,0201,0202,0301,0302);Carrera 80E 40 94",
                      "<VEREDA EL CERRO DEL CORREGIMIENTO DE SANTA ELENA>",
                      "Calle 80 50B 37",
                      "",
                      "<CL 96A 81 46>;<CL 96A 81 42>",
                      "<CL 94 C 84B 10>",
                      "Circular 29 40A 20(0116,0219,030170417)",
                      "<TORRE 2>;Calle 8 84B 65 <0214-1314,0915,1015,1315,0316-0816, 1016-1316, 0217-1317, 0218-118,1318,0219,0419,1219,1319>;<TORRE 3>;Calle 8 84B 65 <0208-0608,1008,1208-1408,0209-1409,0710-0910,1210-1410, 0211-0911,1111-1411,0212-1412,0413-0613,1013,1213-1413>;<TORRE 4>;Calle 8 84B 65 <0201-1401,0202-1402,0203-1403, 0204-1404,0205-1405,0206-1406>;<PISO 1>;<TORRE 2,3,4>;Calle 8 84B 65 <1-105><PARQUEADERO>;Calle 8 84B 65 <1-17><UTILES>;<SOTANO 1>;<TORRE 2,3,4>;Calle 8 84B 65 <141-238><PARQUEADERO>;Calle 8 84B 65 <36-68><UTILES>;<SOTANO 2>;<TORRE 2,3,4>;Calle 8 84B 65 <95-195><UTILES>;<TORRE 1>;Calle 8 84B 65 <0220-1420, 0221-1421,0222-1422,0223-1423,0224-1424,0225-1425>;Calle 8 84B 65 <02031-14031,02032-14032,02033- 14033><UTILES>"]

direccion_estandarizada = limpiar_direccion(direccion_original2)
direccion_modificada = []

for direccion in direccion_estandarizada:
    for patron, reemplazo in sustituciones.items():
        direccion = re.sub(patron, reemplazo, direccion)
    direccion_modificada.append(direccion)

nueva_direccion = borrar_entre(direccion_modificada)

nueva_direccion2 = borrar_direccion_repetida(nueva_direccion)


#for direccion in nueva_direccion:
print(nueva_direccion2)
