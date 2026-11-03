import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions2 import (
    load_data,
    extract_column,
    column_mapper_1,
    shuffle_and_sort,
    parse_column,
    parse_to_one_column,
    reducer
)
def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    data = load_data()
    column = extract_column(4, data)
    parsed_column = parse_column(column, ",")
    stuck_column = parse_to_one_column(parsed_column)
    content = parse_column(stuck_column, ":")
    registers = extract_column(0, content)
    content = column_mapper_1(registers)
    content = shuffle_and_sort(content)
    content = reducer(content, return_dict= True)
    return content

print(pregunta_09())

