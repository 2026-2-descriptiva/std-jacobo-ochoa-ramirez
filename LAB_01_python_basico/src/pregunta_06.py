

from functions2 import (
    extract_column,
    load_data,
    max_min_reducer,
    parse_column,
    parse_to_one_column,
)


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    data = load_data()
    metrics = extract_column(4, data)
    metric_pairs = parse_to_one_column(parse_column(metrics, ","))

    key_values = []
    for pair in metric_pairs:
        key, value = pair.split(":", 1)
        key_values.append((key, int(value)))

    result = max_min_reducer(key_values, reversed=True)
    return sorted(result, key=lambda item: item[0])

print(pregunta_06())