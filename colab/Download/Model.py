import ipywidgets as widgets
from IPython.display import display, clear_output
from IPython import get_ipython
from pathlib import Path
from box import load_style
import sys
import os

def launch_lora_downloader():
    ipy = get_ipython()

    os.chdir(os.path.expanduser("~"))

    # Cargar estilos
    load_style()

    link_input = widgets.Text(
        placeholder="Link de descarga",
        layout=widgets.Layout(width="80%", margin="0 0 6px 0"))
    link_input.add_class("seg-input-html")

    nombre_input = widgets.Text(
        placeholder="Nombre (opcional)",
        layout=widgets.Layout(width="80%", margin="0 0 6px 0"))
    nombre_input.add_class("seg-input-html")

    download_btn = widgets.Button(
        description="Download",
        layout=widgets.Layout(height="35px", padding="0 0px"))
    download_btn.add_class("seg-button")

    def descargar_lora(b):
        link = link_input.value.strip()
        nombre = nombre_input.value.strip() 
        if not link:
            return    
        if ipy:
            ipy.run_line_magic("cd", "$CKPT")
        
        clear_output()
        try:
            if ipy:
                if nombre:
                    nombre_limpio = "-".join(nombre.split())
                    ipy.run_line_magic(
                        "download",
                        f"{link} {nombre_limpio}.safetensors"
                    )
                else:
                    ipy.run_line_magic(
                        "download",
                        f"{link}")
        except:
            pass

    download_btn.on_click(descargar_lora)

    form_box = widgets.VBox([
        widgets.HTML("<div class='seg-title'>Descargar Modelo</div>"),
        link_input,
        nombre_input,
        download_btn])

    form_box.add_class("seg-box")
    display(form_box)

# Ejecutar
launch_lora_downloader()
