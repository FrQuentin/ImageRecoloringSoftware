import os
from tkinter import filedialog
from PIL import Image

def load_image():
    """
    Ouvre une boîte de dialogue pour sélectionner une image et retourne son chemin.
    Démarre dans le dossier Documents par défaut.
    """
    initial_dir = os.path.expanduser("~/Documents")  # Dossier Documents par défaut
    file_path = filedialog.askopenfilename(
        title="Sélectionnez une image PNG",
        initialdir=initial_dir,
        filetypes=[("Fichiers PNG", "*.png"), ("Tous les fichiers", "*.*")]
    )
    if file_path:
        try:
            Image.open(file_path)  # Vérifier que le fichier est une image valide
            return file_path
        except Exception:
            raise ValueError("Le fichier sélectionné n'est pas une image valide.")
    return None