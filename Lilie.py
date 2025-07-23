# main.py
from modules.main_window import AIChatApp
import os
import sys

def resource_path(relative_path):
    """Retorna o caminho absoluto para recursos, compatível com PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

if __name__ == "__main__":
    app = AIChatApp()
    # Define o ícone da janela (barra de tarefas)
    icon_path = resource_path("lilie.ico")
    app.iconbitmap(icon_path)
    app.mainloop()