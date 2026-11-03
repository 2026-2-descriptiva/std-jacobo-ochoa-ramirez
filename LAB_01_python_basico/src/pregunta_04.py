
from functions import column_mapper_1, extract_column, load_data, reducer, shuffle_and_sort


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """

    dates = extract_column(2, load_data())
    months = []

    for date in dates:
        parts = date.strip().split("-")
        if len(parts) >= 2 and parts[1].isdigit():
            months.append(parts[1].zfill(2))

    return shuffle_and_sort(reducer(column_mapper_1(months)))

print(pregunta_04())