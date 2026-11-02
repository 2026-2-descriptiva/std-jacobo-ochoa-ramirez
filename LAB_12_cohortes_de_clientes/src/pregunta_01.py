import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_sales_data(activity_dir: Path) -> pd.DataFrame:
    data_path = activity_dir / "data" / "sales.csv.gz"
    sales = pd.read_csv(data_path, compression="gzip")
    sales["OrderDate"] = pd.to_datetime(sales["OrderDate"])
    return sales


def assign_customer_cohorts(sales: pd.DataFrame) -> pd.DataFrame:
    sales = sales.copy()
    first_purchase = sales.groupby("CustomerID")["OrderDate"].transform("min")
    sales["cohort_month"] = first_purchase.dt.to_period("M").astype(str)

    order_month = sales["OrderDate"].dt.to_period("M")
    cohort_period = first_purchase.dt.to_period("M")
    sales["period_index"] = (
        (order_month.dt.year - cohort_period.dt.year) * 12
        + order_month.dt.month
        - cohort_period.dt.month
    )
    return sales


def calculate_cohort_retention(sales: pd.DataFrame) -> pd.DataFrame:
    cohort_sizes = (
        sales.loc[sales["period_index"] == 0]
        .groupby("cohort_month")["CustomerID"]
        .nunique()
    )
    retention = (
        sales.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )
    retention["cohort_size"] = retention["cohort_month"].map(cohort_sizes)
    retention["retention_rate"] = (
        retention["active_customers"] / retention["cohort_size"]
    )
    return retention[
        [
            "cohort_month",
            "period_index",
            "active_customers",
            "cohort_size",
            "retention_rate",
        ]
    ].sort_values(["cohort_month", "period_index"]).reset_index(drop=True)


def save_retention_table(retention: pd.DataFrame, output_dir: Path) -> None:
    retention.to_csv(output_dir / "cohort_retention.csv", index=False)


def save_retention_heatmap(retention: pd.DataFrame, output_dir: Path) -> None:
    heatmap = retention.pivot(
        index="cohort_month",
        columns="period_index",
        values="retention_rate",
    )
    figure, axis = plt.subplots(figsize=(10, 6))
    image = axis.imshow(heatmap, aspect="auto", cmap="YlGnBu", vmin=0, vmax=1)
    axis.set_xlabel("Período desde la primera compra")
    axis.set_ylabel("Cohorte")
    axis.set_xticks(range(len(heatmap.columns)), heatmap.columns)
    axis.set_yticks(range(len(heatmap.index)), heatmap.index)

    for row in range(len(heatmap.index)):
        for column in range(len(heatmap.columns)):
            value = heatmap.iloc[row, column]
            if pd.notna(value):
                axis.text(column, row, f"{value:.0%}", ha="center", va="center")

    figure.colorbar(image, ax=axis, label="Retención")
    figure.tight_layout()
    figure.savefig(output_dir / "cohort_retention_heatmap.png")
    plt.close(figure)


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    activity_dir = Path(__file__).resolve().parents[1]
    output_dir = activity_dir / "submission"
    output_dir.mkdir(parents=True, exist_ok=True)

    sales = load_sales_data(activity_dir)
    sales = assign_customer_cohorts(sales)
    retention = calculate_cohort_retention(sales)
    save_retention_table(retention, output_dir)
    save_retention_heatmap(retention, output_dir)
    return retention
