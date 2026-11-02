import pandas as pd
import os
def leer_archivos(type_folder, feeling):
    phrases = []
    for _, _, files in os.walk(rf"data/{type_folder}/{feeling}"):
        for file in sorted(files):
            with open(
                f"data/{type_folder}/{feeling}/{file}",
                encoding="utf-8",
            ) as reading_file:
                phrases.append(reading_file.readline().strip())
    return phrases


def build_df(group_type):
    feelings = ["negative", "neutral", "positive"]
    sentences = []
    feelings_of_df = []
    for feeling in feelings:
        archivos = leer_archivos(group_type, feeling)
        sentences.extend(archivos)
        feelings_of_df.extend([feeling]*len(archivos))

    return (sentences, feelings_of_df)



def pregunta_01():



    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        # ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...

    """

    sentences_test, feelings_test = build_df("test")

    dict_for_df_test = {
        "phrase": sentences_test,
        "target": feelings_test
    }
    
    test_df = pd.DataFrame(dict_for_df_test)

    sentences_train, feelings_train = build_df("train")

    dict_for_df_train = {
        "phrase": sentences_train,
        "target": feelings_train
    }
    
    train_df = pd.DataFrame(dict_for_df_train)

    test_df.to_csv("submission/test_dataset.csv", index = False)
    train_df.to_csv("submission/train_dataset.csv", index = False)
    


pregunta_01()