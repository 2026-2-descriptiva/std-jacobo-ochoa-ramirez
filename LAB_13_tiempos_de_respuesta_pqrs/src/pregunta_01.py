import pandas as pd
import numpy as np
from pathlib import Path


def load_channel_data(activity_dir: Path, channel: str) -> pd.DataFrame:
    data_path = activity_dir / "data" / f"historical_requests_{channel}.csv.gz"
    requests = pd.read_csv(data_path, compression="gzip").drop_duplicates()
    requests["channel"] = channel
    requests["in_date"] = pd.to_datetime(requests["in_date"])
    requests["out_date"] = pd.to_datetime(requests["out_date"])
    return requests


def combine_channel_data(activity_dir: Path) -> pd.DataFrame:
    return pd.concat(
        [
            load_channel_data(activity_dir, "letter"),
            load_channel_data(activity_dir, "web"),
        ],
        ignore_index=True,
    )


def calculate_response_times(requests: pd.DataFrame) -> pd.DataFrame:
    requests = requests.copy()
    answered = requests["out_date"].notna()
    requests["calendar_days"] = (
        requests["out_date"] - requests["in_date"]
    ).dt.days
    requests["business_days"] = pd.NA
    requests.loc[answered, "business_days"] = np.busday_count(
        (requests.loc[answered, "in_date"] + pd.Timedelta(days=1))
        .values.astype("datetime64[D]"),
        (requests.loc[answered, "out_date"] + pd.Timedelta(days=1))
        .values.astype("datetime64[D]"),
    )
    requests["business_days"] = pd.to_numeric(
        requests["business_days"], errors="coerce"
    )
    requests["answered"] = answered
    requests["on_time"] = answered & (requests["business_days"] <= 15)
    return requests


def build_channel_summary(requests: pd.DataFrame) -> pd.DataFrame:
    summary = (
        requests.groupby("channel")
        .agg(
            requests=("channel", "size"),
            answered=("answered", "sum"),
            pending=("answered", lambda values: (~values).sum()),
            median_business_days=("business_days", "median"),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
        .sort_values("channel")
    )
    return summary[
        [
            "channel",
            "requests",
            "answered",
            "pending",
            "median_business_days",
            "on_time_rate",
        ]
    ]


def build_yearly_summary(requests: pd.DataFrame) -> pd.DataFrame:
    requests["year"] = requests["in_date"].dt.year
    summary = (
        requests.groupby(["year", "channel"])
        .agg(
            requests=("channel", "size"),
            pending=("answered", lambda values: (~values).sum()),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
        .sort_values(["year", "channel"])
    )
    return summary[["year", "channel", "requests", "pending", "on_time_rate"]]


def build_entry_day_summary(requests: pd.DataFrame) -> pd.DataFrame:
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    requests = requests.copy()
    requests["day_name"] = pd.Categorical(
        requests["day_name"], categories=day_order, ordered=True
    )
    summary = (
        requests.groupby("day_name", observed=False)
        .agg(
            requests=("day_name", "size"),
            median_calendar_days=("calendar_days", "median"),
            median_business_days=("business_days", "median"),
        )
        .reset_index()
    )
    summary["day_name"] = summary["day_name"].astype(str)
    return summary[
        ["day_name", "requests", "median_calendar_days", "median_business_days"]
    ]


def save_summaries(
    channel_summary: pd.DataFrame,
    yearly_summary: pd.DataFrame,
    entry_day_summary: pd.DataFrame,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    channel_summary.to_csv(output_dir / "channel_summary.csv", index=False)
    yearly_summary.to_csv(output_dir / "yearly_summary.csv", index=False)
    entry_day_summary.to_csv(output_dir / "entry_day_summary.csv", index=False)


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """

    activity_dir = Path(__file__).resolve().parents[1]
    requests = calculate_response_times(combine_channel_data(activity_dir))
    channel_summary = build_channel_summary(requests)
    yearly_summary = build_yearly_summary(requests)
    entry_day_summary = build_entry_day_summary(requests)
    save_summaries(
        channel_summary,
        yearly_summary,
        entry_day_summary,
        activity_dir / "submission",
    )
    return channel_summary, yearly_summary, entry_day_summary
