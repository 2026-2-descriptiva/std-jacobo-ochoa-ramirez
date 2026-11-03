import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions2 import (
    load_data,
    extract_multiple_columns,
    parse_column,
    parse_to_one_column_with_value,
    shuffle_and_sort,
    reducer,
    format_for_question_12
)


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    data = load_data()
    column_1, column_5 = extract_multiple_columns([0, 4], data)
    parsed_column_5 = parse_column(column_5, ",")

    content = parse_to_one_column_with_value(parsed_column_5, column_1, (lambda x: x))
    content = format_for_question_12(content)
    content = shuffle_and_sort(content)
    content = reducer(content, return_dict=True)
    return content

print(pregunta_12())