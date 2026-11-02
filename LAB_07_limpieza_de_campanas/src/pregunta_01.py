import pandas as pd
from pathlib import Path

# pylint: disable=import-outside-toplevel
import pandas as pd
import zipfile

# def load_data():
#     data_path = Path(__file__).resolve().parents[1] / "data" / "solicitudes_de_credito.csv.gz"
#     return pd.read_csv(data_path, sep=";", index_col=0, compression="gzip")



def readfiles():
    files_dfs = []

    for i in range(10):
        # zip_path = f"files/input/bank-marketing-campaing-{i}.csv.zip"
        zip_path = Path(__file__).resolve().parents[1] / "data" / f"bank-marketing-campaing-{i}.csv.gz"      
        file_df = pd.read_csv(zip_path, index_col=0, compression="gzip")
        files_dfs.append(file_df)
    return pd.concat(files_dfs)


def define_client_df(df):
    client_df = df[[
        "client_id",
        "age",
        "job",
        "marital",
        "education",
        "credit_default",
        "mortgage"
        ]].copy()

    client_df["job"] = client_df["job"].str.replace(".", "").str.replace("-", "_")
    client_df["education"] = client_df["education"].str.replace(".", "_").replace({"unknown": pd.NA})
    
    client_df["credit_default"] = client_df["credit_default"].map(lambda x: 1 if x == "yes" else 0)
    client_df["mortgage"] = client_df["mortgage"].map(lambda x: 1 if x == "yes" else 0)

    return client_df

def define_campaign_df(df):
    campaign_df = df[[
        "client_id",        
        "number_contacts",        
        "contact_duration",        
        "previous_campaign_contacts",        
        "previous_outcome",
        "campaign_outcome"
    ]].copy()

    campaign_df["previous_outcome"] = campaign_df["previous_outcome"].map(lambda x: 1 if x == "success" else 0)    
    campaign_df["campaign_outcome"] = campaign_df["campaign_outcome"].map(lambda x: 1 if x == "yes" else 0)    

    month_mapping = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
    "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }

    df["month"] = df["month"].map(month_mapping)

    campaign_df["last_contact_date"] = "2022-" + df["month"] + "-" + df["day"].astype(str).str.zfill(2)

    return campaign_df

def define_economics_df(df):
    economics_df = df[[
    "client_id",
    "cons_price_idx",
    "euribor_three_months"
    ]].copy()

    return economics_df


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    df = readfiles()
    client_df = define_client_df(df)
    campaign_df = define_campaign_df(df)
    economics_df = define_economics_df(df)

    client_df.to_csv("submission/client.csv", index = False)
    campaign_df.to_csv("submission/campaign.csv", index = False)
    economics_df.to_csv("submission/economics.csv", index = False)
