import json
import os
import sys


def check_notebooks_have_no_cells(root_dir="."):
    cleaned = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.abspath(dirpath) == os.path.abspath(root_dir):
            dirnames[:] = [
                dirname
                for dirname in dirnames
                if dirname.startswith("PRE") or dirname.startswith("LAB")
            ]

        if os.path.basename(dirpath) != "notebooks":
            continue

        for filename in filenames:
            if not filename.endswith(".ipynb"):
                continue

            notebook_path = os.path.join(dirpath, filename)

            with open(notebook_path, "r", encoding="utf-8") as f:
                notebook = json.load(f)

            cells = notebook.get("cells", [])
            if len(cells) > 0:
                notebook["cells"] = []
                with open(notebook_path, "w", encoding="utf-8") as f:
                    json.dump(notebook, f, ensure_ascii=False, indent=1)
                    f.write("\n")
                cleaned.append(notebook_path)

    if cleaned:
        print("Se eliminaron las celdas de los siguientes notebooks:")
        for notebook_path in cleaned:
            print(f"  - {notebook_path}")
    else:
        print("Todos los notebooks en notebooks/ están vacíos correctamente.")
    return True


def clean_folders(root_dir="."):
    removed = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.abspath(dirpath) == os.path.abspath(root_dir):
            dirnames[:] = [
                dirname
                for dirname in dirnames
                if dirname.startswith("PRE") or dirname.startswith("LAB")
            ]

        dirnames[:] = [dirname for dirname in dirnames if dirname != ".venv"]
        if os.path.basename(dirpath) not in ("submission", "temp", "scripts"):
            continue

        for filename in filenames:
            if filename in (".gitkeep", "__init__.py"):
                continue

            file_path = os.path.join(dirpath, filename)
            os.remove(file_path)
            removed.append(file_path)

    if removed:
        print(
            "Se eliminaron los siguientes archivos de las carpetas submission/, temp/ y scripts/:"
        )
        for file_path in removed:
            print(f"  - {file_path}")
    else:
        print(
            "Todas las carpetas submission/, temp/ y scripts/ contienen únicamente .gitkeep."
        )


def main():
    check_notebooks_have_no_cells(".")
    clean_folders(".")


if __name__ == "__main__":
    main()
