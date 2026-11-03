from functions2 import load_data

def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """
    data = load_data()

    colSum = 0
    for row in data:
        colSum += int(row[1])

    return colSum


print(pregunta_01())