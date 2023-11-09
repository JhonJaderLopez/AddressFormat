"""
import re

def estandarizar_direccion(direccion):
    # Definir un patrón de expresión regular que coincide con "CR," "CL," "TV," "CQ," "SUR," "NORTE", combinaciones alfanuméricas como "80A", "10E" o "5D", y también con combinaciones numéricas como "123"
    patron = r'\b(?:CR|CL|TV|CQ|SUR|NORTE|\d{2,3}[A-Z]|\d{1}[A-Z]|\d{1,3})\b'

    # Dividir la dirección en palabras
    palabras = direccion.split()

    # Inicializar una lista vacía para las palabras que cumplen con el patrón
    palabras_filtradas = []

    # Recorrer cada palabra y verificar si cumple con el patrón
    for palabra in palabras:
        if re.search(patron, palabra):
            palabras_filtradas.append(palabra)
    direccion_estandarizada = ' '.join(palabras_filtradas)

    return direccion_estandarizada

# Ejemplo de uso
direcciones = ["CL 5D 10E 170 SAN ANTONINO DE PRADO", "CR 80A 32 73 URBANIZACION NUEVA VILLA ABURRA","170 METROS APROXIMADAMENTE DE LA CARRETERA MEDELLIN ENVIGADO HACIA EL ESTE ENTRANDO POR EL FRENTE A LA FINCA CHIPRE"]
for direccion in direcciones:
    direccion_estandarizada = estandarizar_direccion(direccion)
    print(direccion_estandarizada)




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



    cadena = "CL 32A 76A 32 CL 32A 76A 34 CL 32A 76A 36"

# Dividimos la cadena en palabras
palabras = cadena.split()

# Contadores para las coincidencias
coincidencias = 0

# Lista para almacenar las palabras válidas
palabras_validas = []

for palabra in palabras:
    if palabra in ["CL", "CR", "TV"]:
        coincidencias += 1
        if coincidencias == 2:
            break  # Detenemos el proceso si encontramos la segunda coincidencia
    palabras_validas.append(palabra)

# Ahora puedes unir las palabras válidas en una cadena nuevamente
resultado = ' '.join(palabras_validas)
print(resultado)



#cadena = "CL 93A 83A 04-06-10-12-16-18-22-24-28-30-34-36-40-42-46-48-52-54-58-60-64-66-70-72-76-78-82-84-88-90-94-96-100"

import re

# Definir la cadena de entrada
cadena = "CL 93A 83A 04-06"

# Usar una expresión regular para encontrar el patrón
patron = r'\d{2,3}-'

# Buscar la primera coincidencia del patrón en la cadena
match = re.search(patron, cadena)

if match:
    # Obtener la posición de inicio de la coincidencia
    posicion_inicio = match.start()

    # Cortar la cadena desde el principio hasta la posición de inicio
    nueva_cadena = cadena[:posicion_inicio]
else:
    # Si no se encontró ninguna coincidencia, la nueva cadena es la misma que la cadena original
    nueva_cadena = cadena

print(nueva_cadena)


# Definir la cadena de entrada
# #"CL 93A 83A 04-06-10-12-16-18-22-24-28-30-34-36-40-42-46-48-52-54-58-60-64-66-70-72-76-78-82-84-88-90-94-96-100"

# Definir la cadena de entrada

lista = ["Carrera 45A 102 11(106) <PRIMER PISO>",
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

for elemento in lista:
    elementos = elemento.split(";")
    
    print(elementos)



    
direccion_original2 = [
                       "Carrera 70<ENTRE> Calle 29A<Y>30<ESQUINA ESTE>",
                       "Carrera 54<ENTRE> Avenida<ORIENTAL Y> CALLE 58A",
                       "Carrera 85<ENTRE> Calle 34A<Y>35",
                       "Calle 54<CON> Carrera 38<ESQUINA",
                       "Calle 49 <25 Y 20 90>",
                       "Calle 68<con> Carrera 85",
                       "<Carrera 29A Calle 40 Y 41>",
                       "Carrera 80C Calle 33 <LOTE 9 MZ 26>"]

"""
cadena = "hola como estas"
lista = [cadena]
print (lista)





















