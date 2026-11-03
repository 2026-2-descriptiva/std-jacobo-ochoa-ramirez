import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions import (
    load_data,
    extract_multiple_columns,
    parse_column,
    parse_to_one_column_with_value,
    shuffle_and_sort,
    reducer
)


def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    data = load_data()
    column_1, column_4 = extract_multiple_columns([1, 3], data)
    parsed_column_4 = parse_column(column_4, ",")

    content = parse_to_one_column_with_value(parsed_column_4, column_1)
    content = shuffle_and_sort(content)
    content = reducer(content, return_dict= True)
    return content
    
print(pregunta_11())