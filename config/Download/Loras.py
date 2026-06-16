import ipywidgets as widgets
from IPython.display import display, clear_output
from IPython import get_ipython
from pathlib import Path
import sys, os

def launch_lora_downloader():
    ipy = get_ipython()
    os.chdir(os.path.expanduser("~"))
    
    download_dir = Path.home() / ".swar" / "Download"
    if str(download_dir) not in sys.path:
        sys.path.insert(0, str(download_dir))
    
    from box import load_style
    load_style()
    
    link = widgets.Text(placeholder="Link de descarga", layout=widgets.Layout(width="80%", margin="0 0 6px 0"))
    link.add_class("seg-input-html")
    
    nombre = widgets.Text(placeholder="Nombre (opcional)", layout=widgets.Layout(width="80%", margin="0 0 6px 0"))
    nombre.add_class("seg-input-html")
    
    btn = widgets.Button(description="Download", layout=widgets.Layout(height="35px", padding="0 0px"))
    btn.add_class("seg-button")
    
    output = widgets.Output()
    
    def descargar(b):
        if ipy:
            ipy.run_line_magic("cd", "$LORA")
        
        with output:
            clear_output()
            url = link.value.strip()
            name = nombre.value.strip()
            
            if not url:
                return
            
            try:
                if ipy:
                    if name:
                        clean_name = "-".join(name.split())
                        ipy.run_line_magic("download", f"{url} {clean_name}.safetensors")
                    else:
                        ipy.run_line_magic("download", url)
            except:
                pass
    
    btn.on_click(descargar)  
    
    box = widgets.VBox([
        widgets.HTML("<div class='seg-title'>Descargar Lora</div>"),
        link, nombre, btn])
    box.add_class("seg-box")
    
    container = widgets.VBox([box])
    display(container)
launch_lora_downloader()
