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
"""
cadena = "Calle 68 ENTRE LAS CARRERAS 44 Y 45 H.N. MANRIQUE"
borrar_palabras = ["Y"]

palabras = cadena.split()
if 'ENTRE' in palabras:
    indice_entre = palabras.index('ENTRE')
    if 'CARRERAS' in palabras:
        indice_carreras = palabras.index('CARRERAS')
        palabras[indice_entre:indice_carreras + 1] = ['']
    elif 'CALLES' in palabras:
        indice_calles = palabras.index('CALLES')
        palabras[indice_entre:indice_calles + 1] = ['']

if 'Y' in palabras:
    indice_y = palabras.index('Y')
    palabras = palabras[:indice_y]

direccion_final = ' '.join(palabra for palabra in palabras if palabra)
print(direccion_final)



