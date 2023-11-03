import re
import pandas as pd
import openpyxl

##realizar caso por caso, limpiar un caso y despues el otro
sustituciones = {
    r'\bCARRERA\b': 'CR',
    r'\bCALLE\b': 'CL',
    r'\bCIRCULAR\b': 'CQ',
    r'\bTRANSVERSAL\b': 'TV',
    r'\bDIAGONAL\b': 'DG',
    r'\bAVENIDA\b': 'AV',
}

palabras_clave = {"CARRERA", "CALLE", "CIRCULAR", "TRANSVERSAL", "DIAGONAL","AVENIDA","DG", "CL", "CR","TV","CQ","AV"}
borrar_palabras = {"CARRERA", "CALLE", "CIRCULAR", "TRANSVERSAL", "DIAGONAL","AVENIDA" ,"DG","CL", "CR","TV","CQ","AV","CARRERAS","CALLES","CARREREA"}
eliminar_caracteres = {";",",","<",">","/","&"}

def reemplazo(match):
    return sustituciones[match.group()]

def vaciar_invalidas(direcciones):
    direccion_limpia = []
    for direccion in direcciones:
        if direccion in palabras_clave:
            direccion = ""
            direccion_limpia.append(direccion)
        else:
            direccion_limpia.append(direccion)

    return direccion_limpia
def contar_palabras(cadena):
    palabras = re.findall(r'\S+', cadena)
    return len(palabras)
def borrar_repetido(direcciones):
    direccion_limpia = []
    direccion_corta = []
    for direccion in direcciones:
        
        cadenas_separadas = direccion.split(';')
        # Inicializar variables para realizar un seguimiento de la cadena más larga y su longitud
        cadena_mas_larga = ""
        longitud_mas_larga = 0
        # Iterar a través de las cadenas separadas
        for cadena in cadenas_separadas:
            num_palabras = contar_palabras(cadena)
            if num_palabras > longitud_mas_larga:
                longitud_mas_larga = num_palabras
                cadena_mas_larga = cadena
        direccion_corta.append(cadena_mas_larga)
        #nueva_direccion= ' '.join(direccion_corta)        
    #direccion_limpia.append(nueva_direccion)
    return direccion_corta

def borrar_repetido_separada(direcciones):
    direccion_limpia = []
    for direccion_larga in direcciones:
        direccion_corta = []
        direccion_separada = direccion_larga.split(";")
        for direccion in direccion_separada:

            if direccion.strip() == "":
                direccion_corta.append(direccion)
                #VALIDAR SI EMPIEZA CON UN NUMERO U OTRO CARACTER
            else:
                # Dividimos la cadena en palabras
                palabras = direccion.split()
                if palabras[0] not in palabras_clave:
                    direccion= ""
                    direccion_limpia.append(direccion)
                else:
                        
                    # Contadores para las coincidencias
                    coincidencias = 0

                    # Lista para almacenar las palabras válidas
                    palabras_validas1 = []
                    palabras_validas2 = []


                    for palabra in palabras:
                        if palabra in borrar_palabras:
                            coincidencias += 1
                            #CALLE 23
                        if coincidencias == 1:
                            palabras_validas1.append(palabra)
                        if coincidencias == 2 and len(palabras_validas1)<3:
                            palabras_validas2.append(palabra)
                            palabras_validas1 = [] #"CALLE CARRERA 91C", ""
                        if coincidencias == 3:
                            break

                    if len(palabras_validas1) > 0:
                        resultado = ' '.join(palabras_validas1)
                    elif len(palabras_validas2) > 0:
                        resultado = ' '.join(palabras_validas2)
                        #ayer estaba tratando de vaciar la ultima lista cuando coincidencias ees = 2, revisar

                        #tengo que tener en cuenta 2 casos: cuando la correcta es la segunda coincidencia y cuando es la primera
                        #porque la larga puede ser la 1 o la 2, porque sino puedo borrar la corecta o incluso dejar vacio 

                        # Ahora puedes unir las palabras válidas en una cadena nuevamente
                    direccion_corta.append(resultado)
        nueva_direccion= ';'.join(direccion_corta)        
        direccion_limpia.append(nueva_direccion)
    return direccion_limpia

