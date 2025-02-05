from tkinter import Tk
from ui_manager import UIManager

if __name__ == "__main__":
    root = Tk()
    root.title("Remplacement de Couleurs d'Image")  # Définir un titre pour la fenêtre
    root.geometry("1200x800")  # Taille initiale de la fenêtre
    app = UIManager(root)
    root.mainloop()