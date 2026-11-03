"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions2 import  (
    load_data,
    extract_column,
    column_mapper_1,
    shuffle_and_sort,
    reducer
)

def pregunta_02():
    """
    


    """

    data = load_data()
    column = extract_column(0, data)
    content = column_mapper_1(column)
    content = shuffle_and_sort(content)
    content = reducer(content)
    return content

pregunta_02()