def eliminar_palabras(direcciones):
    direccion_limpia =[]
    for direccion_larga in direcciones:
        direccion_corta = []
        direccion_separada= direccion_larga.split(";")
        for direccion in direccion_separada:
            # Definir un patrón de expresión regular que coincide con "CR," "CL," "TV," "CQ," "SUR," "NORTE", combinaciones alfanuméricas como "80A", "10E" o "5D", y también con combinaciones numéricas como "123"
            #patron = r'\b(?:CR|CL|TV|CQ|SUR|NORTE|\d{2,3}[A-Z]|\d{1}[A-Z]|\d{1,3})\b'
            #patron = r'\b(?:CR|CL|TV|CQ|AV|SUR|NORTE|\d{1,3}(?:[A-Z]{1,2})?)\b'
            #patron = r'\b(?:CR|CL|TV|CQ|AV|SUR|NORTE|\d{1,3}(?:[A-Z]{1,2}|\d{1,4}[A-Z]{1,4})?)\b'
            patron = r'\b(?:CR|CL|TV|CQ|AV|DG|SUR|ESTE|\d{1,3}(?:[A-Z]{1,4})?)\b'
            # Dividir la dirección en palabras
            palabras = direccion.split()

            # Inicializar una lista vacía para las palabras que cumplen con el patrón
            palabras_filtradas = []

            # Recorrer cada palabra y verificar si cumple con el patrón
            encontrado = False
            for palabra in palabras:
                
                if re.search(patron, palabra) and encontrado == False:
                    palabras_filtradas.append(palabra)
                else:
                    encontrado = True
            direccion_estandarizada = ' '.join(palabras_filtradas)
            direccion_corta.append(direccion_estandarizada)
        nueva_direccion= ';'.join(direccion_corta)        
        direccion_limpia.append(nueva_direccion)
    return direccion_limpia

def borrar_union(direcciones):
    direccion_limpia=[]
    # Expresión regular para encontrar "CALLE" o "CARRERA" y capturar todo antes de ellos
    pattern = re.compile(r'^(.*?)(CALLE|CARRERA|TORRE|PARQUEADERO)')

    for direccion_larga in direcciones:
        direccion_corta = []
        direccion_separada = direccion_larga.split(";")
        for direccion in direccion_separada:
            match = re.search(pattern, direccion)
            if match:
                inicio_direccion = match.group(1)
                direccion_corta.append(inicio_direccion)
            else:
                direccion_corta.append(direccion)
        nueva_direccion= ';'.join(direccion_corta)        
        direccion_limpia.append(nueva_direccion)
    return direccion_limpia

