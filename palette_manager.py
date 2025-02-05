import os
import json

class PaletteManager:
    def __init__(self, palette_dir="palettes"):
        """
        Initialise le gestionnaire de palettes.
        :param palette_dir: Dossier où les palettes sont enregistrées.
        """
        self.palette_dir = palette_dir
        os.makedirs(self.palette_dir, exist_ok=True)

    def save_palette(self, name, color_mapping):
        """
        Enregistre une palette de couleurs sous un nom donné.
        :param name: Nom de la palette.
        :param color_mapping: Dictionnaire des correspondances de couleurs.
        """
        file_path = os.path.join(self.palette_dir, f"{name}.json")
        with open(file_path, "w") as f:
            json.dump(color_mapping, f)
        print(f"Palette '{name}' enregistrée.")

    def load_palette(self, name):
        """
        Charge une palette de couleurs par son nom.
        :param name: Nom de la palette.
        :return: Dictionnaire des correspondances de couleurs.
        """
        file_path = os.path.join(self.palette_dir, f"{name}.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"La palette '{name}' n'existe pas.")
        with open(file_path, "r") as f:
            return json.load(f)

    def list_palettes(self):
        """
        Liste toutes les palettes disponibles.
        :return: Liste des noms de palettes.
        """
        return [os.path.splitext(f)[0] for f in os.listdir(self.palette_dir) if f.endswith(".json")]