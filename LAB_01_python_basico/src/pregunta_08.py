import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions2 import (
    load_data,
    column_mapper_3,
    shuffle_and_sort,
    reducer_3,
    extract_multiple_columns
)


def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    data = load_data()
    column_2, column_1 = extract_multiple_columns(range(2), data)
    content = column_mapper_3(column_1, column_2)
    content = shuffle_and_sort(content)
    content = reducer_3(content)
    return content

print(pregunta_08())