import os
import sys

# Auto-restart in virtual environment if needed
def _ensure_venv():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv_python = os.path.join(root_dir, 'venv', 'bin', 'python')
    if os.name == 'nt':
        venv_python = os.path.join(root_dir, 'venv', 'Scripts', 'python.exe')
        
    if os.path.exists(venv_python) and os.path.abspath(sys.executable) != os.path.abspath(venv_python):
        os.execv(venv_python, [venv_python] + sys.argv)

_ensure_venv()
