import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions2 import (
    load_data,
    column_mapper_3,
    shuffle_and_sort,
    reducer_2,
    extract_multiple_columns
)
def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """

    
    data = load_data()
    column_2, column_1 = extract_multiple_columns(range(2), data)
    content = column_mapper_3(column_1, column_2)
    content = shuffle_and_sort(content)
    content = reducer_2(content)
    return content

print(pregunta_07())
