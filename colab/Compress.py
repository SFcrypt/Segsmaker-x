import os, shutil, ipywidgets as widgets
from IPython.display import display, clear_output, HTML
from html import escape
from box import load_style

def launch_image_compressor():
    carpeta = "/content/ComfyUI/output"
    destino = "/content/zip"
    os.makedirs(carpeta, exist_ok=True)
    os.makedirs(destino, exist_ok=True)
    load_style()

    nombre_input = widgets.Text(placeholder="Nombre (zip)", layout=widgets.Layout(width="80%", margin="0 0 6px 0"))
    nombre_input.add_class("seg-input-html")
    crear_btn = widgets.Button(description="comprimir", layout=widgets.Layout(height="35px", padding="0 0px"))
    crear_btn.add_class("seg-button")

    def crear_zip(b):
        nombre = nombre_input.value.strip()
        if not nombre:
            return
        nombre = nombre.capitalize().replace(" ", "-")
        if nombre.lower().endswith(".zip"):
            nombre = nombre[:-4]
        if not nombre or nombre in (".", ".."):
            return

        marcador = os.path.join(carpeta, "_output_images_will_be_put_here")
        if os.path.isfile(marcador):
            os.remove(marcador)
        if not os.listdir(carpeta):
            clear_output(wait=True)
            print("Carpeta vacía.")
            return

        base = os.path.join(destino, nombre)
        zip_path, n = base + ".zip", 2
        while os.path.exists(zip_path):
            zip_path, n = f"{base}({n}).zip", n + 1

        clear_output(wait=True)
        try:
            shutil.make_archive(zip_path[:-4], "zip", root_dir=carpeta)
            if os.path.isfile(zip_path) and os.path.getsize(zip_path) > 0:
                for archivo in os.listdir(carpeta):
                    ruta = os.path.join(carpeta, archivo)
                    shutil.rmtree(ruta) if os.path.isdir(ruta) and not os.path.islink(ruta) else os.remove(ruta)

                display(HTML(f"""
                <div style="font-family:monospace;font-size:14px;padding:8px 0;overflow-wrap:anywhere;color:#d1d1d1;">
                <span style="color:#00e6a0;">●</span>
                <span style="color:#ff8733;">/</span><span>content</span><span style="color:#ff8733;">/</span><span>zip</span><span style="color:#ff8733;">/</span><span>{escape(os.path.basename(zip_path))}</span>
                </div>"""))
            else:
                print("Error al crear el ZIP.")
        except Exception as e:
            print(f"Error al comprimir: {e}")

    crear_btn.on_click(crear_zip)
    form_box = widgets.VBox([
        widgets.HTML("<div class='seg-title'>Comprimir Imágenes</div>"),
        nombre_input, crear_btn
    ])
    form_box.add_class("seg-box")
    display(form_box)

# Ejecutar
launch_image_compressor()
