import re

direcciones = [
    "CR 70 117 19CARRERA",
    "CL 101C 76A 49CALLE",
    "CL 94D 83AC 36CALLE",
]

# Expresión regular para encontrar "CALLE" o "CARRERA" y capturar todo antes de ellos
pattern = re.compile(r'^(.*?)(CALLE|CARRERA)')

for direccion in direcciones:
    match = re.search(pattern, direccion)
    if match:
        inicio_direccion = match.group(1)
        print(inicio_direccion)

