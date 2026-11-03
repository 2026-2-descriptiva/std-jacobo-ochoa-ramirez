
from functions import (
    column_mapper_2,
    extract_multiple_columns,
    load_data,
    reducer,
    shuffle_and_sort,
)


def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    letters, values = extract_multiple_columns([0, 1], load_data())
    mapped_data = column_mapper_2(letters, values)
    return shuffle_and_sort(reducer(mapped_data))

print(pregunta_03())