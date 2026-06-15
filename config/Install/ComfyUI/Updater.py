from IPython.display import clear_output, Image, display
from nenen88 import say

clear_output()

def run_update():
    img = os.path.expanduser("~/.gutris1/loading.png")
    display(Image(filename=img))
    say("<b>【{red} Updating SwarmUI{d} 】{red}</b>")
    
    clear_output()
    say("<b>【{red} ComfyUI Instalado{d} 】{red}</b>")

if __name__ == "__main__":
    run_update()