def borrar_entre(direcciones):
    
    direccion_limpia = []

    for direccion_larga in direcciones:
        direcciones_estandarizadas = []
        direccion_final = ""
        direccion_separada = direccion_larga.split(";")
        #print(direccion_separada)
        for direccion in direccion_separada:
            #palabras = ""
            palabras = direccion.split()
            #print(palabras)
            if 'ENTRE' in palabras or 'POR' in palabras or 'CON' in palabras or 'CRUCERO' in palabras:
                if 'ENTRE' in palabras:
                    indice_entre = palabras.index('ENTRE')
                    if indice_entre > 0 and (indice_entre + 1) < len(palabras) and palabras[indice_entre + 1] in borrar_palabras:
                        palabras[indice_entre:indice_entre + 2] = ['']
                        if 'Y' in palabras[indice_entre:]:
                            indice_y = palabras.index('Y', indice_entre)
                            palabras = palabras[:indice_y]
                        if 'Y' in palabras:   #CR 45 ENTRE CALLES 12 Y 13
                            palabras = [palabra for palabra in palabras if palabra != 'Y']
                    elif indice_entre > 0 and (indice_entre + 2) < len(palabras) and palabras[indice_entre + 2] in borrar_palabras:
                        palabras[indice_entre:indice_entre + 3] = ['']
                        if 'Y' in palabras[indice_entre:]:
                            indice_y = palabras.index('Y', indice_entre)
                            palabras = palabras[:indice_y]
                        if 'Y' in palabras:   #CR 45 ENTRE CALLES 12 Y 13
                            palabras = [palabra for palabra in palabras if palabra != 'Y']
                    elif indice_entre > 0 and (indice_entre) < len(palabras):
                        palabras[indice_entre:indice_entre + 1] = ['']
                        if 'Y' in palabras[indice_entre:]:
                            indice_y = palabras.index('Y', indice_entre)
                            palabras = palabras[:indice_y]
                        if 'Y' in palabras:   #CR 45 ENTRE CALLES 12 Y 13
                            palabras = [palabra for palabra in palabras if palabra != 'Y']
                if 'POR' in palabras:
                    indice_entre = palabras.index('POR')
                    if indice_entre > 0 and (indice_entre + 1) < len(palabras) and palabras[indice_entre + 1] in borrar_palabras:
                        palabras[indice_entre:indice_entre + 2] = ['']
                        if 'Y' in palabras[indice_entre:]:
                            indice_y = palabras.index('Y', indice_entre)
                            palabras = palabras[:indice_y]
                        if 'Y' in palabras:
                            palabras = [palabra for palabra in palabras if palabra != 'Y']
                    elif indice_entre > 0 and (indice_entre + 2) < len(palabras) and palabras[indice_entre + 2] in borrar_palabras:
                        palabras[indice_entre:indice_entre + 3] = ['']
                        if 'Y' in palabras[indice_entre:]:
                            indice_y = palabras.index('Y', indice_entre)
                            palabras = palabras[:indice_y]
                        if 'Y' in palabras:   #CR 45 ENTRE CALLES 12 Y 13
                            palabras = [palabra for palabra in palabras if palabra != 'Y']
                if 'CRUCERO' in palabras:
                    indice_entre = palabras.index('CRUCERO')
                    if indice_entre > 0 and (indice_entre + 1) < len(palabras) and palabras[indice_entre + 1] in borrar_palabras:
                        palabras[indice_entre:indice_entre + 2] = ['']
                        if 'Y' in palabras[indice_entre:]:
                            indice_y = palabras.index('Y', indice_entre)
                            palabras = palabras[:indice_y]
                        if 'Y' in palabras:
                            palabras = [palabra for palabra in palabras if palabra != 'Y']
                    elif indice_entre > 0 and (indice_entre + 2) < len(palabras) and palabras[indice_entre + 2] in borrar_palabras:
                        palabras[indice_entre:indice_entre + 3] = ['']
                        if 'Y' in palabras[indice_entre:]:
                            indice_y = palabras.index('Y', indice_entre)
                            palabras = palabras[:indice_y]
                        if 'Y' in palabras:   #CR 45 ENTRE CALLES 12 Y 13
                            palabras = [palabra for palabra in palabras if palabra != 'Y']
                    elif indice_entre > 0 and (indice_entre + 3) < len(palabras) and palabras[indice_entre + 3] in borrar_palabras:
                        palabras[indice_entre:indice_entre + 4] = ['']
                        if 'Y' in palabras[indice_entre:]:
                            indice_y = palabras.index('Y', indice_entre) #Carrera 29 <CRUCERO CON LA CALLE 59 ESQ. N.E.>
                            palabras = palabras[:indice_y]
                        if 'Y' in palabras:   #CR 45 ENTRE CALLES 12 Y 13
                            palabras = [palabra for palabra in palabras if palabra != 'Y']
                if 'CON' in palabras:
                    indice_entre = palabras.index('CON')
                    if indice_entre > 0 and (indice_entre + 1) < len(palabras) and palabras[indice_entre + 1] in borrar_palabras:
                        palabras[indice_entre:indice_entre + 2] = ['']
                        if 'Y' in palabras[indice_entre:]:
                            indice_y = palabras.index('Y', indice_entre)
                            palabras = palabras[:indice_y]
                        if 'Y' in palabras:
                            palabras = [palabra for palabra in palabras if palabra != 'Y']
                    elif indice_entre > 0 and (indice_entre + 2) < len(palabras) and palabras[indice_entre + 2] in borrar_palabras:
                        palabras[indice_entre:indice_entre + 3] = ['']
                        if 'Y' in palabras[indice_entre:]:
                            indice_y = palabras.index('Y', indice_entre)
                            palabras = palabras[:indice_y]
                        if 'Y' in palabras:   #CR 45 ENTRE CALLES 12 Y 13
                            palabras = [palabra for palabra in palabras if palabra != 'Y']

                direccion_final = ' '.join(palabra for palabra in palabras if palabra)
                direcciones_estandarizadas.append(direccion_final.strip())
                #print(direcciones_estandarizadas)
            else:
                direccion_final = ' '.join(palabra for palabra in palabras if palabra)
                direcciones_estandarizadas.append(direccion_final.strip())
        nueva_direccion= ';'.join(direcciones_estandarizadas)        
        direccion_limpia.append(nueva_direccion)
    return direccion_limpia
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
    direccion_split = []

    for direccion_larga in direcciones:
        
        direccion_corta = []
        encontrado = False
        direccion_split = str.upper(direccion_larga)
        direcciones = direccion_split.split(";")
        for direccion in direcciones:
            nueva_cadena = ""
            #print(direccion)
            if direccion.strip() == "":
                
                direccion_corta.append(direccion)
            elif direccion =="NAN" or direccion=="NULL":
                direccion = ""
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
                        #otro split 
                        # union = ",".join(parte_anterior)***no se le hace join
                        # parte_anterior2 = union.split(">", 1)[0]
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
                                if caracter in eliminar_caracteres:
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
                            if caracter in eliminar_caracteres:
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
                                if caracter in eliminar_caracteres:
                                    encontrado = True
                                if not encontrado:
                                    nueva_cadena += caracter
                            direccion_corta.append(nueva_cadena)
                        else :
                                contenido = ""
                                direccion_corta.append(contenido)  
                    else :
                        contenido = ""
                        direccion_corta.append(contenido)   

            else:
                dire_upper = str.upper(direccion)
                direccion_split = dire_upper.split()
                direccion_unida= ""
                
                if direccion_split[0] in palabras_clave:
                    direccion_unida = " ".join(direccion_split)

                    if "<ENTRE" in direccion_unida or "<POR" in direccion_unida or "<CON" in direccion_unida or "<CRUCERO" in direccion_unida:
                        cadena_nueva = direccion_unida.replace("<ENTRE", "ENTRE").replace("<POR", "POR").replace("<CON","CON").replace("<CRUCERO","CRUCERO").replace(">", "")
                        
                        direccion_sin_caracteres = re.compile(r'<[^>]+>')
                        cadena_sin_contenido = direccion_sin_caracteres.sub('', cadena_nueva)
                        contenido_entre_parentesis = re.compile(r'\([^)]+\)')

                        cadena_sin_parentesis = contenido_entre_parentesis.sub('', cadena_sin_contenido)

                        for caracter in cadena_sin_parentesis:
                            if caracter in eliminar_caracteres:
                                encontrado = True
                            if not encontrado:
                                nueva_cadena += caracter
                    else:
                        direccion_sin_caracteres = re.compile(r'<[^>]+>')
                        cadena_sin_contenido = direccion_sin_caracteres.sub('', dire_upper)
                        contenido_entre_parentesis = re.compile(r'\([^)]+\)')

                        cadena_sin_parentesis = contenido_entre_parentesis.sub('', cadena_sin_contenido)

                        for caracter in cadena_sin_parentesis:
                            if caracter in eliminar_caracteres:
                                encontrado = True
                            if not encontrado:
                                nueva_cadena += caracter
                        
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
                        if caracter in eliminar_caracteres:
                            ##if caract < equivale al primer caracter ejecute otra funcion que verifica si la informacion contenida si es valida
                            encontrado = True
                        if not encontrado:
                            nueva_cadena += caracter
                    direccion_corta.append(nueva_cadena)
        nueva_direccion= ';'.join(direccion_corta)        
        direccion_limpia.append(nueva_direccion)
    return direccion_limpia

