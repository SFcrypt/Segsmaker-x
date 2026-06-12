from IPython.display import display, HTML, clear_output
from multiprocessing import Process, Condition, Value
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import argparse
import logging
import json
import yaml
import sys
import os

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
MARK = SRC / 'marking.json'
IMG = SRC / 'loading.png'

SyS = get_ipython().system

R = '\033[31m'
P = '\033[38;5;135m'
RST = '\033[0m'
ERR = f'{P}[{RST}{R}ERROR{RST}{P}]{RST}'

def get_args(ui):
    args_line = {
        'A1111': ('--xformers'),
        'Forge': ('--disable-xformers --opt-sdp-attention --cuda-stream'),
        'ReForge': ('--xformers --cuda-stream'),
        'Forge-Classic': ('--xformers --cuda-stream --persistent-patches'),
        'ComfyUI': ('--dont-print-server --use-pytorch-cross-attention'),
        'SwarmUI': ('--launch_mode none'),
        'FaceFusion': '',
        'SDTrainer': ''
    }

    return args_line.get(ui, '')

def GPU_check():
    return Path('/proc/driver/nvidia').exists()

def load_config():
    global ui
    config = json.loads(MARK.read_text()) if MARK.exists() else {}

    ui = config.get('ui', None)
    arg = config.get('launch_args')
    tunnell = config.get('tunnel')
    zrok_token.value = config.get('zrok_token', '')
    ngrok_token.value = config.get('ngrok_token', '')

    if arg:
        launch_args.value = arg
    else:
        launch_args.value = get_args(ui)

    if tunnell in ['Pinggy', 'ZROK', 'NGROK']:
        tunnel.value = tunnell
    else:
        tunnel.value = 'Pinggy'
        config.update({'tunnel': tunnel.value})
        MARK.write_text(json.dumps(config, indent=4))

    cpu_cb.value = False if GPU_check() else config.get('cpu_usage', False)
    cpu_cb.layout.display = 'none' if ui in ['SDTrainer', 'FaceFusion', 'SwarmUI'] or GPU_check() else 'block'

    ui_titles = {
        'A1111': 'A1111',
        'Forge': 'Forge',
        'ReForge': 'ReForge',
        'Forge-Classic': 'Forge Classic',
        'ComfyUI': 'ComfyUI',
        'SwarmUI': 'SwarmUI',
        'FaceFusion': 'Face Fusion',
        'SDTrainer': 'SD Trainer'
    }

    title.value = f"<div class='seg-title'>{ui_titles.get(ui, 'Unknown UI')}</div>"

def save_config(zrok_token, ngrok_token, launch_args, tunnel):
    config = json.loads(MARK.read_text()) if MARK.exists() else {}

    config.update({
        'zrok_token': zrok_token,
        'ngrok_token': ngrok_token,
        'launch_args': launch_args,
        'tunnel': tunnel,
        'cpu_usage': cpu_cb.value
    })

    MARK.write_text(json.dumps(config, indent=4))

def load_css():
    # Cambiar al directorio home sin mostrar salida
    os.chdir(os.path.expanduser("~"))
    
    # Agregar la ruta donde está box.py
    download_dir = Path.home() / ".swar" / "Download"
    if str(download_dir) not in sys.path:
        sys.path.insert(0, str(download_dir))
    
    # Importar box.py desde la ubicación actualizada
    from box import load_style
    load_style()

# ============ NUEVA INTERFAZ (como launch_lora_downloader) ============
title = widgets.HTML()
zrok_token = widgets.Text(
    placeholder="Your ZROK Token",
    layout=widgets.Layout(width="80%", margin="0 0 6px 0"))
zrok_token.add_class("seg-input-html")

ngrok_token = widgets.Text(
    placeholder="Your NGROK Token",
    layout=widgets.Layout(width="80%", margin="0 0 6px 0"))
ngrok_token.add_class("seg-input-html")

launch_args = widgets.Text(
    placeholder="Launch Arguments List",
    layout=widgets.Layout(width="80%", margin="0 0 6px 0"))
launch_args.add_class("seg-input-html")

# Selector de tunel
tunnel = widgets.ToggleButtons(
    options=['Pinggy', 'ZROK', 'NGROK'],
    button_style='',
    layout=widgets.Layout(
        display='flex',
        justify_content='center',
        margin='0 0 6px 0',
        width='80%'
    )
)
tunnel.style = {'button_width': '80px', 'colors': {'selected': '#C41564'}}

# Checkbox CPU
cpu_cb = widgets.Checkbox(
    value=False,
    description='CPU',
    layout=widgets.Layout(margin='6px 0'))

# Botones
launch_button = widgets.Button(
    description='Iniciar',
    layout=widgets.Layout(height="35px", padding="0 50px"))
launch_button.add_class("seg-button")

exit_button = widgets.Button(
    description='Exit',
    layout=widgets.Layout(height="35px", padding="0 50px"))
exit_button.add_class("seg-button")

button_box = widgets.HBox(
    [launch_button, exit_button],
    layout=widgets.Layout(
        display='flex',
        gap='20px',
        justify_content='center',
        margin='6px 0 0 0'
    )
)

# Formulario igual que el diseño original
form_box = widgets.VBox([
    title,
    tunnel,
    zrok_token,
    ngrok_token,
    launch_args,
    cpu_cb,
    button_box
])
form_box.add_class("seg-box")

launch_panel = form_box
# ============ FIN NUEVA INTERFAZ ============

