import ipywidgets as widgets
from IPython.display import display, HTML

def load_style():
    css = """
    .seg-box {
        background: #1E1F21;
        border-radius: 12px;
        padding: 25px;
        width: 100%;           
        max-width: 100%;
        font-family: 'Source Sans Pro', sans-serif;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;    
        justify-content: center;}

    .seg-title {
        color: rgba(255,255,255,0.9);
        font-size: 27px;        
        font-weight: 400;       
        margin-bottom: 12px;}

    .seg-input-html input {
        background: #333333;  
        border: none;
        border-radius: 12px;
        padding: 12px 0;
        width: 80%;            /* Largo */ 
        margin-bottom: 6px;    /* subir botón */
        color: rgba(255,255,255,0.85);
        font-size: 18px;       
        text-align: center;
        transition: none;      /* no cambia al escribir */
    }

    .seg-input-html input::placeholder {
        color: rgba(255,255,255,0.7);
        text-align: center;
    }

    .seg-button {
        border: 2px solid #C41564; /* borde rosa */
        border-radius: 12px;
        background: #C41564;
        color: #fff;
        font-size: 15px;
        padding: 8px 50px;
        margin-top: 4px;           /* sube un poco el botón */
        transition: background 0.3s ease, transform 0.2s ease;
    }

    .seg-button:hover {
        background: #db5a94;
        transform: translateY(-1px);
    }
    """
    display(HTML(f"<style>{css}</style>"))

def pink_button_download(
    title="Crea tu proyecto",     # Título del widget
    btn_text="Crear",             # Texto del botón
    btn_height=35,                # Alto del botón
    btn_padding=50,               # Padding horizontal del botón
    btn_font_size=15,             # Tamaño de fuente del botón
    btn_border_radius=12,         # Bordes redondeados del botón
    btn_color="#C41564",          # Color de fondo del botón
    btn_hover_color="#db5a94",    # Color al pasar el mouse
    input_placeholder="Proyecto", # Placeholder del input
    input_width="80%",            # Ancho del input # Largo
    input_font_size=18,           # Tamaño de fuente del input
    input_border_radius=12,       # Bordes redondeados del input
    input_margin_bottom=6         # Margen inferior del input
):
    load_style()

    # Crear input tipo Text
    input_text = widgets.Text(
        placeholder=input_placeholder,
        layout=widgets.Layout(width=input_width, margin=f"0 0 {input_margin_bottom}px 0"),
        style={"description_width": "initial"})

    input_text.add_class("seg-input-html")
    input_text.style.placeholder_color = '#d0d0d099'

    # Crear botón con borde rosa
    button = widgets.Button(
    description=btn_text,
    layout=widgets.Layout(height=f"{btn_height}px", width="auto", padding=f"0 {btn_padding}px"),)
    button.add_class("seg-button")

    # Caja principal
    box = widgets.VBox([
    widgets.HTML(f"<div class='seg-title'>{title}</div>"),
    input_text, button])

    box.add_class("seg-box")
    display(box)

    # Devuelve botón y el input para enlazar eventos
    return button, input_text
