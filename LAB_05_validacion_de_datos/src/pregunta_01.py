from pathlib import Path
import json
import re
import pandas as pd

def load_data():
    data_path = Path(__file__).resolve().parents[1] / "data" / "ventas.csv.gz"
    return pd.read_csv(data_path, compression="gzip")



def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    df = load_data()
    df.columns = [
        re.sub(r"\s+", "_", str(column).lstrip("\ufeff").strip().lower())
        for column in df.columns
    ]

    required_columns = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email",
    ]
    missing_required_columns = sorted(
        set(required_columns) - set(df.columns)
    )
    unexpected_columns = sorted(set(df.columns) - set(required_columns))

    missing_value_count_by_column = {
        column: int(
            df[column].isna().sum()
            + df[column].astype("string").str.strip().eq("").sum()
        )
        for column in df.columns
    }

    report = {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": int(df.duplicated().sum()),
        "duplicate_supplier_id_row_count": 0,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": 0,
        "invalid_unit_count": 0,
        "country_values": [],
    }

    if "supplier_id" in df.columns:
        report["duplicate_supplier_id_row_count"] = int(
            df["supplier_id"].duplicated(keep=False).sum()
        )

    if "contact_email" in df.columns:
        email_values = df["contact_email"].astype("string")
        valid_email = email_values.str.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", na=False
        )
        report["invalid_email_count"] = int((~valid_email).sum())

    if "units" in df.columns:
        units = pd.to_numeric(df["units"], errors="coerce")
        present_units = df["units"].notna()
        valid_units = units.notna() & (units > 0) & (units % 1 == 0)
        report["invalid_unit_count"] = int(
            (present_units & ~valid_units).sum()
        )

    if "country" in df.columns:
        report["country_values"] = sorted(
            df["country"].dropna().unique().tolist()
        )

    output_path = (
        Path(__file__).resolve().parents[1]
        / "submission"
        / "data_quality_report.json"
    )
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report