parser = argparse.ArgumentParser()
parser.add_argument('--skip-comfyui-check', action='store_true', help='Skip checking custom node dependencies for ComfyUI')
parser.add_argument('--skip-widget', action='store_true', help='Skip displaying the widget')
args, unknown = parser.parse_known_args()

condition = Condition()
is_ready = Value('b', False)

def NGROK_ZROK(T):
    P = {
        'zrok': {
            'B': HOME / '.zrok/bin/zrok',
            'C': HOME / '.zrok/environment.json',
            't': zrok_token.value
        },
        'ngrok': {
            'B': HOME / '.ngrok/bin/ngrok',
            'C': HOME / '.config/ngrok/ngrok.yml',
            't': ngrok_token.value
        }
    }

    B, C, t = P[T]['B'], P[T]['C'], P[T]['t']

    if not t:
        print(f'{ERR}: {T.upper()} Token is empty'); sys.exit()
    if not B.exists():
        print(f'{ERR}: {T.upper()} is not installed'); sys.exit()

    E = f'{T} enable {t}' if T == 'zrok' else f'{T} config add-authtoken {t}'

    if C.exists():
        ct = None
        if T == 'zrok':
            ct = json.loads(C.read_text()).get('zrok_token')
        elif T == 'ngrok':
            ct = yaml.safe_load(C.read_text()).get('agent', {}).get('authtoken')

        if ct != t:
            if T == 'zrok':
                SyS(f'{T} disable')
            SyS(E); print()
    else:
        SyS(E); print()

def launching(ui, skip_comfyui_check=False):
    args = f'{launch_args.value}'
    tunnel_name = tunnel.value

    get_ipython().run_line_magic('run', 'venv.py')

    if ui in ['A1111', 'Forge', 'ReForge', 'Forge-Classic']:
        port = 7860
        PY = '/tmp/python311/bin/python3' if ui == 'Forge-Classic' else '/tmp/venv/bin/python3'
        args += ' --enable-insecure-extension-access --disable-console-progressbars --theme dark'

    elif ui in ['ComfyUI', 'SwarmUI']:
        PY = '/tmp/venv-comfy-swarm/bin/python3'

        if ui == 'ComfyUI':
            port = 8188
            skip_comfyui_check or (SyS(f'{PY} apotek.py'), clear_output(wait=True))
        else:
            port = 7801

    elif ui == 'SDTrainer':
        port = 28000
        PY = 'HF_HOME=huggingface /tmp/venv-sd-trainer/bin/python3'

    elif ui == 'FaceFusion':
        port = 7860
        PY = '/tmp/venv-fusion/bin/python3'

    if cpu_cb.value:
        if ui == 'A1111':
            args += ' --use-cpu all --precision full --no-half --skip-torch-cuda-test'
        elif ui in ['Forge', 'ReForge', 'Forge-Classic']:
            args += ' --always-cpu --skip-torch-cuda-test'
        elif ui == 'ComfyUI':
            args += ' --cpu'

    tunnel_config = {
        'Pinggy': {
            'command': f'ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io',
            'name': 'PINGGY',
            'pattern': r'https://[\w-]+\.run\.pinggy-free\.link'
        },
        'NGROK': {
            'command': f'ngrok http http://localhost:{port} --log stdout',
            'name': 'NGROK',
            'pattern': r'https://[\w-]+\.ngrok-free\.[\w.-]+'
        },
        'ZROK': {
            'command': f'zrok share public localhost:{port} --headless',
            'name': 'ZROK',
            'pattern': r'https://[\w-]+\.share\.zrok\.[\w.-]+'
        }
    }

    c = f'{PY} Launcher.py {args}'
    cmd = {key: c for key in ['Pinggy', 'ZROK', 'NGROK']}.get(tunnel_name)
    configs = tunnel_config.get(tunnel_name)

    if cmd and configs:
        try:
            from cupang import Tunnel as Alice_Zuberg

            if tunnel_name == 'ZROK': NGROK_ZROK('zrok')
            if tunnel_name == 'NGROK': NGROK_ZROK('ngrok')

            Alice_Synthesis_Thirty = Alice_Zuberg(port)
            Alice_Synthesis_Thirty.logger.setLevel(logging.DEBUG)
            Alice_Synthesis_Thirty.add_tunnel(command=configs['command'], name=configs['name'], pattern=configs['pattern'])

            with Alice_Synthesis_Thirty: SyS(cmd)
        except KeyboardInterrupt:
            pass

def waiting(condition, is_ready):
    with condition:
        while not is_ready.value:
            try:
                condition.wait()
            except KeyboardInterrupt:
                print('')
                clear_output()
                sys.exit()

    load_config()
    launching(ui, skip_comfyui_check=args.skip_comfyui_check)

def launch(b):
    global ui, zrok_token, ngrok_token, launch_args, tunnel
    launch_panel.close()
    save_config(zrok_token.value, ngrok_token.value, launch_args.value, tunnel.value)
    with condition:
        is_ready.value = True
        condition.notify()

def exit(b):
    launch_panel.close()

def display_widgets():
    load_config()
    load_css()
    display(launch_panel)
    launch_button.on_click(launch)
    exit_button.on_click(exit)

if __name__ == '__main__':
    try:
        if args.skip_widget:
            load_config()
            launching(ui, skip_comfyui_check=args.skip_comfyui_check)

        else:
            display_widgets()
            p = Process(target=waiting, args=(condition, is_ready))
            p.start()

    except KeyboardInterrupt:
        pass