direccion_original2 = ["Carrera 45A 102 11(106) <PRIMER PISO>",
        "<Calle Bolivar entre la terminal del Tranvia del Sur>",
        "Calle 48 92B 17 <ANTERIOR>;Calle 47F 92B 08 (201,301) <ACTUAL>",
        "Calle 13 37 46 <ACTUAL>;Calle 13 37 50 <ACTUAL>",
        "Carrera 50BB 87 24 <ANTERIOR>;Carrera 50BB 87 26 (201,202)",
        "Calle 96 <ENTRE LAS CARRERAS 47 Y 48 H.N. >",
        "<calle San Juan media cuadra abajo de Lepelin>",
        "Carrera 42B 101 33 <PIRMER PISO>",
        "Carrera 52 55 11;Carrera 52 55 15;Carrera 52 55 19 ;Carrera 52 55 23 Calle;Carrera 52 55 27;Carrera 52 55 03;Calle 55 52 08;Calle 55 52 16;Calle 55 52 20",
        "Calle 92EE 71 56 <2PISO>",
        "Carrera 79 49 76;Carrera 79 49 60",
        "Carrera 71 92BB 49 <PRIMER PISO>",
        "Calle 76 48A 82",
        "Calle 15 <ENTRE LAS CARRERAS 75 Y 76 H.S. EL RINCON>",
        "Calle 39 36A 19 <ACTUAL>",
        "<Calle Luciano Restrepo entre Carrera basti y Boleras>",
        "Calle 56E 17A 01",
        "Calle 2A <ENTRE LAS CARRERAS 86 Y 87 H.S. BELEN>",
        "<Plazuela Independencia entrando occidental>",
        "Carrera 30 <ENTRE LAS CALLES 46 Y 47 H.W. BUENOS AIRES>",
        "Calle 51 33 67 (142);Calle 51 33 67 (141)",]

direccion_estandarizada = limpiar_direccion(direccion_original2)

direccion_modificada = []

for direccion in direccion_estandarizada:
    for patron, reemplazo in sustituciones.items():
        direccion = re.sub(patron, reemplazo, direccion)
    direccion_modificada.append(direccion)

direccion_sin_cruce = borrar_entre(direccion_modificada) 
direccion_limpia = borrar_union(direccion_sin_cruce)

direccion_sin_palabras = eliminar_palabras(direccion_limpia)
#print(direccion_sin_palabras)
direccion_sin_repetir_separada = borrar_repetido_separada(direccion_sin_palabras)
#print(direccion_sin_repetir_separada)
direccion_sin_repetir= borrar_repetido(direccion_sin_repetir_separada)
#print(direccion_sin_repetir)
direccion_vacia = vaciar_invalidas(direccion_sin_repetir)


#for direccion in nueva_direccion:
print(direccion_vacia)
