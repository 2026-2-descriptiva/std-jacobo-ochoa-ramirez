import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions2 import (
        load_data,
        extract_multiple_columns,
        parse_column
)

def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    
    data = load_data()
    column_1, column_4, column_5 = extract_multiple_columns([0, 3, 4], data)
    parsed_column_4 = parse_column(column_4, ",")
    parsed_column_5 = parse_column(column_5, ",")

    return [(column_1[indx], len(parsed_column_4[indx]), len(parsed_column_5[indx])) for indx in range(len(column_1))]

print(pregunta_10())

