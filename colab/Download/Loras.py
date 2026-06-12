import ipywidgets as widgets
from IPython.display import display, clear_output
from IPython import get_ipython
from pathlib import Path
import sys
import os

def launch_lora_downloader():
    ipy = get_ipython()

    # Ir al HOME
    os.chdir(os.path.expanduser("~"))

    # Agregar ruta de utilidades
    download_dir = Path.home() / ".swar" / "Download"
    if str(download_dir) not in sys.path:
        sys.path.insert(0, str(download_dir))

    # Cargar estilos
    from box import load_style
    load_style()

    link_input = widgets.Text(
        placeholder="Link de descarga",
        layout=widgets.Layout(width="80%", margin="0 0 6px 0")
    )
    link_input.add_class("seg-input-html")

    nombre_input = widgets.Text(
        placeholder="Nombre del archivo",
        layout=widgets.Layout(width="80%", margin="0 0 6px 0")
    )
    nombre_input.add_class("seg-input-html")

    download_btn = widgets.Button(
        description="Download",
        layout=widgets.Layout(height="35px", padding="0 0px")
    )
    download_btn.add_class("seg-button")

    def descargar_lora(b):

        link = link_input.value.strip()
        nombre = "-".join(nombre_input.value.strip().split())

        if not link or not nombre:
            return

        # Cambiar al directorio LoRA
        if ipy:
            ipy.run_line_magic("cd", "$LORA")

        # quitar la UI para que %download escriba
        clear_output()

        try:
            if ipy:
                ipy.run_line_magic(
                    "download",
                    f"{link} {nombre}.safetensors"
                )
        except Exception as e:
            print(f"Error durante la descarga: {e}")

    download_btn.on_click(descargar_lora)

    form_box = widgets.VBox([
        widgets.HTML("<div class='seg-title'>Descargar LoRA</div>"),
        link_input,
        nombre_input,
        download_btn
    ])

    form_box.add_class("seg-box")

    display(form_box)

# Ejecutar
launch_lora_downloader()
