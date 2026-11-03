
from functions import load_data, extract_multiple_columns, column_mapper_2, max_min_reducer, shuffle_and_sort


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    letters, values = extract_multiple_columns((0, 1), load_data())
    pairs = column_mapper_2(letters, values)
    result = max_min_reducer(pairs)
    return shuffle_and_sort(result)

print(pregunta_05())