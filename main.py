from tkinter import Tk
from ui_manager import UIManager
from dark_theme import apply_dark_theme

if __name__ == "__main__":
    root = Tk()
    root.title("Remplacement de Couleurs d'Image")
    root.geometry("1200x800")

    app = UIManager(root)

    # Appliquer le thème sombre
    apply_dark_theme(root)

    root.mainloop()