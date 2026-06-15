R = '\033[31m'
P = '\033[38;5;135m'
RST = '\033[0m'
ERR = f'{P}[{RST}{R}ERROR{RST}{P}]{RST}'

import sys, subprocess
python_version = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.split()[1]
if tuple(map(int, python_version.split('.'))) < (3, 10, 6):
    print(f'{ERR}: Python version 3.10.6 or higher required, and you are using Python {python_version}')
    sys.exit()

from pathlib import Path
import shutil
import shlex
import json
import os

from nenen88 import pull, say, download, clone, tempe

REPO = {
    'ComfyUI': 'https://github.com/comfyanonymous/ComfyUI'
}

SyS = get_ipython().system
CD = os.chdir

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MRK = SRC / 'marking.py'
MARKED = SRC / 'marking.json'
TMP = Path('/tmp')

SRC.mkdir(parents=True, exist_ok=True)
iRON = os.environ

def SM_Script(WEBUI):
    return [
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}',
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}',
        f'https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}'
    ]

def CN_Script(WEBUI):
    return [
        f'https://github.com/gutris1/segsmaker/raw/main/script/controlnet.py {WEBUI}/asd',
        f'https://github.com/gutris1/segsmaker/raw/main/script/cn15.py {WEBUI}/asd',
        f'https://github.com/gutris1/segsmaker/raw/main/script/cnxl.py {WEBUI}/asd',
    ]

def tmp_cleaning(v):
    for i in TMP.iterdir():
        if i.is_dir() and i != v:
            shutil.rmtree(i)
        elif i.is_file() and i != v:
            i.unlink()

def marking(p, n, i):
    t = p / n
    if not t.exists():
        t.write_text(json.dumps({
            'ui': i,
            'launch_args': '',
            'zrok_token': '',
            'ngrok_token': '',
            'tunnel': ''
        }, indent=4))
    d = json.loads(t.read_text())
    d.update({'ui': i, 'launch_args': ''})
    t.write_text(json.dumps(d, indent=4))

def install_tunnel():
    bins = {
        'zrok': {
            'bin': HOME / '.zrok/bin/zrok',
            'url': 'https://github.com/openziti/zrok/releases/download/v1.0.6/zrok_1.0.6_linux_amd64.tar.gz'
        },
        'ngrok': {
            'bin': HOME / '.ngrok/bin/ngrok',
            'url': 'https://bin.ngrok.com/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz'
        }
    }

    for n, b in bins.items():
        binPath = b['bin']
        if binPath.exists(): binPath.unlink()

        url = b['url']
        name = Path(url).name
        binDir = binPath.parent

        binDir.mkdir(parents=True, exist_ok=True)

        SyS(f'curl -sLo {binDir}/{name} {url}')
        SyS(f'tar -xzf {binDir}/{name} -C {binDir} --wildcards *{n}')
        SyS(f'rm -f {binDir}/{name}')

        if str(binDir) not in iRON.get('PATH', ''): iRON['PATH'] += ':' + str(binDir)
        binPath.chmod(0o755)

def sym_link(U, M):
    configs = {
        'ComfyUI': {
            'sym': [
                f"rm -rf {M / 'checkpoints/tmp_ckpt'} {M / 'loras/tmp_lora'} {M / 'controlnet'}",
                f"rm -rf {M / 'clip'} {M / 'clip_vision'} {M / 'diffusers'} {M / 'diffusion_models'}",
                f"rm -rf {M / 'text_encoders'} {M / 'unet'}"
            ],
            'links': [
                (M / 'checkpoints', M / 'checkpoints_symlink'),
                (TMP, HOME / 'tmp'),
                (TMP / 'ckpt', M / 'checkpoints/tmp_ckpt'),
                (TMP / 'lora', M / 'loras/tmp_lora'),
                (TMP / 'controlnet', M / 'controlnet'),
                (TMP / 'clip', M / 'clip'),
                (TMP / 'clip_vision', M / 'clip_vision'),
                (TMP / 'diffusers', M / 'diffusers'),
                (TMP / 'diffusion_models', M / 'diffusion_models'),
                (TMP / 'text_encoders', M / 'text_encoders'),
                (TMP / 'unet', M / 'unet')
            ]
        }
    }

    cfg = configs.get(U)
    SyS(f"rm -rf {HOME / 'tmp'} {HOME / '.cache'}/*")
    [SyS(f'{cmd}') for cmd in cfg['sym']]
    [SyS(f'ln -s {src} {tg}') for src, tg in cfg['links']]

def webui_req(U, W, M):
    vnv = TMP / 'venv'
    tmp_cleaning(vnv)
    CD(W)

    pull(f'https://github.com/gutris1/segsmaker {U.lower()} {W}')
    sym_link(U, M)

    scripts = SM_Script(W)
    scripts.extend(CN_Script(W))

    u = M / 'upscale_models'
    upscalers = [
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x-UltraSharp.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x-AnimeSharp.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x_NMKD-Superscale-SP_178000_G.pth {u}',
        f'https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/8x_NMKD-Superscale_150000_G.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x_RealisticRescaler_100000_G.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/8x_RealESRGAN.pth {u}',
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/4x_foolhardy_Remacri.pth {u}',
        f'https://huggingface.co/subby2006/NMKD-YandereNeoXL/resolve/main/4x_NMKD-YandereNeoXL_200k.pth {u}',
        f'https://huggingface.co/subby2006/NMKD-UltraYandere/resolve/main/4x_NMKD-UltraYandere_300k.pth {u}'
    ]

    line = scripts + upscalers
    for item in line: download(item)

def WebUIExtensions(U, W, M):
    EXT = W / 'custom_nodes'
    CD(EXT)

    say('<br><b>【{red} Installing Custom Nodes{d} 】{red}</b>')
    clone(str(W / 'asd/custom_nodes.txt'))
    print()

    for faces in [
        f'https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth {M}/facerestore_models',
        f'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth {M}/facerestore_models'
    ]: download(faces)

def installing_webui(U, W):
    M = W / 'models'
    E = M / 'embeddings'
    V = M / 'vae'

    webui_req(U, W, M)
    install_tunnel()

    extras = [
        f'https://huggingface.co/gutris1/webui/resolve/main/misc/embeddingsXL.zip {W}',
        f'https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl.vae.safetensors {V} sdxl_vae.safetensors'
    ]

    for i in extras: download(i)
    SyS(f"unzip -qo {W / 'embeddingsXL.zip'} -d {E} && rm {W / 'embeddingsXL.zip'}")
    WebUIExtensions(U, W, M)

def webui_install(ui):
    WEBUI = HOME / ui
    repo = REPO[ui]

    say(f"<b>【{{red}} Installing {ui.replace('-', '')}{{d}} 】{{red}}</b>")
    clone(repo)

    marking(SRC, MARKED, ui)
    installing_webui(ui, WEBUI)
    tempe()

    get_ipython().run_line_magic('run', str(MRK))
    get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

    say('<b>【{red} Done{d} 】{red}</b>')
    CD(HOME)

# Instalación automática de ComfyUI
CD(HOME)
webui_install('ComfyUI')
