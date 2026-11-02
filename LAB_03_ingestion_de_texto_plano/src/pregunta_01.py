# def pregunta_01():
#     """
#     El archivo `data/clusters_report.txt` es un reporte de clústeres de
#     palabras clave pensado para ser leído por una persona, no por un programa:
#     los encabezados ocupan varias líneas, las columnas están alineadas con
#     espacios y la lista de palabras clave de un clúster continúa en las líneas
#     siguientes.

#     Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
#     por clúster y las columnas:

#     - `cluster`: número del clúster, como entero.
#     - `cantidad_de_palabras_clave`: como entero.
#     - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
#       texto `15,9 %` debe quedar como `15.9`.
#     - `principales_palabras_clave`: todas las palabras clave del clúster en un
#       solo texto, separadas por una coma y un único espacio.

#     Retorne el DataFrame.

#     Ejemplo del formato de la respuesta (se omite la última columna):

#            cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
#         0        1                         105                          15.9
#         1        2                         102                          15.4
#         ...
#     """

#     raise NotImplementedError


import re
import pandas as pd
# pylint: disable=import-outside-toplevel

def clean_headers(header_lines):
	
	almost_headers = [title.strip().lower() for title in re.split(r'\s{2,}', header_lines[0])]
	add_to_header = "palabras clave"
	almost_headers[1] += " " + add_to_header
	almost_headers[2] += " " + add_to_header

	return [header.replace(" ", "_") for header in almost_headers]

def extract_columns_info(lines):
	cluster_count = 0
	columns = [[], [], [], []]
	for line in lines:
		line_info = re.sub(r'\s{6,}', ':', line.strip()).split(':')
		
		if len(line_info) == 3:
			cluster_num, word_qnt = re.split(r'\s{3,}', line_info[0])
			columns[0].append(int(cluster_num))
			columns[1].append(int(word_qnt))
			columns[2].append(float(line_info[1][:-2].replace(",", ".")))
			columns[3].append(line_info[2])
			cluster_count += 1


		if len(line_info) == 1:
			
			columns[3][cluster_count-1]+= " " + line_info[0]
			
	return columns
		
def clean_key_words(key_words_list):
	cleaned_key_words_list = []
	for line in key_words_list:
		line = line.replace(".", "").strip()
		cleaned_line = re.sub(r'\s*,\s*', ', ', line)  # Fix spaces around commas
		cleaned_line = re.sub(r'\s{2,}', ' ', cleaned_line)  # Remove extra spaces
		cleaned_line = re.sub(r',+', ',', cleaned_line)  # Remove extra commas
		cleaned_key_words_list.append(cleaned_line)

	return cleaned_key_words_list

def pregunta_01():
	"""
	Construya y retorne un dataframe de Pandas a partir del archivo
	'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

	- El dataframe tiene la misma estructura que el archivo original.
	- Los nombres de las columnas deben ser en minusculas, reemplazando los
	espacios por guiones bajos.
	- Las palabras clave deben estar separadas por coma y con un solo
	espacio entre palabra y palabra.


	"""

	with open("data/clusters_report.txt") as file:
		lines = file.readlines()

	filtered_lines = [line.strip() for line in lines if "---" not in line]

	headers = clean_headers(filtered_lines[:2])
	info = extract_columns_info(lines[4:])
	info[3] = clean_key_words(info[3])
	
	reports_dict = {headers[column_num]:info[column_num] for column_num in range(4)}
	return pd.DataFrame.from_dict(reports_dict)


print(pregunta_01())