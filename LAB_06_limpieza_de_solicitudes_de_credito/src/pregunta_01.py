import pandas as pd
from pathlib import Path

def load_data():
    data_path = Path(__file__).resolve().parents[1] / "data" / "solicitudes_de_credito.csv.gz"
    return pd.read_csv(data_path, sep=";", index_col=0, compression="gzip")



def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    df = load_data()
    
    text_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]

    for column in text_columns:
        df[column] = df[column].str.lower()
        df[column] = df[column].str.strip()
        df[column] = df[column].str.replace(r"[\_\-]", " ", regex=True)
        df[column] = df[column].str.replace(",", "")
        if column not in ("barrio", "línea_credito"):
            df[column] = df[column].str.replace(".", "")
        df[column] = df[column].str.replace(r"\s+", " ", regex=True)
        df[column] = df[column].str.strip()

    df["estrato"] = pd.to_numeric(df["estrato"], errors="coerce").astype("Int64")
    df["comuna_ciudadano"] = pd.to_numeric(df["comuna_ciudadano"], errors="coerce")
    df["monto_del_credito"] = pd.to_numeric(
        df["monto_del_credito"]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .str.replace(r"\.00$", "", regex=True)
        .str.replace(r"\.0$", "", regex=True),
        errors="coerce",
    ).astype("Int64")

    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    ).combine_first(
        pd.to_datetime(
            df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce"
        )
    ).combine_first(
        pd.to_datetime(df["fecha_de_beneficio"], format="%Y-%m-%d", errors="coerce")
    )
    
    df = df.drop_duplicates()
    required_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]
    df = df.dropna(subset=required_columns)

    output_path = (
        Path(__file__).resolve().parents[1]
        / "submission"
        / "solicitudes_de_credito.csv"
    )
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].dt.strftime("%Y-%m-%d")
    df = df[
        [
            "sexo",
            "tipo_de_emprendimiento",
            "idea_negocio",
            "barrio",
            "estrato",
            "comuna_ciudadano",
            "fecha_de_beneficio",
            "monto_del_credito",
            "línea_credito",
        ]
    ]
    df.to_csv(output_path, sep=";", index=False)

