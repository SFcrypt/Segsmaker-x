import ipywidgets as widgets
from IPython.display import display, clear_output
from IPython import get_ipython
from pathlib import Path
from box import load_style 
import sys
import os

def launch_lora_downloader():
    ipy = get_ipython()
    load_style()
    
    main_container = widgets.VBox()
    output = widgets.Output()
    
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
        if ipy:
            ipy.run_line_magic("cd", "$LORA")
        main_container.children = [output]
        with output:
            clear_output()
            Link = link_input.value.strip()
            Nombre = nombre_input.value.strip()
            
            if not Link:
                return
            
            try:
                if ipy:
                    if Nombre:
                        nombre_limpio = "-".join(Nombre.split())
                        ipy.run_line_magic(
                            "download",
                            f"{Link} {nombre_limpio}.safetensors")
                    else:
                        ipy.run_line_magic(
                            "download",
                            f"{Link}")
            except:
                pass
    
    download_btn.on_click(descargar_lora)
    
    form_box = widgets.VBox([
        widgets.HTML("<div class='seg-title'>Descargar Lora</div>"),
        link_input,
        nombre_input,
        download_btn])
    form_box.add_class("seg-box")
    
    main_container.children = [form_box]
    display(main_container)

# ejecutar
launch_lora_downloader()
